import redis
import hashlib
import time

from server.auth.authentication_error import AuthenticationError

class AuthManager(object):
    def __init__(self, configuration, user_manager):
        self.user_manager = user_manager
        self.r = redis.StrictRedis(host=configuration.get_db_host(), port=configuration.get_db_port(), db=configuration.get_db_db())

    def login(self, username, password):
        user = self.user_manager.get_user_by_name(username)
        
        raw_password = username + password + user.get_created_at()  
        hashed_password = hashlib.md5( (raw_password).encode() ).hexdigest()
        
        if hashed_password == user.get_password_hash():
            session_key = user.get_session_key()
            if session_key is None:
                session_key = hashlib.md5( (user.get_username() + time.ctime()).encode() ).hexdigest()
                pipe = self.r.pipeline()
                pipe.hset('user:' + user.get_user_id(), 'session_key', session_key)
                pipe.hset('session_keys', session_key, user.get_user_id())
                pipe.execute()
                
            return session_key
                
        raise AuthenticationError('Invalid user credentials!')
    
    def _decode(self, val):
        if val is not None:
            return val.decode();
        
        return None
    
    def logout(self, session_key):
        user_id = self._decode(self.r.hget('session_keys', session_key))
        if user_id is not None:
            pipe = self.r.pipeline()
            pipe.hdel('session_keys', session_key)
            pipe.hdel('user:' + user_id, 'session_key')
            pipe.execute()
        
            return True
        
        return False