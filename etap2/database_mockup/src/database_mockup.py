from flask import Flask, jsonify

database_mockup = Flask(__name__)

users = [
         {
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
                      }},
         {
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
                      }},
          {
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
]

@database_mockup.route('/')
def index():
    return jsonify({'users': users})

@database_mockup.route('/rso/users/', methods=['GET'])
def get_tasks():
    return jsonify({'users': users})

if __name__ == '__main__':
    database_mockup.run(debug=True)