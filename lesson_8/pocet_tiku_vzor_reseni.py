# vzorove reseni pocet tiku

from microbit import i2c, sleep, button_a
from utime import ticks_ms, ticks_diff

from tridy import Senzory

class Enkoder:

    def __init__(self, jmeno):
        self.__tiky_celkem = 0
        self.__posledni_hodnota = 0
        self.__aktualni_hodnota = 0
        self.__jmeno = jmeno
        # vytvorim objekt podle tridy Senzory()
        # volam konstruktor
        self.__senzory = Senzory()

    def inicializuj(self):
        self.__posledni_hodnota = self.vycti_aktualni_hodnotu()

    def vycti_aktualni_hodnotu(self):
        senzoricka_data = self.__senzory.precti_senzory()
        self.__aktualni_hodnota = senzoricka_data[self.__jmeno]

    def pocet_tiku(self):
        # pokud je posledni merena hodnota jina nez aktualni hodnota
        # jedna se o zmenu a tedy tik!
        if self.__posledni_hodnota != self.__aktualni_hodnota:
            # tento radek znamena to same jako tiky_celkem = tiky_celkem + 1
            self.__tiky_celkem += 1
            # musime si zapamatovat aktualni hodnotu, jako tu posledne videnou
            self.__posledni_hodnota = self.__aktualni_hodnota

        return self.__tiky_celkem

if __name__ == "__main__":

    levy_enkoder = Enkoder("levy_enkoder")
    levy_enkoder.inicializuj()

    print("otacejte manualne kolem")
    print("uvidite jak tiky narustaji")
    while not button_a.was_pressed():
        levy_enkoder.vycti_aktualni_hodnotu()
        tiky = levy_enkoder.pocet_tiku()
        print("pocet_tiku", tiky)
        # toto neni spravne, vysvetleni jak cas
        # ovlivnuje enkoder a tiky je v dalsi dodatecne prezentaci
        sleep(100)


