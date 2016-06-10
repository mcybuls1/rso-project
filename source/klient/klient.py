import io

import requests, random
from flask import abort
from requests.auth import HTTPBasicAuth
from werkzeug.exceptions import Unauthorized
from flask.helpers import send_file

class Klient(object):
    def __init__(self, plik_konfiguacyjny=None):
        self.plik_konf = plik_konfiguacyjny
        self.token = None #nieuzywane chyba juz, ale niech lezy do testow
        self.login = None
        self.haslo = None
        self.auth = None
        self.timeout = 0.3
        self._listaIP = None
        self.id = None

        self._wczytajlisteIP()
        self._wylosujIP_mieszajac_liste()
        # self.aktualnyIP = random.choice(self._listaIP)


    def _wczytajlisteIP(self):
        self._listaIP = self._listaIPzPliku()

    def _listaIPzPliku(self):
        #parser pliku
        # return ['127.0.0.1:5000' '127.0.0.1:5001']
        pass

    # def _wylosujIP(self):
    #     'losuje ip eliminujac z losowania akutalne ip'
    #     kopiaListaIP = self._listaIP[:]
    #     kopiaListaIP.remove(self.aktualnyIP)
    #     self.aktualnyIP = random.choice(kopiaListaIP)

    def _wylosujIP_mieszajac_liste(self):
        random.shuffle(self._listaIP)
        self.aktualnyIP = self._listaIP[0]


    def _pozytywny_status(self, status_code):
        if 200 <= status_code < 300 :
            return True
        else:
            return False

    def _zadanie_logowania(self, login, haslo):
        adres = 'http://' + self.aktualnyIP + '/api/login'
        self.auth = HTTPBasicAuth(username=login, password=haslo)
        # response = requests.post(adres, data={'username': login, 'password': haslo}, timeout=self.timeout,
        #                          auth=self.auth)
        response = requests.get(adres, timeout=self.timeout, auth=self.auth)

        if self._pozytywny_status(response.status_code):
            print('ZALOGOWANO')
            # self.token = response.json()['api_key']
            self.login = login
            self.haslo = haslo
            self.auth = HTTPBasicAuth(username=login, password=haslo)
            # self.id = int(response.json()['id'])
            return True, response.status_code
        else:
            self.token = None
            return False, response.status_code
            # abort(response.status_code)

    def zaloguj(self, login, haslo):
        l = login
        h = haslo
        try:
            for ip in self._listaIP:
                self.aktualnyIP = ip
                try:
                    try:
                        sukces, status_code = self._zadanie_logowania(l, h)
                        if sukces:
                            break
                        else:
                            abort(status_code)
                    except Unauthorized as e:
                        print(e)
                        try:
                            self._reloguj_do_skutku()
                        except StopIteration:
                            # zalogowano
                            break
                        # except Exception as e:
                        #     print(e, 'Ponawiam próbę logowania do innego serwera')
                        #     continue
                except Exception as e:
                    print(e, 'Ponawiam próbę logowania do innego serwera')
                    continue

            # gdy koniec listy wezlow
            if self.token == None:
                # nie zalogowano
                # raise Exception('Nie ma żadnego działającego węzła')
                pass
            else:
                print('zalogowano')
                # pass
        except Exception as e:
            print('nie zalogowano')
            self.token = None
            print(str(e) + ", kończę działanie programu")
            # raise e

    def _reloguj_do_skutku(self):
        print('Błędny login lub hasło, podaj nowe')
        l = input('login: ')
        h = input('haslo: ')
        try:
            self._zadanie_relogowania_do_skutku(l, h)
        except StopIteration:
            # zalogowano
            raise StopIteration
        # except Exception as e:
        #     print(e, 'serwer zerwal polaczenie lub nie odpowiada')
        #     raise e

    def _zadanie_relogowania_do_skutku(self, l, h):
        s = True
        while s:
            try:
                s, status_code = self._zadanie_logowania(l, h)
                if s == True:
                    #sukces, zalogowano
                    raise StopIteration
                else:
                    s = True  # kontynuuje petle
                    abort(status_code)
            except Unauthorized as e:
                print(e, 'Błędny login lub hasło, podaj nowe')
                l = input('login: ')
                h = input('haslo: ')

    def _wykonaj_zadanie(self, sciezka_postfix, handler, data=None, params=None, typ='POST'):
        # handler(*args_handler)
        # adres = 'http://' + adresIP + sciezka_postfix
        # sukces, response = self._post_wrapper(sciezka_postfix=sciezka_postfix,
        #                                       post_data=post_data)
        sukces = False
        try:
            for ip in self._listaIP:
                self.aktualnyIP = ip
                try:
                    sukces, response = self._req_wrapper(sciezka_postfix=sciezka_postfix,
                                                  data=data,
                                                  params=params,
                                                  typ=typ)
                    if sukces:
                        handler(response)
                        break
                    else:
                        abort(response.status_code)
                except Unauthorized as e:
                    print(e, ' żądanie zasobu, który wymaga uwierzytelnienia')
                    raise e
                except Exception as e:
                    print('Ponawiam żądanie do innego serwera')
                    continue
            if sukces:
                pass # wykonano poprawnie zadanie
            else:
                raise Exception('Nie ma żadnego działającego węzła')
        except Unauthorized as e:
            print('spróbuj się zalogować raz jeszcze')
            raise e
        except Exception as e:
            print(e, ', żaden serwer nie potrafi obsłużyć żądania')
            raise e


    def _req_wrapper(self, sciezka_postfix, data=None, params=None, typ="POST"):
        """
        :rtype: bool, response
        """
        url = 'http://' + self.aktualnyIP + sciezka_postfix
        if typ == 'DELETE':
            response = requests.delete(url, data=data, auth=self.auth)
        elif typ == 'GET':
            response = requests.get(url, params=params, timeout=self.timeout, auth=self.auth)
        else : #typ == 'POST'
            response = requests.post(url, data=data, timeout=self.timeout, auth=self.auth)
        if self._pozytywny_status(response.status_code):
            return True, response
        else:
            return False, response

    def usun_moj_obrazek(self, obrazek_id: int) -> bool:
        def handler(response):
            print('usunieto obrazek', obrazek_id, 'response.status.code:',response.status_code)

        data={'token': self.token, 'user_id': self.id, 'image_id': obrazek_id}
        sciezka_postfix = '/' + str(self.id) + '/' + 'images' + '/' + str(obrazek_id)
        try:
            self._wykonaj_zadanie(sciezka_postfix=sciezka_postfix,
                                  data=data,
                                  handler=handler,
                                  typ='DELETE')
        except Exception as e:
            print(e)
            return False
        return True

    def hello(self):
        return "hello_from_klient"

    def wyslij_plik(self, file_path):
        def handler(response):
            print(response)

        self._wykonaj_zadanie('/api/add_photo', handler=handler)

