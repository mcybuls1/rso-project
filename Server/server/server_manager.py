
class ServerManager(object):
    def __init__(self, configuration, image_manager, user_manager, auth_manager):
        self.configuration = configuration
        self.image_manager = image_manager
        self.user_manager = user_manager
        self.auth_manager = auth_manager

    def login(self, username, password):
        return self.auth_manager.login(username, password)
    
    def logout(self, session_key):
        return self.auth_manager.logout(session_key);
    
    def get_images(self, user_id):
        #TODO authorizations
        
        return self.image_manager.get_images(user_id);
    
    def get_image(self, user_id, image_id):
        #TODO authorizations
        
        return self.image_manager.get_image(image_id);
        
    def upload_image(self, user_id, image):
        #TODO authorizations
        
        return self.image_manager.upload_image(image);
    
    def delete_image(self, user_id, image_id):
        #TODO authorizations
        
        return self.image_manager.delete_image(image_id);
    
    def share_image(self, user_id, image_id, shared_for_user_id):
        #TODO authorizations
        
        return self.image_manager.share_image(image_id, shared_for_user_id);
    
    def unshare_image(self, user_id, image_id, shared_for_user_id):
        #TODO authorizations
        
        return self.image_manager.unshare_image(image_id, shared_for_user_id);
    
    def create_user(self, username, password):
        #TODO authorizations
        
        return self.user_manager.create_user()