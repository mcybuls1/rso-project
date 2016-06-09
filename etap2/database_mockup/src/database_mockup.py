from flask import Flask, jsonify, abort, make_response, request

database_mockup = Flask(__name__)

users = {
         
          'John_hash': {
                      'user_name': 'John',
                      'user_password': 'pass1',
                      'friends': [{ 
                                   'user_hash': 'Ana_hash',
                                   'user_name': 'Ana'
                                }], 
                      'images': [{
                                  'photo_hash': 'hash1'
                                  },
                                 {
                                  'photo_hash': 'hash2'
                                  }]
                      },
         
        'Eric_hash': {
                      'user_name': 'Eric',
                      'user_password': 'pass2',
                      'friends': [{ 
                                   'user_hash': 'Ana_hash',
                                   'user_name': 'Ana'
                                   },
                                  {
                                   'user_hash': 'John_hash',
                                   'user_name': 'John'
                                   }],
                      'images': [{
                                  'photo_hash': 'hash3'
                                  }]
                      },
        
        'Ana_hash': {
                     'user_name': 'Ana',
                     'user_password': 'pass3',
                     'images': [{
                                 'photo_hash': 'hash4'
                                 },
                                {
                                 'photo_hash': 'hash5'
                                 }]
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