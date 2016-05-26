import hashlib
from abc import abstractmethod, ABCMeta

import flask
import time
from flask import Flask, request, abort
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

        @blueprint.route('/hello')
        def hello():
            return self._hello()

        @blueprint.route('/login', methods=['POST'])
        def login():
            return self._login(request)

        self.app.register_blueprint(blueprint)

    def _hello(self):
        return "hello"
        # raise NotImplementedError

    def _login(self, request):
        akceptowalny_login = 'login'
        akceptowalne_haslo = 'haslo'
        if request.values['login'] == akceptowalny_login \
            and request.values['haslo'] == akceptowalne_haslo:
            login_plus_haslo = request.values['login'] + request.values['haslo']
            czas = '2016-05-25-18-58-42'
            md5_hex = hashlib.md5( (login_plus_haslo+czas).encode() ).hexdigest()
            #dla login=login i haslo=haslo token=60febe74408dd25f11999b4a90548980
            return md5_hex
        else:
            abort(401)
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

class TestSerwerLongTimeLogin(TestSerwerNormal):
    def _login(self, request):
        time.sleep(2)
        return "LongTimeLogin"





if __name__ == '__main__':
    www1 = TestSerwerBadLogin(port=5070)
    www1.startProcess()

    # www2 = TestSerwerKlient2(port=5075)
    # www2.startProcess()
