import hashlib
from abc import abstractmethod, ABCMeta

import flask
import time
from flask import Flask, request, abort, jsonify
from flask.blueprints import Blueprint
from multiprocessing import Process

class TestSerwerNormal():
    def __init__(self, port):
        self.app = None
        self.port = port
        self.app = Flask(__name__)
        # self.app.debug = True
        self._make_and_register_blueprint()


    def _make_and_register_blueprint(self):
        blueprint = Blueprint(__name__, __name__)

        @blueprint.route('/hello', methods=['POST', 'GET'])
        def hello():
            return self._hello()

        @blueprint.route('/login', methods=['POST'])
        def login():
            return self._login(request)

        @blueprint.route('/test_zadanie', methods=['POST', 'GET'])
        def test_zadanie():
            return self._test_zadanie(request)

        self.app.register_blueprint(blueprint)

    def _hello(self):
        return "hello"
        # raise NotImplementedError

    def _login(self, request):
        akceptowalny_login = 'login'
        akceptowalne_haslo = 'haslo'
        if request.values['username'] == akceptowalny_login \
            and request.values['password'] == akceptowalne_haslo:
            login_plus_haslo = akceptowalny_login + akceptowalne_haslo
            czas = '2016-05-25-18-58-42'
            md5_hex = hashlib.md5( (login_plus_haslo+czas).encode() ).hexdigest()
            #dla login=login i haslo=haslo token=60febe74408dd25f11999b4a90548980
            return jsonify({'api_key': md5_hex, 'id': 42})
            # return md5_hex
        else:
            abort(401)

    def _test_zadanie(self, request):
        return request.values['test_text']

    def startProcess(self):
        self.process = Process(target=self.app.run, args=('0.0.0.0', self.port))
        self.process.start()

    def join(self):
        self.process.join()

    def terminate(self):
        self.process.terminate()


class TestSerwerBadLogin(TestSerwerNormal):
    def _login(self, request):
        abort(401)

    def _test_zadanie(self, request):
        abort(401)

class TestSerwerTimeout(TestSerwerNormal):
    timeout = 0.6
    def _login(self, request):
        time.sleep(self.timeout)
        return "Timeout_login"

    def _test_zadanie(self, request):
        time.sleep(self.timeout)
        return "Timeout_test_zadanie"

class TestSerwerError(TestSerwerNormal):
    '''504 - Service Unavalible'''
    def _test_zadanie(self, request):
        abort(504)




if __name__ == '__main__':
    www1 = TestSerwerBadLogin(port=5070)
    www1.startProcess()

    # www2 = TestSerwerKlient2(port=5075)
    # www2.startProcess()
