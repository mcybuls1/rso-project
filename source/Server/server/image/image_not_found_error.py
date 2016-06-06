class ImageNotFoundError(RuntimeError):
    
    def __init__(self, message):
        self.msg = message
        