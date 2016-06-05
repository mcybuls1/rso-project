import sys

from flask import Flask, abort
from flask.json import jsonify
from flask.globals import request

from server.server_manager import ServerManager
from server.image.image_manager import ImageManager
from server.user.user_manager import UserManager
from server.image.image_not_found_error import ImageNotFoundError
from server.user.user_not_found_error import UserNotFoundError
from server.image.image import Image

app = Flask(__name__)
server_manager = None

def main(argv=None):
    config = get_config(argv)
    init(config)
    
    return start()

def get_config(argv):
    if argv is None:
        argv = sys.argv
        
    return "";
    
def init(config):
    image_manager = ImageManager(config)
    user_manager = UserManager(config)
    global server_manager
    server_manager = ServerManager(config, image_manager, user_manager)
        
def start():
    app.run(debug=True)

#######
####### USER OPERATIONS
#######
@app.route('/login', methods=['POST'])
def login():
    try:
        if not request.json or not 'username' in request.json or not 'password' in request.json:
            abort(400)
            
        username = request.json['username']
        password = request.json['password']
        
        api_key = server_manager.get_user_manager.login(username, password)
        
        if api_key != None:
            response = jsonify({'api_key': api_key})
            response.set_cookie('api_key', api_key)
            return response
        else:
            abort(400)
    except UserNotFoundError:
        abort(404)

@app.route('/logout', methods=['POST'])
def logout():    
    response = jsonify({"success":True})
        
    api_key = request.cookies.get('api_key')
    if api_key != None:
        return response.set_cookie('api_key', '', expires=0)
    
    return response


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
        abort(404)
    except UserNotFoundError:
        abort(404)


@app.route('/<int:user_id>/images/<int:image_id>', methods=['GET'])
def get_image(user_id, image_id):
    try:
        image = server_manager.get_image(user_id, image_id)
        if image == None:
            abort(404)
            
        return jsonify(image.serialize())
    except ImageNotFoundError:
        abort(404)
    except UserNotFoundError:
        abort(404)

@app.route('/<int:user_id>/images/', methods=['POST'])
def upload_image(user_id):
    try:
        if not request.json or not 'description' in request.json or not 'data' in request.json:
            abort(400)
            
        result = server_manager.upload_image(user_id, Image(user_id, request.json['description'], request.json['data']));
        
        return jsonify(result.serialize())
    except UserNotFoundError:
        abort(404)

@app.route('/<int:user_id>/images/<int:image_id>', methods=['DELETE'])
def delete_image(user_id, image_id):
    try:
        result = server_manager.delete_image(user_id, image_id);
        
        if result:
            return jsonify(success = 'true')
        
        return jsonify(success = 'false')
    except ImageNotFoundError:
        abort(404)
    except UserNotFoundError:
        abort(404)

@app.route('/<int:user_id>/images/<int:image_id>/share/<int:shared_for_user_id>', methods=['POST', 'PUT'])
def share_image(user_id, image_id, shared_for_user_id):
    try:
        result = server_manager.share_image(user_id, image_id, shared_for_user_id);
        
        if result:
            return jsonify(success = 'true')
        
        return jsonify(success = 'false')
    except ImageNotFoundError:
        abort(404)
    except UserNotFoundError:
        abort(404)

@app.route('/<int:user_id>/images/<int:image_id>/share/<int:shared_for_user_id>', methods=['DELETE'])
def unshare_image(user_id, image_id, shared_for_user_id):
    try:
        result = server_manager.unshare_image(user_id, image_id, shared_for_user_id);
    
        if result:
            return jsonify(success = 'true')
        
        return jsonify(success = 'false')
    except ImageNotFoundError:
        abort(404)
    except UserNotFoundError:
        abort(404)
        
@app.route('/user', methods=['POST'])
def create_user():
    try:
        result = server_manager.create_user(request.json['username'], request.json['password']);
    
        if result:
            return jsonify(success = 'true', user_id = result)
        
        return jsonify(success = 'false')
    except ImageNotFoundError:
        abort(404)
    except UserNotFoundError:
        abort(404)

if __name__ == '__main__':
    sys.exit(main())
