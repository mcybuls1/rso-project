class AuthenticationError(RuntimeError):

    def __init__(self, message):
        self.message = message
        