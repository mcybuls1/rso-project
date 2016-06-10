import time

import binascii
import io

import requests
from flask import Flask, request, abort, jsonify, make_response
from flask.blueprints import Blueprint
from multiprocessing import Process
import hashlib
from flask.ext.httpauth import HTTPBasicAuth
from flask.helpers import send_file
from werkzeug.exceptions import NotFound
from tempfile import NamedTemporaryFile


class DB_API(object):

    def __init__(self):
        self.port = None
        self.ip = 'http://0.0.0.0:'

    def get_user(self, user_hash):
        # /rso/users/user_hash
        r = requests.get(url=self.ip+str(self.port)+'/rso/users/'+user_hash)
        return r

    def put_user(self, username, dict):
        pass

    def get_photo(self, hash):
        r = requests.get(url=self.ip + str(self.port) + '/rso/get_file/' + hash)
        return send_file(r.content)

    def put_photo(self, hash, file):
        files = {'file': io.BytesIO(file)}
        r = requests.post(url=self.ip + str(self.port) + '/rso/put_file/' + hash,
                          files=files)
        return r





class Serwer(object):
    def __init__(self, port):
        self.app = None
        self.port = port
        self.app = Flask(__name__)

        # self.app.debug = True

        self.auth = HTTPBasicAuth()
        self.db_api = DB_API()

        self._make_and_register_blueprint()


    def _make_and_register_blueprint(self):
        blueprint = Blueprint(__name__, __name__)

        @self.auth.get_password
        def get_password(username):
            # response_db = self.db_api.get_user(username)
            response_db = self.db_api.get_user(self.hash(username))
            if response_db.status_code == 404:
                return None
            slownik = response_db.json()
            # slownik = response_db
            if slownik != None:
                return slownik['password']
            return None

        @self.auth.error_handler
        def unauthorized():
            abort(401)

        @blueprint.route('/hello', methods=['POST', 'GET'])
        @self.auth.login_required
        def hello():
            return self._hello()

        @blueprint.route('/api/login', methods=['POST', 'GET'])
        @self.auth.login_required
        def login():
            return self._login(request)

        @blueprint.route('/api/follow_friend', methods=['POST'])
        @self.auth.login_required
        def follow_friend():
            return self._follow_friend(request)

        @blueprint.route('/api/get_photos_list', methods=['POST'])
        @self.auth.login_required
        def get_photos_list():
            return self._get_photos_list(request)

        @blueprint.route('/api/get_photo', methods=['POST'])
        @self.auth.login_required
        def get_photo():
            return self._get_photo(request)

        @blueprint.route('/api/add_photo', methods=['POST'])
        @self.auth.login_required
        def add_photo():
            return self._add_photo(request)

        self.app.register_blueprint(blueprint)

    def _hello(self):
        return "hello"

    def _login(self, request):
        return jsonify({'status': 'ok'})

    def _follow_friend(self, request):
        new_friend_name = request.values['friend']
        new_friend_hash = self.hash(new_friend_name)
        res_db = self.db_api.get_user(new_friend_hash)
        if res_db.status_code == 404:
            return jsonify({'error': 'no such user'}), 404
        zleceniodawca_login = request.authorization['username']
        # todo zleceniodawca_hash
        zleceniodawca_hash = self.hash(zleceniodawca_login)

        res_db2 = self.db_api.get_user(new_friend_hash)
        if res_db2.status_code == 404:
            return jsonify({'error': 'no such user'}), 404
        zleceniodawca_dict = res_db.json()
        zleceniodawca_dict['friends'].append(new_friend_hash)
        self.db_api.put_user(zleceniodawca_hash, zleceniodawca_dict)
        return jsonify({'status': 'ok'})

    def _get_photos_list(self, request):
        user_name = request.values['friend']
        user_hash = self.hash(user_name)
        res_db = self.db_api.get_user(user_hash)
        if res_db.status_code == 404:
            return jsonify({'error': 'no such user'}), 404
        user_dict = res_db.json()
        return jsonify({'status': 'ok', 'images':user_dict['images']})

    def _get_photo(self, request):
        photo_hash = request.values['photo_hash']
        zdjecie = self.db_api.get_photo(photo_hash)
        # if res_db.status_code == 404:
        #     return jsonify({'error': 'no such user'}), 404
        return zdjecie
        return send_file(zdjecie)

    def _add_photo(self, request):
        user_name = request.authorization['username']
        user_hash = self.hash(user_name)
        file_hash = self.hash_bin(request.files['file'].stream.read())
        request.files['file'].stream.seek(0)
        slownik_usera = self.db_api.get_user(user_hash=user_hash).json()
        slownik_usera['images'].append(file_hash)
        self.db_api.put_user(user_hash, slownik_usera)
        # db_res= self.db_api.put_photo(hash=file_hash, file=request.files['file'])
        db_res = self.db_api.put_photo(hash=file_hash,
                                       file=request.files['file'].stream.read())
        if db_res.status_code == 200:
            return jsonify({'status': 'zaladowano plik'}), 200
        else:
            print('ERROR ADD PHOTO SERWER')



    def hash(self, text):
        return hashlib.md5(binascii.a2b_qp(text)).hexdigest()

    def hash_bin(self, bin):
        return hashlib.md5(bin).hexdigest()


    def startProcess(self):
        self.process = Process(target=self.app.run, args=('0.0.0.0', self.port))
        self.process.start()

    def join(self):
        self.process.join()

    def terminate(self):
        self.process.terminate()

if __name__ == '__main__':
    www = Serwer(port=5677)
    www.startProcess()

    # print("spie")
    # time.sleep(7)
    #
    # www.terminate()