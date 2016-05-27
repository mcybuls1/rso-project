class UserManager(object):
    def __init__(self, config):
        self.config = config;
        
    def login(self, username, password):
        return True
    
    def logout(self, username):
        return True