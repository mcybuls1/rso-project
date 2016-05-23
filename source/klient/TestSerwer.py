from flask import Flask
from multiprocessing import Process

class TestKlientSerwerWWW(object):
    app = Flask("APP")
    def __init__(self, text, port=5000):
        # self.app = app = Flask(__name__)
        self.port = port
        self.text = text

    def run(self):
        self.app.run(host='0.0.0.0', debug=True, port=self.port)

    @app.route('/')
    def hello_word():
        print("przetwarzam request'a")
        return "hello word"

# class TestKlientSerwerWWW2(TestKlientSerwerWWW):

if __name__=='__main__':
    www = TestKlientSerwerWWW(text="jeden", port=5000)
    www2 = TestKlientSerwerWWW(text="dwa", port=5001)
    p1 = Process(target=www.run)
    p2 = Process(target=www2.run)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
