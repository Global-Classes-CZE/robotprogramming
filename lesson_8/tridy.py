from microbit import i2c
from utime import ticks_ms, ticks_diff

class Enkoder:

    def __init__(self, jmeno, nova_verze=True):
        self.jmeno = jmeno
        self.nova_verze = nova_verze
        self.__tiky = 0
        self.__posledni_hodnota = -1
        self.tiky_na_otocku = 40
        self.DEBUG = False

    def inicializuj(self):
        self.__posledni_hodnota = self.aktualni_hodnota()
        i2c.init(400000)

    def aktualni_hodnota(self):
        if self.nova_verze:
            # TODO
            print("naimplementuj")
        else:
            senzoricka_data = self.__precti_senzory()
            if self.jmeno == "pravy_enkoder" or self.jmeno == "levy_enkoder":
                return int(senzoricka_data[self.jmeno])
            else:
                print(self.jmeno, "neni podporovane.")
                print("Podporovana jmena jsou \"levy_enkoder\" nebo \"pravy_enkoder\"")
                return -1

    def pocet_tiku(self):
        if self.__posledni_hodnota == -1:
            print("Musite nejdrive zavolat metodu inicializuj")
            return -1

        aktualni_enkoder = self.aktualni_hodnota()
        if self.DEBUG:
            print("aktualni enkoder", aktualni_enkoder)

        if aktualni_enkoder != -1:
            if self.__posledni_hodnota != aktualni_enkoder:
                self.__posledni_hodnota = aktualni_enkoder
                self.__tiky += 1

        return self.__tiky

    def vynuluj_tiky(self):
        self.__tiky = 0

    def __byte_na_bity(self, data_bytes):
        data_int = int.from_bytes(data_bytes, "big")
        bit_pole_string = bin(data_int)

        if self.DEBUG:
            print("data_int", data_int)
            print("bit pole", bit_pole_string)

        return bit_pole_string

    def __precti_senzory(self):
        surova_data_byte = i2c.read(0x38, 1)
        if self.DEBUG:
            print("surova data", surova_data_byte)

        # chceme prevest vycteny byte na bity, abychom se dostali k informaci ze senzoru
        bitove_pole = self.__byte_na_bity(surova_data_byte)

        senzoricka_data = {}  # vytvorim si prazdny slovnik

        senzoricka_data["levy_enkoder"] = bitove_pole[9]
        senzoricka_data["pravy_enkoder"] = bitove_pole[8]
        senzoricka_data["levy_sledovac_cary"] = bitove_pole[7]
        senzoricka_data["prostredni_sledovac_cary"] = bitove_pole[6]
        senzoricka_data["pravy_sledovac_cary"] = bitove_pole[5]
        senzoricka_data["levy_IR"] = bitove_pole[4]
        senzoricka_data["pravy_IR"] = bitove_pole[3]
        # pripominka - my mame jen 7 senzoru, ale vycetli jsme 1 byte,
        # tzn 8. bit na pozici [2] je nejaky "duch", o ktery nam tu nejde
        # pozice [1] je pismeno "b", o tom nam taky nejde
        # pozice [0] je vzdy 0, taky nam o to nejde

        return senzoricka_data

class Motor:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.enkoder = Enkoder(jmeno + "_enkoder", False)
        self.tiky_na_otocku = self.enkoder.tiky_na_otocku
        self.otacky_za_cas = 0

    def jed_PWM(self, smer, PWM):
        self.cas_zacatku = ticks_ms()
        self.enkoder.inicializuj()
        if(self.jmeno == "levy"):
            if(smer=="dopredu"):
                i2c.write(0x70, b"\x05" + bytes([PWM]))
                return 0
        return -1

    def rychlost(self):

        tiky = self.enkoder.pocet_tiku()

        interval_ms = ticks_diff(ticks_ms(), self.cas_zacatku)
        if interval_ms >= 1000:
            interval_s = interval_ms/1000
            otacky = tiky/self.tiky_na_otocku
            self.otacky_za_cas = otacky / interval_s
            self.enkoder.vynuluj_tiky()
            self.cas_zacatku = ticks_ms()

        return self.otacky_za_cas
