import random
import unittest
import requests
import sys, os
import time

from io import StringIO

from unittest.mock import MagicMock, patch

from werkzeug.exceptions import Unauthorized

sys.path.extend([os.path.dirname(__file__)])
# print(os.path.dirname(__file__))
from serwerTestWWW import TestSerwerNormal, TestSerwerBadLogin, TestSerwerTimeout, TestSerwerError

try:
    from klient import Klient
except ImportError:
    from klient.klient import Klient


class KlientTestNormal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.portNormal = 5040
        cls.wwwNormal = TestSerwerNormal(port=cls.portNormal)
        cls.wwwNormal.startProcess()

        cls.portBadLogin = 5041
        cls.wwwBadLogin = TestSerwerBadLogin(port=cls.portBadLogin)
        cls.wwwBadLogin.startProcess()

        cls.portTimeout = 5042
        cls.wwwTimeout = TestSerwerTimeout(port=cls.portTimeout)
        cls.wwwTimeout.startProcess()

        cls.portError = 5043
        cls.wwwError = TestSerwerError(port=cls.portError)
        cls.wwwError.startProcess()

        # poczekajmy az serwery sie odpala
        time.sleep(1)

        cls.lista_ip = cls._lista_serwerow([cls.portNormal, cls.portBadLogin])

        # cls.klient_patch = patch('klient.klient.Klient._listaIPzPliku', return_value = cls.lista_ip)
        # cls.klient_patch.start()

        Klient._listaIPzPliku = MagicMock(return_value=cls.lista_ip[:])
        # klient miesza ta liste                           ^^^^^^^^^^^

        cls.klient = Klient()
        # cls.lista_ip.reverse()
        cls.klient._listaIP = cls.lista_ip[:]
        cls.klient.zaloguj('login','haslo')

        random.seed(10)

    def setUp(self):
        # self.klient = Klient()
        # self.klient.zaloguj('login','haslo')
        self.klient._listaIP = self.lista_ip[:]
        self.klient.aktualnyIP = self.lista_ip[0]

    @classmethod
    def tearDownClass(cls):
        cls.wwwNormal.terminate()
        cls.wwwBadLogin.terminate()
        cls.wwwTimeout.terminate()
        cls.wwwError.terminate()
        # cls.klient_patch.stop()

    @staticmethod
    def _lista_serwerow(porty):
        return ['localhost:' + str(port) for port in porty]

    def test_login_token(self):
        self.assertEqual('60febe74408dd25f11999b4a90548980', self.klient.token)

    def test_login_id(self):
        self.assertEqual(42, self.klient.id)

    def test_login_pass(self):
        'strzela do pierwszego serwera i odrazu podaje dobry login i haslo'
        k = Klient()
        k._listaIP = self.lista_ip[:]
        k.zaloguj('login', 'haslo')
        self.assertEqual('60febe74408dd25f11999b4a90548980', k.token)


    @patch('sys.stdout', new_callable=StringIO) # wywalam w piach wyjscie zeby nie syfilo
    @patch('sys.stdin', new_callable=StringIO)
    def test_login_fail_bad_login1(self, mock_stdin, mock_stdout):
        '''strzela do jednego serwera ze zlym loginem kilka (3+1) razy,
        serwer go ciagle pyta az poda dobre dane -> za 4 razem je podaje'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portNormal])

        #przy zapytaniu o login i haslo poda 3 razy niepoprawne
        mock_stdin.write('pierwszy_zly_login\npierwszy_zle_haslo\n')
        mock_stdin.write('drugi_zly_login\ndrugie_zle_haslo\n')
        mock_stdin.write('trzeci_zly_login\ntrzecie_zle_haslo\n')
        # i raz poprawne
        mock_stdin.write('login\nhaslo\n')
        mock_stdin.seek(0)

        k.zaloguj('zly_login', 'zle_haslo')

    @patch('sys.stdout', new_callable=StringIO) # w piach stdout
    def test_login_fail_timeout1(self, mock_stdout):
        '''strzela do jednego serwera, ktory robi timeout
        i nie ma juz zadnego innego'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portTimeout])
        k.zaloguj('jakikolwiek', 'jakikolwiek')
        self.assertEqual(None, k.token)

    @patch('sys.stdout', new_callable=StringIO)  # w piach stdout
    def test_login_fail_timeout2(self, mock_stdout):
        '''strzela kolejno do 3 serwerow, ktore robia timeout
        i nie ma juz zadnego innego'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portTimeout] * 3)
        k.zaloguj('jakikolwiek', 'jakikolwiek')
        self.assertEqual(None, k.token)

    @patch('sys.stdout', new_callable=StringIO)  # w piach stdout
    def test_login_fail_timeout3(self, mock_stdout):
        '''strzela kolejno do 3 serwerow, 2 robia timeout
        a ostatni loguje dobrze'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portTimeout] * 2 + [self.portNormal])
        k.zaloguj('login', 'haslo')
        self.assertEqual('60febe74408dd25f11999b4a90548980', k.token)

    @patch('sys.stdout', new_callable=StringIO)  # wywalam w piach wyjscie zeby nie syfilo
    @patch('sys.stdin', new_callable=StringIO)
    def test_login_fail_timeout4(self, mock_stdin, mock_stdout):
        '''strzela kolejno do 3 serwerow, 2 pierwsze robia timeout
        a ostatni 2 razy zle dane logowania i potem loguje dobrze'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portTimeout] * 2 + [self.portNormal])
        mock_stdin.write('pierwszy_zly_login\npierwszy_zle_haslo\n')
        mock_stdin.write('login\nhaslo\n')
        mock_stdin.seek(0)
        k.zaloguj('zly_login', 'zle_haslo')
        self.assertEqual('60febe74408dd25f11999b4a90548980', k.token)

    def test_wykonania_zadania_sukces(self):
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portNormal])
        k.zaloguj('login', 'haslo')
        post_data = {'token': k.token, 'test_text': 'ala_ma_kota'}
        sciezka_postfix = '/test_zadanie'
        def handler(request):
            self.temp = request.text
        k._wykonaj_zadanie(sciezka_postfix=sciezka_postfix,
                           data=post_data,
                           handler=handler,
                           typ='POST')
        self.assertEqual('ala_ma_kota', self.temp)

    def test_wykonania_zadania_sukces2(self):
        '''strzela do 1 i timeout -> ponawia do nastepnego
        i udaje mu sie'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portTimeout, self.portNormal])
        # k.zaloguj('login', 'haslo')
        post_data = {'token': k.token, 'test_text': 'ala_ma_kota'}
        sciezka_postfix = '/test_zadanie'

        def handler(request):
            self.temp = request.text

        k._wykonaj_zadanie(sciezka_postfix=sciezka_postfix,
                           data=post_data,
                           handler=handler,
                           typ='POST')
        self.assertEqual('ala_ma_kota', self.temp)

    def test_wykonania_zadania_sukces3(self):
        '''strzela do 1 i error -> ponawia do nastepnego
        i udaje mu sie'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portError, self.portNormal])
        # k.zaloguj('login', 'haslo')
        post_data = {'token': k.token, 'test_text': 'ala_ma_kota'}
        sciezka_postfix = '/test_zadanie'

        def handler(request):
            self.temp = request.text

        k._wykonaj_zadanie(sciezka_postfix=sciezka_postfix,
                           data=post_data,
                           handler=handler,
                           typ='POST')
        self.assertEqual('ala_ma_kota', self.temp)

    def test_wykonania_zadania_fail_timeout(self):
        '''strzela do 2 z timeoutem'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portTimeout]*2)
        post_data = {'token': k.token, 'test_text': 'ala_ma_kota'}
        sciezka_postfix = '/test_zadanie'

        def handler(request):
            self.temp = request.text

        # k._wykonaj_zadanie(sciezka_postfix=sciezka_postfix,
        #                    post_data=post_data,
        #                    handler=handler)

        self.assertRaises(Exception, k._wykonaj_zadanie,
                                     sciezka_postfix=sciezka_postfix,
                                     data=post_data,
                                     handler=handler,
                                     typ='POST')

    def test_wykonania_zadania_fail_bad_token(self):
        '''strzela do 2 z blednym tokenem,
        ale juz pierwszy mu mowi zeby sie zalogowal jeszcze raz
        i konczy obsluge'''
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portBadLogin]*2)
        post_data = {'token': k.token, 'test_text': 'ala_ma_kota'}
        sciezka_postfix = '/test_zadanie'

        def handler(request):
            self.temp = request.text

        # k._wykonaj_zadanie(sciezka_postfix=sciezka_postfix,
        #                    post_data=post_data,
        #                    handler=handler)

        self.assertRaises(Unauthorized, k._wykonaj_zadanie,
                          sciezka_postfix=sciezka_postfix,
                          data=post_data,
                          handler=handler,
                          typ='POST')

    def test_delete_method(self):
        # data={'token': "fdasfdsa"}
        data={'image_id': 69, 'token': '60febe74408dd25f11999b4a90548980', 'user_id': 42}
        adres = 'http://localhost:' + str(self.portNormal) + '/32/images/23'
        response = requests.delete(adres, data=data)
        print(response)

    def test_usun_obrazek_pass(self):
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portNormal])
        k.zaloguj('login', 'haslo')
        sukces = k.usun_moj_obrazek(obrazek_id=69)
        self.assertEqual(True, sukces)

    def test_usun_obrazek_fail(self):
        k = Klient()
        k._listaIP = self._lista_serwerow([self.portError])
        k.zaloguj('login', 'haslo')
        sukces = k.usun_moj_obrazek(obrazek_id=69)
        self.assertEqual(False, sukces)

    @patch('sys.stdout',new_callable=StringIO)
    def test_mock_stdout(self, mock_stdout):
        print("ala", end="")
        self.assertEqual('ala', mock_stdout.getvalue())

    @patch('sys.stdin', new_callable=StringIO)
    def test_mock_stdin(self, mock_stdin):
        mock_stdin.write('ala\n')
        mock_stdin.seek(0)
        s = input() #robi normalnie sys.stdin.readline()
        self.assertEqual('ala\n', mock_stdin.getvalue())


    def test_www1_response(self):
        response = requests.get('http://localhost:' + str(self.portNormal) + '/hello')
        # print(self.port1)
        self.assertEqual(response.text, 'hello')

    def test_www2_response(self):
        response = requests.get('http://localhost:' + str(self.portBadLogin) + '/hello')
        self.assertEqual(response.text, 'hello')

    def test_www3_response(self):
        response = requests.get('http://localhost:' + str(self.portTimeout) + '/hello')
        self.assertEqual(response.text, 'hello')

    def test_mockup_listaIP(self):
        self.assertEqual(self.klient._listaIP, self.lista_ip)

    def test_klient_exist(self):
        self.assertEqual(self.klient.hello(), 'hello_from_klient')

    def test_random_seed(self):
        random.seed(10)
        self.assertEqual(random.randint(0, 100), 73)
        self.assertEqual(random.randint(0, 100), 4)
        self.assertEqual(random.randint(0, 100), 54)



# class KlientLoginTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.token = '60febe74408dd25f11999b4a90548980'
#
#
#     @classmethod
#     def tearDownClass(cls):
#         pass
#
#     def test_a(self):
#         pass

    # def test_login_fail(self):
    #     k = Klient()
    #     with patch('klient.klient.Klient._listaIPzPliku', return_value = 5):
    #         self.assertEqual(self.klient._listaIPzPliku(), 5)
    #     with patch('serwerWWW.TestSerwerKlient1._login', side_effect= lambda a: 5):
    #         print(self.www1._login("sdffasd"))
    #         self.www2
    #         k.zaloguj('login', 'haslo')
    #         self.assertEqual(k.token, 'ala')

# class KlientTestBadLogin(unittest.TestCase):
#     pass

# if __name__ == '__main__':
#     unittest.main()

