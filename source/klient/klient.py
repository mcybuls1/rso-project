import requests, random

class Klient(object):
    def __init__(self, plik_konfiguacyjny):
        self.plik_konf = plik_konfiguacyjny
        self.token = None
        self.timeout = None
        self.listaIP = None

        self._wczytajlisteIP()
        self.aktualnyIP = self.listaIP[0]


    def _wczytajlisteIP(self):
        # parsowanie pliku
        self.listaIP = ['127.0.0.1:5000', '127.0.0.1:5001']

    def _wylosujIP(self):
        kopiaListaIP = self.listaIP[:]
        kopiaListaIP.remove(self.aktualnyIP)
        self.aktualnyIP = random.choice(kopiaListaIP)


    def zaloguj(self, login, haslo):
        requests.post('zaloguj', data={'login': login, 'haslo': haslo})


    def wyslijPlik(self):
        pass

    def pobierzSwojPlik(self, nazwa_plik):
        pass

    def pobierzPlikZnajomego(self, znajomy, nazwa_pliku):
        pass

    def listaMoichPlikow(self):
        pass

    def listaZnajomych(self):
        pass

    def listaPlikowZnajomego(self, znajomy):
        pass



if __name__ == '__main__':
    klient = Klient("sciezka_plik_konfiguracyjny")
