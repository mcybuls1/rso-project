from flask import Flask, jsonify, abort, make_response, request

database_mockup = Flask(__name__)

users = {
         
          'John_hash': {
                      'name': 'John',
                      'password': 'pass1',
                      'friends': ['Ana'], 
                      'images': ['hash1', 'hash2']
                      },
         
        'Eric_hash': {
                      'name': 'Eric',
                      'password': 'pass2',
                      'friends': ['Ana', 'John'],
                      'images': ['hash3']
                      },
        
        'Ana_hash': {
                     'name': 'Ana',
                     'password': 'pass3',
                     'images': ['hash', 'hash5']
                     }
                         
}

@database_mockup.route('/')
def index():
    return jsonify({'users': users})

@database_mockup.route('/rso/users/', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@database_mockup.route('/rso/users/<string:user_hash>', methods=['GET'])
def get_user(user_hash):
    if not user_hash in users.keys() :
        abort(404)
    user = users.get(user_hash)
    if len(user) == 0:
        abort(404)
    return jsonify(user)

@database_mockup.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@database_mockup.route('/rso/users/<string:user_hash>', methods=['POST'])
def update_user(user_hash):
    if not request.json:
        abort(400)
    user = users[user_hash]
    if len(user) == 0:
        abort(400)
    users[user_hash] = request.json
    return jsonify({'user': request.json}), 201

if __name__ == '__main__':
    database_mockup.run(debug=True, host="0.0.0.0")