
class Image(object):
    def __init__(self, image_id = None, owner_id = None, description = None, data = None, mime = None):
        self.image_id = image_id
        self.owner_id = owner_id
        self.description = description
        self.data = data
        self.mime = mime
        
    def serialize(self):
        return {'image_id': self.image_id,
                'owner_id': self.owner_id,
                'description': self.description,
                'data': self.data,
                'mime': self.mime}
        
