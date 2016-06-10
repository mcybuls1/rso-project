import unittest

import time
from unittest.mock import MagicMock

import requests
from requests.auth import HTTPBasicAuth

from source.serwer2.serwer import Serwer
from source.klient.klient import Klient, Klient2
from source.serwer2.testy import DB_API_MOCK
from source.baza.db import DataBaseSerwer


class Test_klient_serwer_MOCK_db(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serwer_port = 5987
        Klient2._listaIPzPliku = MagicMock(return_value=['http://0.0.0.0:'+str(cls.serwer_port)])
        cls.klient = Klient2()

        cls.serwer = Serwer(port=cls.serwer_port)
        cls.serwer.db_api = DB_API_MOCK()

        cls.serwer.startProcess()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.serwer.terminate()

    def test_login(self):
        self.assertTrue(self.klient.zaloguj(login='przemek', haslo='przemekhaslo'))

    def test_login_fail_bad_data(self):
        self.assertFalse(self.klient.zaloguj(login='dfsa', haslo='przemekhaslo'))

    def test_get_photo(self):
        k = Klient2()
        k.zaloguj(login='przemek', haslo='przemekhaslo')
        print(k._daj_zdjecie('hashhash'))

    def test_add_photo(self):
        k = Klient2()
        k.zaloguj(login='przemek', haslo='przemekhaslo')
        print(k.wrzuc_zdjecie('foty/pies.jpg'))


class Test_klient_serwer_DB_ip_na_sztywno(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serwer_port = 6789
        Klient2._listaIPzPliku = MagicMock(return_value=['http://0.0.0.0:' + str(cls.serwer_port)])

        cls.baza_port = 6787
        cls.baza = DataBaseSerwer(cls.baza_port)

        cls.serwer = Serwer(port=cls.serwer_port)
        cls.serwer.db_api.port = cls.baza_port


        cls.klient = Klient2()

        cls.baza.startProcess()
        cls.serwer.startProcess()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.serwer.terminate()
        cls.baza.terminate()

    def test_zaloguj(self):
        k = Klient2()
        self.assertTrue(k.zaloguj('John', 'pass1'))

    def test_wrzuc_zdjecie(self):
        k = Klient2()
        self.assertTrue(k.zaloguj('John', 'pass1'))
        self.assertEqual(200,k.wrzuc_zdjecie('foty/pies.jpg'))

    def test_daj_zdjecie(self):
        k = Klient2()
        self.assertTrue(k.zaloguj('John', 'pass1'))
        k._daj_zdjecie(photo_hash='7bf865229610d143752b238790c7808b')

    def test_sledz_znajomego(self, znajomy):
        k = Klient2()

