import redis
import hashlib
import time

from server.auth.authentication_error import AuthenticationError

class AuthenticationManager(object):
    def __init__(self, configuration, user_manager):
        self.user_manager = user_manager
        self.r = redis.StrictRedis(host=configuration.get_db_host(), port=configuration.get_db_port(), db=configuration.get_db_db())

    def authenticate(self, username, password):
        user = self.user_manager.get_user_by_name(username)
        
        raw_password = username + password + user.get_created_at()  
        hashed_password = hashlib.md5( (raw_password).encode() ).hexdigest()
        
        if hashed_password == user.get_password_hash():
            session_key = user.get_session_key()
            if session_key is None:
                session_key = hashlib.md5( (user.get_username() + time.time()).encode() ).hexdigest()
                pipe = self.r.pipeline()
                pipe.hset('user:' + user.get_user_id(), 'session_key', session_key)
                pipe.hset('session_keys', session_key, user.get_user_id())
                pipe.execute()
                
            return session_key
                
        raise AuthenticationError('Invalid user credentials!')
    
    def unauthenticate(self, username):
        # TODO