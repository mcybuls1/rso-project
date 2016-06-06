import sys

from flask import Flask
from flask.json import jsonify
from flask.globals import request

from server.server_manager import ServerManager
from server.image.image_manager import ImageManager
from server.user.user_manager import UserManager
from server.image.image_not_found_error import ImageNotFoundError
from server.user.user_not_found_error import UserNotFoundError
from server.image.image import Image
from server.auth.auth_manager import AuthManager 

app = Flask(__name__)
server_manager = None

class StubConfiguration(object):
    _db_host = '192.168.56.2'
    _db_port = 6379
    _db_db = 0
    
    def get_db_host(self):
        return StubConfiguration._db_host
    
    def get_db_port(self):
        return StubConfiguration._db_port
    
    def get_db_db(self):
        return StubConfiguration._db_db

def main(argv=None):
    config = get_config(argv)
    init(config)
    
    return start()

def get_config(argv):
    if argv is None:
        argv = sys.argv
        
    return StubConfiguration();
    
def init(config):
    image_manager = ImageManager(config)
    user_manager = UserManager(config)
    auth_manager = AuthManager(config, user_manager)
    global server_manager
    server_manager = ServerManager(config, image_manager, user_manager, auth_manager)
        
def start():
    app.run(debug=True)
    
def _on_not_found_error(message):
    response = jsonify(success='false', error=message)
    response.status_code = 404
    
    return response
    
def _on_user_not_found_error():
    return _on_not_found_error('User not found!')

def _on_image_not_found_error():
    return _on_not_found_error('Image not found!')

def _on_bad_request(message):
    if message is None:
        message = ''
    else:
        message = ' ' + message
        
    response = jsonify(success='false', error='Bad request!' + message)
    response.status_code = 400
    
    return response

def _internal_error():
    response = jsonify(success='false', error='Internal error!')
    response.status_code = 500
    
    return response

#######
####### USER OPERATIONS
#######
@app.route('/login', methods=['POST'])
def login():
    try:
        if not request.json:
            return _on_bad_request()
        
        if not 'username' in request.json:
            return _on_bad_request("Argument 'username' is missing!")
            
        if not 'password' in request.json:
            return _on_bad_request("Argument 'password' is missing!")
            
        username = request.json['username']
        password = request.json['password']
        
        api_key = server_manager.login(username, password)
        
        if api_key != None:
            response = jsonify({'success':'true', 'api_key': api_key, 'id':42})
            response.set_cookie('api_key', api_key)
            return response
        else:
            return _internal_error()
    except UserNotFoundError:
        return _on_user_not_found_error()

@app.route('/logout', methods=['POST'])
def logout():    
    try:
        if not request.json:
            return _on_bad_request()
        
        if not 'api_key' in request.json:
            return _on_bad_request("Argument 'api_key' is missing!")
        
        api_key = request.json['api_key']
        
        result = server_manager.logout(api_key)
        
        if result:
            return jsonify(success='true')
        else:
            return jsonify(success='false')
        
    except UserNotFoundError:
        return _on_user_not_found_error()
    

#######
####### IMAGE OPERATIONS
#######
@app.route('/<int:user_id>/images/', methods=['GET'])
def get_images(user_id):
    try:
        images = server_manager.get_images(user_id)
        
        images_array = {}
        for image in images:
            images_array[image.image_id] = image.serialize()
        
        response = {'images': images_array,
                    'user_id': user_id}
        
        return jsonify(response)
    except ImageNotFoundError:
        return _on_image_not_found_error()
    except UserNotFoundError:
        return _on_user_not_found_error()


@app.route('/<int:user_id>/images/<int:image_id>', methods=['GET'])
def get_image(user_id, image_id):
    try:
        image = server_manager.get_image(user_id, image_id)
        if image == None:
            return _on_image_not_found_error()
            
        return jsonify(image.serialize())
    except ImageNotFoundError:
        return _on_image_not_found_error()
    except UserNotFoundError:
        return _on_user_not_found_error()

@app.route('/<int:user_id>/images/', methods=['POST'])
def upload_image(user_id):
    try:
        if not request.json or not 'description' in request.json or not 'data' in request.json:
            return _on_bad_request()
            
        result = server_manager.upload_image(user_id, Image(user_id, request.json['description'], request.json['data']));
        
        return jsonify(result.serialize())
    except UserNotFoundError:
        return _on_user_not_found_error()

@app.route('/<int:user_id>/images/<int:image_id>', methods=['DELETE'])
def delete_image(user_id, image_id):
    try:
        result = server_manager.delete_image(user_id, image_id);
        
        if result:
            return jsonify(success='true')
        
        return jsonify(success='false')
    except ImageNotFoundError:
        return _on_image_not_found_error()
    except UserNotFoundError:
        return _on_user_not_found_error()

@app.route('/<int:user_id>/images/<int:image_id>/share/<int:shared_for_user_id>', methods=['POST', 'PUT'])
def share_image(user_id, image_id, shared_for_user_id):
    try:
        result = server_manager.share_image(user_id, image_id, shared_for_user_id);
        
        if result:
            return jsonify(success='true')
        
        return jsonify(success='false')
    except ImageNotFoundError:
        return _on_image_not_found_error()
    except UserNotFoundError:
        return _on_user_not_found_error()

@app.route('/<int:user_id>/images/<int:image_id>/share/<int:shared_for_user_id>', methods=['DELETE'])
def unshare_image(user_id, image_id, shared_for_user_id):
    try:
        result = server_manager.unshare_image(user_id, image_id, shared_for_user_id);
    
        if result:
            return jsonify(success='true')
        
        return jsonify(success='false')
    except ImageNotFoundError:
        return _on_image_not_found_error()
    except UserNotFoundError:
        return _on_user_not_found_error()
        
@app.route('/user', methods=['POST'])
def create_user():
    try:
        result = server_manager.create_user(request.json['username'], request.json['password']);
    
        if result:
            return jsonify(success='true', user_id=result)
        
        return jsonify(success='false')
    except ImageNotFoundError:
        return _on_image_not_found_error()
    except UserNotFoundError:
        return _on_user_not_found_error()

if __name__ == '__main__':
    sys.exit(main())
