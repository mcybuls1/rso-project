from server.image.image import Image
import redis
from server.image.image_not_found_error import ImageNotFoundError
from server.user.user_not_found_error import UserNotFoundError
from redis.exceptions import WatchError

class ImageManager(object):
    _images = {}
    
    # user_id => images_ids
    _user_visible_images = {}
    
    _next_image_id = 1
    
    def __init__(self, config):
        self.r = redis.StrictRedis(host=config.get_db_host(), port=config.get_db_port(), db=config.get_db_db())
        pipe = self.r.pipeline()
        if not pipe.exists('next_image_id'):
            pipe.set('next_image_id', 5000)
            pipe.execute()
    
    
    def _decode(self, val):
        if val is not None:
            return val.decode('UTF-8')
        else:
            return None
        
    def get_images(self, user_id):
        user_images = set()
        user_id = str(user_id)
        
        if not self.r.exists('user:' + str(user_id)):
            raise UserNotFoundError("User " + str(user_id) + " does not exist!")
        
        user_images_ids = self.r.smembers('user_images:' + str(user_id))
        if user_images_ids is not None:
            for image_id in user_images_ids:
                result = self.r.hmget('image:' + self._decode(image_id), 'owner_id', 'description', 'data', 'mime')
                if result is not None:
                    user_images.add(Image(self._decode(image_id), self._decode(result[0]), self._decode(result[1]), self._decode(result[2]), self._decode(result[3])))
                
        return user_images;
    
    def get_image(self, image_id):
        image_id = str(image_id)
        
        if self.r.exists('image:' + str(image_id)):
            result = self.r.hmget('image:' + str(image_id), 'owner_id', 'description', 'data', 'mime')
            
            return Image(image_id, self._decode(result[0]), self._decode(result[1]), self._decode(result[2]), self._decode(result[3]))
        else:
            raise ImageNotFoundError("Image " + image_id + " does not exist!")
                
        return True
    
        if image_id in self._images:
            return self._images.get(image_id)
        
        return None
        
    def upload_image(self, image):
                    
        image_id = self.r.incr('next_image_id')
        
        pipe = self.r.pipeline()
        pipe.hmset('image:' + str(image_id), {'owner_id': str(image.owner_id), 'description': image.description, 'data': image.data, 'mime': image.mime})
        pipe.sadd('user_images:' + str(image.owner_id), image_id)
        pipe.execute()
        
        image.image_id = image_id
        
        return image
    
    def delete_image(self, image_id):
        image_id = str(image_id)
        
        image_key = 'image:' + str(image_id)
        
        users_images = self.r.keys('user_images:*')
        pipe = self.r.pipeline()
        if users_images is not None:
            for user_images in users_images:
                pipe.srem(user_images, image_id)
                    
        pipe.r.delete(image_key)
        pipe.execute()
        
        return True;
    
    def share_image(self, image_id, user_id):
        image_id = str(image_id)
        user_id = str(user_id)
        
        image_key = 'image:' + str(image_id)
        user_key = 'user:' + str(user_id)
        while 1:
            try:
                pipe = self.r.pipeline()
                pipe.watch(image_key, user_key)
                pipe.multi()
                if self.r.exists(image_key):
                    if self.r.exists(user_key):
                        pipe.sadd('user_images:' + str(user_id), str(image_id))
                        pipe.execute()
                        break
                    else:
                        raise UserNotFoundError("User " + user_id + " does not exist!")
                else:
                    raise ImageNotFoundError("Image " + image_id + " does not exist!")
            except WatchError:
                pass
                
        return True
    
    def unshare_image(self, image_id, user_id):
        image_id = str(image_id)
        user_id = str(user_id)
        
        image_key = 'image:' + str(image_id)
        user_key = 'user:' + str(user_id)
        while 1:
            try:
                pipe = self.r.pipeline()
                pipe.watch(image_key, user_key)
                pipe.multi()
                if self.r.exists(image_key):
                    if self.r.exists(user_key):
                        pipe = self.r.pipeline()
                        pipe.srem('user_images:' + str(user_id), image_id)
                        pipe.execute()
                        break
                    else:
                        raise UserNotFoundError("User " + user_id + " does not exist!")
                else:
                    raise ImageNotFoundError("Image " + image_id + " does not exist!")
            except WatchError:
                pass
                
        return True
    
