import hashlib
import time

import redis

from server.user.user_not_found_error import UserNotFoundError


class UserManager(object):
    def __init__(self, config):
        self.r = redis.StrictRedis(host=config.get_db_host(), port=config.get_db_port(), db=config.get_db_db())
        self.r.set('next_user_id', 1000)
        
    def create_user(self, username, password):
        creation_time = time.gmtime(time.time())
        raw_password = username + password + creation_time 
        hashed_password = hashlib.md5( (raw_password).encode() ).hexdigest()
            
        user_id = self.r.incr('next_user_id')
        pipe = self.r.pipeline()
        pipe.hmset('user:' + user_id, 'username ' + username + ' password ' + hashed_password + ' creation_time ' + creation_time)
        pipe.hset('users', username, user_id)
        pipe.execute()
        
        return user_id
    
    def get_user_by_name(self, username):
        user_id = self.r.hget('users', username)
        
        if user_id is None:
            raise UserNotFoundError("User username=" + username + " does not exist!")
        
        self.r.hmget('user'+user_id)
    
        