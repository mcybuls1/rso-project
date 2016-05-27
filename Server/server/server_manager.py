from flask import Flask
from redis import Redis

app = Flask(__name__)

class Server(object):
    def __init__(self, configuration):
        self.configuration = configuration;

    @app.route('/')
    def index(self):
        return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)