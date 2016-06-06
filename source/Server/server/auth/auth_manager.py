import redis
import hashlib
import time

from server.auth.authentication_error import AuthenticationError
from server.auth.authorization_error import AuthorizationError

class AuthManager(object):
    def __init__(self, configuration, user_manager, image_manager):
        self.user_manager = user_manager
        self.image_manager = image_manager
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
    
    def check_authenticated(self, user_id, api_key):
        session_user_id = self._decode(self.r.hget('session_keys', api_key))
        if str(user_id) != str(session_user_id):
            raise AuthenticationError("Not authenticated!") 
    
    def check_is_owner(self, user_id, image_id, api_key):
        self.check_authenticated(user_id, api_key)
        
        image = self.image_manager.get_image(image_id)
        if image is not None and not str(image.owner_id) == str(user_id):
            raise AuthorizationError("Not authorized!")
        
        return True
            
    def check_authorized_get_image(self, user_id, image_id, api_key):
        self.check_authenticated(user_id, api_key)
        
        if self.check_is_owner(user_id, image_id, api_key):
            return
                
        result = self.r.sismember('user_images:' + str(user_id), image_id)
        if not result:
            raise AuthorizationError("Not authorized!")
        