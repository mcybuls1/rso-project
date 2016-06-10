import io
import unittest
import requests
import time

from flask import jsonify, abort, make_response
from requests.auth import HTTPBasicAuth
from source.serwer2.serwer import Serwer
from source.serwer2.serwer import DB_API

class ResponseMock(object):
    def __init__(self, json_slownik, status_code):
        self.status_code = status_code
        self.json = lambda : json_slownik
    def json(self):
        pass

class DB_API_MOCK(DB_API):
    def __init__(self):
        super().__init__()
        self.uzytkownicy = {
            'a533085fa15e31769d1f4bcee3470492': {
                'name': 'przemek',
                'password': 'przemekhaslo',
                'images': ['przemek_image_hash1', 'przemek_image_hash2'],
                'friends': ['karolina']
            },
            'karolina_hash': {
                'user': 'karolina',
                'password': 'karolinahaslo',
                'images': ['karolina_image_hash1, karolina_image_hash2'],
                'friends': ['przemek', 'michal']
            },
            '06b2af75179fb94be097af182a442a4a': {
                'user': 'michal',
                'password': 'michalhaslo',
                'images': ['michal_image_hash1, michal_image_hash2'],
                'friends': ['przemek', 'karolina']
            }
        }

    def get_user(self, user_hash):
        if user_hash in self.uzytkownicy.keys():
            ret = ResponseMock(json_slownik= self.uzytkownicy[user_hash], status_code=200)
            # ret.json = lambda : self.uzytkownicy[user_hash]
            # return jsonify(self.uzytkownicy[user_hash])
            # return make_response(jsonify(self.uzytkownicy[user_hash]), 200)
            # return jsonify({'user': request.json}), 200
            return ret
        else:
            return ResponseMock(json_slownik={'error':'ni ma takiego hashu uzytkownika'},
                                status_code=404)

    def put_user(self, username, dict):
        self.uzytkownicy[username] = dict

    def get_photo(self, hash):
        r = requests.get('https://upload.wikimedia.org/wikipedia/commons/0/09/Mieszaniec_czarny_978.jpg',
                         stream=True)
        ret = io.BytesIO(r.raw.read())
        return ret

    def put_photo(self, hash, file):
        file.save('foty/'+hash+'.jpg')
        return ResponseMock(json_slownik={'status': 'ok'}, status_code=200)



class Test_Serwer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.www = Serwer(port=5678)
        cls.www.db_api = DB_API_MOCK()
        cls.base_adress = 'http://0.0.0.0:5678/api'
        cls.www.startProcess()
        # przemek hash
        cls.auth_pass = HTTPBasicAuth(username='przemek', password='przemekhaslo')
        cls.auth_fail = HTTPBasicAuth(username='przemek', password='zlehaslo')
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.www.terminate()

    def test_login_pass(self):
        r = requests.get(url=self.base_adress + '/login', auth=self.auth_pass)
        self.assertEqual(200, r.status_code)
        self.assertEqual('ok', r.json()['status'])

    def test_login_fail(self):
        r = requests.get(url=self.base_adress + '/login', auth=self.auth_fail)
        self.assertEqual(401, r.status_code)

    # @unittest.skip('.')
    def test_follow_friend_pass(self):
        data = {'friend': 'michal'}
        r = requests.post(url= self.base_adress + '/follow_friend', data=data,
                          auth=self.auth_pass)
        self.assertEqual(200, r.status_code)
        self.assertEqual({'status': 'ok'}, r.json())

    # @unittest.skip('.')
    def test_follow_friend_fail(self):
        data = {'friend': 'nie_ma_takiego_hasha'}
        r = requests.post(url=self.base_adress + '/follow_friend', data=data,
                          auth=self.auth_pass)
        self.assertEqual(404, r.status_code)
        self.assertEqual({'error': 'no such user'}, r.json())

    def test_get_images_list_pass(self):
        data = {'friend': 'michal'}
        r = requests.post(url=self.base_adress + '/get_photos_list', data=data,
                          auth=self.auth_pass)
        self.assertEqual(200, r.status_code)
        self.assertEqual(['michal_image_hash1, michal_image_hash2'], r.json()['images'])

    def test_get_photo(self):
        data = {'photo_hash': 'michal_image_hash1'}
        r = requests.post(url=self.base_adress + '/get_photo', data=data,
                          auth=self.auth_pass)



        # self.assertEqual(200, r.status_code)
        # self.assertEqual(['michal_image_hash1, michal_image_hash2'], r.json()['images'])
