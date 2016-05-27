from flask import Flask

app = Flask(__name__)

class ServerManager(object):
    def __init__(self, configuration, image_manager, user_manager):
        self.configuration = configuration
        self.user_manager = user_manager
        self.image_manager = image_manager

    def get_user_manager(self):
        return self.user_manager
    
    def get_image_manager(self):
        return self.image_manager