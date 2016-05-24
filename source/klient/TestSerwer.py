from abc import abstractmethod, ABCMeta

from flask import Flask
from flask.blueprints import Blueprint
from multiprocessing import Process


class TestSerwerBase(metaclass=ABCMeta):
    def __init__(self, port):
        self.app = None
        self.port = port
        self.app = Flask(__name__)
        # self.app.debug = True
        self._make_and_register_blueprint()


    def _make_and_register_blueprint(self):
        blueprint = Blueprint(__name__, __name__)

        @blueprint.route('/')
        def hello():
            return self._hello()

        self.app.register_blueprint(blueprint)

    @abstractmethod
    def _hello(self):
        raise NotImplementedError

    def startProcess(self):
        self.process = Process(target=self.app.run, args=('0.0.0.0', self.port))
        self.process.start()

    def join(self):
        self.process.join()


class TestSerwerKlient1(TestSerwerBase):
    def _hello(self):
        return "111111"


class TestSerwerKlient2(TestSerwerBase):
    def _hello(self):
        return "222222"


if __name__ == '__main__':
    www1 = TestSerwerKlient1(port=5051)
    www1.startProcess()

    www2 = TestSerwerKlient2(port=5071)
    www2.startProcess()
