from flask import Flask, jsonify, abort, make_response, request, send_file
from flask.blueprints import Blueprint
from multiprocessing import Process
import logging
import os

logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = '/db_data'
USERS = {

    '61409aa1fd47d4a5332de23cbf59a36f': {
        'name': 'John',
        'password': 'pass1',
        'friends': ['Ana'],
        'images': ['hash1', 'hash2']
    },

    '77dcd555f38b965d220a13a3bb080260': {
        'name': 'Eric',
        'password': 'pass2',
        'friends': ['Ana', 'John'],
        'images': ['hash3']
    },

    '9aba45a7f1999a9c5fc96ef2a45810fb': {
        'name': 'Ana',
        'password': 'pass3',
        'images': ['hash', 'hash5']
    }

}


class DataBaseSerwer():
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.users = USERS
        # self.app.debug = True
        self._make_and_register_blueprint()

    def _make_and_register_blueprint(self):
        blueprint = Blueprint(__name__, __name__)

        @blueprint.route('/')
        def index():
            return jsonify({'users': self.users})

        @blueprint.route('/rso/users/', methods=['GET'])
        def get_users():
            return jsonify({'users': self.users})

        @blueprint.route('/rso/users/<string:user_hash>', methods=['GET'])
        def get_user(user_hash):
            if not user_hash in self.users.keys():
                abort(404)
            user = self.users.get(user_hash)
            if len(user) == 0:
                abort(404)
            return jsonify(user)

        @blueprint.errorhandler(404)
        def not_found(error):
            return make_response(jsonify({'error': 'Not found'}), 404)

        @blueprint.route('/rso/users/<string:user_hash>', methods=['POST'])
        def update_user(user_hash):
            if not request.json:
                abort(400)
            if user_hash in self.users.keys():
                self.users[user_hash] = request.json
                return jsonify({'user': request.json}), 201
            abort(400)

        @blueprint.route('/rso/put_file/<string:file_hash>', methods=['POST'])
        def upload_file(file_hash):
            if request.method == 'POST':
                # check if the post request has the file part
                if 'file' not in request.files:
                    abort(400)
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    abort(400)
                if file:

                    with open(file_hash + '.jpg', 'wb') as f:
                        f.write(file.read())

                    # file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], file_hash))
                    return jsonify({'status': 'ok'}), 200
                    # return redirect(url_for('uploaded_file', filename=filename))

        @blueprint.route('/rso/get_file/<string:file_hash>', methods=['GET'])
        def get_file(file_hash):
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], file_hash)
            if os.path.isfile(file_path+'.jpg'):
                return send_file(file_path)
            abort(404)

        self.app.register_blueprint(blueprint)

    def startProcess(self):
        self.process = Process(target=self.app.run, args=('0.0.0.0', self.port))
        self.process.start()

    def join(self):
        self.process.join()

    def terminate(self):
        self.process.terminate()


if __name__ == '__main__':
    www1 = DataBaseSerwer(port=80)
    www1.startProcess()