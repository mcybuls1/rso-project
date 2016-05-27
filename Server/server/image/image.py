
class Image(object):
    def __init__(self, owner_id = None, description = None, data = None):
        self.image_id = None
        self.owner_id = owner_id
        self.description = description
        self.data = data
        
    def serialize(self):
        return {'image_id': self.image_id,
                'owner_id': self.owner_id,
                'description': self.description,
                'data': self.data}
        
