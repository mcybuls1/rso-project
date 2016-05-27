from server.image.image import Image

class ImageManager(object):
    _images = {}
    
    # user_id => images_ids
    _user_visible_images = {}
    
    _next_image_id = 1
    
    def __init__(self, config):
        self.config = config
        self.upload_image(Image(1, 'Image 01', 'dump'))
        self.upload_image(Image(1, 'Image 02', 'dump'))
        self.upload_image(Image(2, 'Image 03', 'dump'))
        self.upload_image(Image(3, 'Image 04', 'dump'))
        self.upload_image(Image(3, 'Image 05', 'dump'))
        self.upload_image(Image(3, 'Image 06', 'dump'))
        self.upload_image(Image(3, 'Image 07', 'dump'))
        
        self.share_image(1, 3)
        self.share_image(1, 4)
        self.share_image(2, 1)
        self.share_image(2, 6)
        self.share_image(2, 7)
        self.share_image(3, 1)
        self.share_image(3, 2)
    
    def get_images(self, user_id):
        user_images = set()
        
        for image_id in self._user_visible_images[user_id]:
            user_images.add(self._images[image_id])
        
        return user_images;
    
    def get_image(self, image_id):
        if image_id in self._images:
            return self._images.get(image_id)
        
        return None
        
    def upload_image(self, image):
        image_id = self._next_image_id
        self._next_image_id = self._next_image_id + 1
        
        image.image_id = image_id
        
        self._images[image_id] = image
        self.share_image(image_id, image.owner_id)
        
        return image
    
    def delete_image(self, image_id):
        for shared_images in self._user_visible_images.values():
            if image_id in shared_images:
                shared_images.remove(image_id)
        
        del self._images[image_id]
        
        return True;
    
    def share_image(self, image_id, user_id):
        if not user_id in self._user_visible_images:
            self._user_visible_images[user_id] = set()
            
        self._user_visible_images[user_id].add(image_id)
        
        return True
    
    def unshare_image(self, image_id, user_id):
        self._user_visible_images[user_id].remove(image_id)
        
        return True
    