# if __name__ == '__main__':
#     klient = Klient("sciezka_plik_konfiguracyjny")

class Klient2(object):
    def __init__(self):
        self.auth = None
        self.timeout = 0.3
        self._listaIP = None

        self._wczytajlisteIP()
        self._wylosujIP_mieszajac_liste()
        pass

    def _wczytajlisteIP(self):
        self._listaIP = self._listaIPzPliku()

    def _wylosujIP_mieszajac_liste(self):
        random.shuffle(self._listaIP)
        self.aktualnyIP = self._listaIP[0]

    def _listaIPzPliku(self):
        # TODO PARSER PLIKU
        pass

    def zaloguj(self, login, haslo):
        self.auth = HTTPBasicAuth(username=login, password=haslo)
        r = requests.get(url=self._listaIP[0] + '/api/login', auth=self.auth)
        if r.status_code == 200:
            print('ZALOGOWANO')
            return True
        if r.status_code == 401:
            print('BLEDNE DANE LOGOWANIA')
            return False

    def sledz_znajomego(self, znajomy):
        data = {'friend': znajomy}
        r = requests.post(url=self._listaIP[0] + '/api/follow_friend',
                          data=data,
                          auth=self.auth)
        if r.status_code == 404:
            print('NIE MA TAKIEGO UZYTKOWNIKA')
            # TODO

    def _daj_zdjecie(self, photo_hash, rozszerzenie='.jpg'):
        data = {'photo_hash': photo_hash}
        r = requests.post(url=self._listaIP[0] + '/api/get_photo', verify=False,
                          data=data,
                          auth=self.auth)
        with open(data['photo_hash']+'POBRANE'+rozszerzenie, 'wb') as f:
            f.write(r.content)
        return "ZAPISANO ZDJECIE"

    def wrzuc_zdjecie(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            # file_stream = io.BytesIO(f.read())
            r = requests.post(url=self._listaIP[0]+'/api/add_photo', files=files,
                              auth=self.auth)
            return r.status_code





