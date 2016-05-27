import sys

from flask import Flask, abort
from flask.json import jsonify
from flask.globals import request

from server.server_manager import ServerManager
from server.image.image_manager import ImageManager
from server.user.user_manager import UserManager

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
    server_manager = ServerManager(config, image_manager, user_manager)
        
def start():
    app.run(debug=True)

#######
####### USER OPERATIONS
#######
@app.route('/login', methods=['POST'])
def login():
    if not request.json or not 'username' in request.json:
        abort(400)
    if not request.json or not 'password' in request.json:
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
    images = server_manager.get_images(user_id)
    
    return jsonify(images)

@app.route('/<int:user_id>/images/<int:image_id>', methods=['GET'])
def get_image(user_id, image_id):
    image = server_manager.get_image(user_id, image_id)
    return jsonify(image)

@app.route('/<int:user_id>/images/', methods=['POST'])
def upload_image(user_id):
    if not request.json or not 'title' in request.json:
        abort(400)
        
    return jsonify({'title': request.json['title']})

@app.route('/<int:user_id>/images/<int:image_id>', methods=['DELETE'])
def delete_image(user_id, image_id):
    return jsonify({'user_id': user_id, 'image_id': image_id})

@app.route('/<int:user_id>/images/<int:image_id>/shared/<int:shared_for_user_id>', methods=['POST', 'PUT'])
def share_image(user_id, image_id, shared_for_user_id):
    return jsonify({'user_id': user_id, 'image_id': image_id})

@app.route('/<int:user_id>/images/<int:image_id>/shared/<int:shared_for_user_id>', methods=['DELETE'])
def unshare_image(user_id, image_id, shared_for_user_id):
    return jsonify({'user_id': user_id, 'image_id': image_id})

if __name__ == '__main__':
    sys.exit(main())
