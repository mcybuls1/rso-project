import requests, random
from flask import abort
from werkzeug.exceptions import Unauthorized

class Klient(object):
    def __init__(self, plik_konfiguacyjny=None):
        self.plik_konf = plik_konfiguacyjny
        self.token = None
        self.timeout = 1
        self._listaIP = None

        self._wczytajlisteIP()
        self._wylosujIP_mieszajac_liste()
        # self.aktualnyIP = random.choice(self._listaIP)


    def _wczytajlisteIP(self):
        self._listaIP = self._listaIPzPliku()

    # def _listaIPzPliku(self):
    #     #parser pliku
        # pass

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
        adres = 'http://' + self.aktualnyIP + '/login'
        response = requests.post(adres, data={'login': login, 'haslo': haslo}, timeout=self.timeout)
        if self._pozytywny_status(response.status_code):
            self.token = response.text
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
                raise Exception('Nie ma żadnego działającego węzła')
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

    # def wyslijPlik(self):
    #     pass
    #
    # def pobierzSwojPlik(self, nazwa_plik):
    #     pass
    #
    # def pobierzPlikZnajomego(self, znajomy, nazwa_pliku):
    #     pass
    #
    # def listaMoichPlikow(self):
    #     pass
    #
    # def listaZnajomych(self):
    #     pass
    #
    # def listaPlikowZnajomego(self, znajomy):
    #     pass

    def hello(self):
        return "hello_from_klient"


# if __name__ == '__main__':
#     klient = Klient("sciezka_plik_konfiguracyjny")
