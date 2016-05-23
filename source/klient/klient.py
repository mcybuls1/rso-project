import requests

class Klient(object):
    def __init__(self, plik_konfiguacyjny):
        self.plik_konf = plik_konfiguacyjny
        self.token = None
        self.timeout = None
        self.listaIP = None

        self._wczytajlistaIP()

    def _wczytajlistaIP(self):
        # parsowanie pliku
        self.listaIP = ['127.0.0.1:5000', '127.0.0.1:5001']

    def zaloguj(self):
        pass

    def wyslijPlik(self):
        pass

    def pobierzSwojPlik(self, plik):
        pass

    def pobierzPlikZnajomego(self, znajomy, plik):
        pass

    def listaMoichPlikow(self):
        pass

    def listaZnajomych(self):
        pass

    def listaPlikowZnajomego(self, znajomy):
        pass



if __name__ == '__main__':
    klient = Klient("sciezka_plik_konfiguracyjny")

    klient
