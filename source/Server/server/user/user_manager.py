import hashlib
import time

from server.user.model.user import User

import redis

from server.user.user_not_found_error import UserNotFoundError


class UserManager(object):
    def __init__(self, config):
        self.r = redis.StrictRedis(host=config.get_db_host(), port=config.get_db_port(), db=config.get_db_db())

        pipe = self.r.pipeline()
        if not pipe.exists('next_user_id'):
            pipe.set('next_user_id', 1000)
            pipe.execute()
        
        self.create_user('user01', 'pass01')
        
    def create_user(self, username, password):
            
        user_id = self.r.incr('next_user_id')
        user_key = 'user:' + str(user_id)
        
        while 1:
            try:        
                pipe = self.r.pipeline()
                pipe.watch(user_key)
                if not pipe.exists(user_key):
                    pipe.multi()
                    
                    creation_time = time.ctime()
                    raw_password = username + password + creation_time 
                    hashed_password = hashlib.md5( (raw_password).encode() ).hexdigest()
                    
                    pipe.hmset(user_key, {'username': str(username), 'password': str(hashed_password), 'creation_time': str(creation_time)})
                    pipe.hset('users', username, user_id)
                    pipe.execute()
                else:
                    pipe.unwatch()
                    break
            except redis.exceptions.WatchError:
                pass
        
        return user_id
    
    def _decode(self, val):
        if val is not None:
            return val.decode('UTF-8')
        else:
            return None
    
    def get_user_by_name(self, username):
        user_id = self.r.hget('users', username)
        
        if user_id is None:
            raise UserNotFoundError("User username=" + username + " does not exist!")
        
        user_id = self._decode(user_id)
        
        result = self.r.hmget('user:'+ str(user_id), 'username', 'password', 'creation_time', 'session_key')
        username = self._decode(result[0])
        password = self._decode(result[1])
        creation_time = self._decode(result[2])
        session_key = self._decode(result[3])
        return User(user_id, username, password, creation_time, session_key)
    
        