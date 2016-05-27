from flask import Flask

app = Flask(__name__)

class ServerManager(object):
    def __init__(self, configuration, image_manager, user_manager):
        self.configuration = configuration
        self.user_manager = user_manager
        self.image_manager = image_manager

    def login(self, username, password):
        return self.user_manager.login(username, password)
    
    def logout(self, username):
        return self.user_manager.logout(username);
    
    def get_images(self, user_id):
        #TODO authorizations
        
        return self.image_manager.get_images();
    
    def get_image(self, user_id, image_id):
        #TODO authorizations
        
        return self.image_manager.get_image(image_id);
        
    def upload_image(self, user_id, image):
        #TODO authorizations
        
        return self.upload_image(user_id, image);
    
    def delete_image(self, user_id, image_id):
        #TODO authorizations
        
        return self.delete_image(user_id, image_id);
    
    def share_image(self, user_id, image_id, share_for_user_id):
        #TODO authorizations
        
        return self.share_image(user_id, image_id, share_for_user_id);
    
    def unshare_image(self, user_id, image_id, share_for_user_id):
        #TODO authorizations
        
        return self.unshare_image(user_id, image_id, share_for_user_id);