from microbit import pin14, pin15
from utime import ticks_us, ticks_diff

from konstanty import Konstanty
from senzory import Senzory

class Enkoder:

    def __init__(self, jmeno, perioda_rychlosti=1, nova_verze=True, debug=False):
        self.__jmeno = jmeno
        self.__perioda_rychlosti = perioda_rychlosti*1000000  # na us

        self.__nova_verze = nova_verze
        self.__tiky = 0
        self.__posledni_hodnota = -1
        self.__tiky_na_otocku = 40
        self.__nova_verze = nova_verze
        self.__DEBUG = debug
        self.__inicializovano = False
        self.__cas_posledni_rychlosti = ticks_us()
        self.__radiany_za_sekundu = 0

        if not self.__nova_verze:
            self.__senzory = Senzory(False, debug)

    def inicializuj(self):
        self.__posledni_hodnota = self.__aktualni_hodnota()
        self.__inicializovano = True

    def __aktualni_hodnota(self):
        if self.__nova_verze:
            if self.__jmeno == Konstanty.PR_ENKODER:
                return pin15.read_digital()
            elif self.__jmeno == Konstanty.LV_ENKODER:
                return pin14.read_digital()
            else:
                return -2
        else:
            senzoricka_data = self.__senzory.precti_senzory()

            if self.__jmeno == Konstanty.LV_ENKODER or self.__jmeno == Konstanty.PR_ENKODER:
                return int(senzoricka_data[self.__jmeno])
            else:
                return -2

    # drive se tato metoda jmenovala pocet_tiku
    def aktualizuj_se(self):
        if self.__DEBUG:
            print("v aktualizuj", self.__tiky)
        if self.__posledni_hodnota == -1:
            if self.__DEBUG:
                print("posledni_hodnota neni nastavena", self.__posledni_hodnota)
            return -1

        aktualni_enkoder = self.__aktualni_hodnota()
        if self.__DEBUG:
            print("aktualni enkoder", aktualni_enkoder)

        if aktualni_enkoder >= 0:  # nenastaly zadne chyby
            if self.__posledni_hodnota != aktualni_enkoder:
                self.__posledni_hodnota = aktualni_enkoder
                self.__tiky += 1
        else:
            return aktualni_enkoder

        return 0

    def __us_na_s(self, cas):
        return cas/1000000

    def vypocti_rychlost(self):
        cas_ted = ticks_us()
        interval_us = ticks_diff(cas_ted, self.__cas_posledni_rychlosti)
        if interval_us >= self.__perioda_rychlosti:
            interval_s = self.__us_na_s(interval_us)
            otacky = self.__tiky/self.__tiky_na_otocku
            radiany = otacky * 2 * Konstanty.PI
            self.__radiany_za_sekundu = radiany / interval_s
            self.__tiky = 0
            self.__cas_posledni_rychlosti = cas_ted

        return self.__radiany_za_sekundu
