from flask import Flask, abort
import sys
from flask.json import jsonify
from flask.globals import request

app = Flask(__name__)

def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    app.run(debug=True)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"


@app.route('/login', methods=['POST'])
def login():
    if not request.json or not 'username' in request.json:
        abort(400)
    if not request.json or not 'password' in request.json:
        abort(400)
        
    username = request.json['username']
    password = request.json['password']
        
    return "Hello, World!"


@app.route('/<int:user_id>/images/', methods=['GET'])
def get_images(user_id):
    return jsonify({'user_id': user_id})

@app.route('/<int:user_id>/images/<int:image_id>', methods=['GET'])
def get_image(user_id, image_id):
    return jsonify({'user_id': user_id, 'image_id': image_id})

@app.route('/<int:user_id>/images/', methods=['POST'])
def upload_image(user_id):
    if not request.json or not 'title' in request.json:
        abort(400)
        
    return jsonify({'title': request.json['title']})


@app.route('/<int:user_id>/images/<int:image_id>', methods=['DELETE'])
def delete_image(user_id, image_id):
    return jsonify({'user_id': user_id, 'image_id': image_id})


if __name__ == '__main__':
    sys.exit(main())
