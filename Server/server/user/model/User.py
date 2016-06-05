class User(object):
    

    def set_user_id(self, user_id):
        self._user_id = user_id
        
    def get_user_id(self):
        return self._user_id
        
    def set_username(self, username):
        self._username = username
        
    def get_username(self):
        return self._username
        
    def set_password_hash(self, password_hash):
        self._password_hash = password_hash
        
    def get_password_hash(self):
        return self._password_hash
        
    def set_created_at(self, created_at):
        self._created_at = created_at
        
    def get_created_at(self):
        return self._created_at
    
    def set_session_key(self, session_key):
        self._session_key = session_key
    
    def get_session_key(self):
        return self._session_key
        