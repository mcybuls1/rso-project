from flask import Flask

class TestSerwerWWW(object):
    app = Flask(__name__)
    def __init__(self):
        self.aaa = 'aaa'

    def run(self):
        self.app.run(host='0.0.0.0', debug=True)

    @app.route('/')
    def hello_word():
        return 'hello'

if __name__=='__main__':
    www = TestSerwerWWW()
    www.run()