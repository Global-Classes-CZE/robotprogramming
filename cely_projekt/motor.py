from microbit import i2c

import Konstanty

class Motor:
    def __init__(self, jmeno, prumer_kola):
        if jmeno == Konstanty.LEVY:
            self.__kanal_dopredu = b"\x05"
            self.__kanal_dozadu = b"\x04"
        elif jmeno == Konstanty.PRAVY:
            self.__kanal_dopredu = b"\x03"
            self.__kanal_dozadu = b"\x02"
        else:
            raise AttributeError("spatne jmeno motoru, musi byt \"levy\" a nebo \"pravy\", zadane jmeno je" + str(jmeno))

        self.__jmeno = jmeno
        self.__prumer_kola = prumer_kola
        self.__enkoder = Enkoder(jmeno + "_enkoder")
        self.__smer = Konstanty.NEDEFINOVANO
        self.__inicializovano = False
        self.__rychlost_byla_zadana = False

    def inicializuj(self):
         self.enkoder.inicializuj()
         # probud cip motoru
        i2c.write(0x70, b"\x00\x01")
        i2c.write(0x70, b"\xE8\xAA")
        self.__inicializovano = True

    def kalibrace(self):
        """
        Zmeri zavislost mezi PWM a uhlovou rychlosti a prolozi ji lomenou primkou
        """
        if not self.__inicializovano:
            return -1

        # TODO naimplementuj

        # TODO jine parametery!! tyhle jsou pro uhlovou rcyhlost v ot/s,
        # ja potrebuji rad/s

        self.__limity = [0.675, 2.15]
        self.__primky_par_a = [94.915]
        self.__primky_par_b = [35.932]
        return 0

    def jed_doprednou_rychlosti(self, v: float):
        """
        Rozjede motor pozadovanou doprednou rychlosti
        """
        if not self.__inicializovano:
            return -1

        self.__pozadovana_uhlova_r_kola = dopredna_na_uhlovou(v)
        self.__rychlost_byla_zadana = True

        # pouziji funkci abs pro vypocteni absolutni hodnoty
        # PWM je vzdy pozitivni
        # znamenko uhlove rychlosti ovlivni smer
        prvni_PWM = uhlova_na_PWM(abs(self.__pozadovana_uhlova_r_kola))

        if self.__pozadovana_uhlova_r_kola > 0:
            self.__smer = Konstanty.DOPREDU
        elif self.__pozadovana_uhlova_r_kola < 0:
            self.__smer = Konstanty.DOZADU
        else: # = 0
            self.__smer == Konstanty.NEDEFINOVANO

        return self.__jed_PWM(prvni_PWM)


    #lekce 8, slidy 8 - 11
    def __dopredna_na_uhlovou(self, v: float):
        """
        Prepocita doprednou rychlost kola na uhlovou
        """
        return v/self.__prumer_kola/2

    def __uhlova_na_PWM(self, uhlova):
        """
        Prepocte uhlovou rychlost na PWM s vyuzitim dat z kalibrace
        """

        a, b = self.__najdi_spravne_parametery(uhlova)
        return int(a*uhlova + b)

    def __najdi_spravne_parametery(self, uhlova):
        # TODO
        return a[0], b[0]

    # DU 5 pokrocily/DU 7 zacatecnici
    # jed(motor, smer, rychlost)
    def __jed_PWM(self, PWM):
        je_vse_ok = -2
        if self.__smer == Konstanty.DOPREDU:
            je_vse_ok  = self.__nastav_PWM_kanaly(self.__kanal_dopredu, self.__kanal_dozadu, PWM)
        elif self.__smer == Konstanty.DOZADU:
            je_vse_ok  = self.__nastav_PWM_kanaly(self.__kanal_dozadu, self.__kanal_dopredu, PWM)
        elif self.__smer == Konstanty.NEDEFINOVANO:
            if PWM == 0:
                je_vse_ok = self.__nastav_PWM_kanaly(self.__kanal_dozadu, self.__kanal_dopredu, PWM)
            else:
                je_vse_ok = -1
        else:
            je_vse_ok = -1

        return je_vse_ok

    def __nastav_PWM_kanaly(self, kanal_on, kanal_off, PWM):
        # TODO zkontroluj, ze motor byl inicializovan
        i2c.write(0x70, kanal_off + bytes([0]))
        i2c.write(0x70, kanal_on + bytes([PWM]))
        self.__PWM = PWM
        return 0

    # ukazka v pridanem materialu k hodine 8
    def reguluj_otacky(self):

        if not self.__inicializovano:
            return -1

        if not self.__rychlost_byla_zadana:
            return -2

        P = 30 # TODO tohle bude jine, protoze otacky budou v radianech!

        aktualni_rychlost = self.enkoder.vypocti_rychlost()
        # aktualni_rychlost bude vzdy pozitivni
        # musim tedy kombinovat se smerem, kterym se pohybuji
        if self.__pozadovana_uhlova_r_kola < 0:
            aktualni_rychlost *= -1

        error = self.__pozadovana_uhlova_r_kola - aktualni_rychlost
        akcni_zasah = P*error
        return self.__zmen_PWM_o(akcni_zasah)

    def __zmen_PWM_o(self, akcni_zasah):
        # error a tim padem i akcni_zasah muze byt jak pozitivni tak negativni, nezavisle na smeru
        # priklad, pozadovana = 5, aktualni = 2
        # smer = dopredu a error > 0 => musim zrychlit
        # priklad, pozadovana 5, aktualni 10
        # smer = dopredu a error < 0 => musim zpomalit
        # priklad, pozadovana -5, aktualni -2
        # smer = dozadu a error < 0 => musim zrychlist
        # priklad, pozadovana -5, aktualni -7
        # smer= dozadu a error>0 => musim zpomalit

        akcni_zasah = int(akcni_zasah) #PWM je v celych cislech

        if self.__smer == Konstanty.DOZADU:
            # prohod logiku aby pozitivni akcni_zasah u jizdy dozadu
            # take znamenal zrychli a ne zpomal, viz priklad nahore
            akcni_zasah *= -1

        nove_PWM = self.__PWM + akcni_zasah

        if nove_PWM > 255:
            nove_PWM = 255

        # toto nastane ve chvili, kdy by akcni_zasah zpomaleni byl
        # vetsi nez aktualni rychlost
        # myslenka je, ze chceme zpomalit co nejvice muzeme, tedy v nasem pripade zastavit
        # rozjet motor na opacnou stranu za me z pohledu rizeni rychlosti otaceni nedava smysl
        # ale muzeme se o tom pobavit :)

        if nove_PWM < 0:
            nove_PWM  = 0

        return self.__jed_PWM(nove_PWM)
