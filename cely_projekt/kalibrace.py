from microbit import sleep, i2c
from utime import ticks_diff, ticks_us

from cely_projekt import Konstanty, Motor

class Kalibrace:

    def __init__(self, prumer_kola: float, smer: string, akcelerace: string, nova_verze: bool = True):
        """
        Konstrukt tridy: vytvoreni objektu motoru a jejich inicializace
        """
        self.__levy_motor = Motor(Konstanty.LEVY, prumer_kola, nova_verze)
        self.__pravy_motor = Motor(Konstanty.PRAVY, prumer_kola, nova_verze)
        self.__smer = smer
        self.__akcelerace = akcelerace

        i2c.init(400000)
        self.__levy_motor.inicializuj()
        self.__pravy_motor.inicializuj()

        self.__min_rychlost_rozjezd = {}
        self.__min_pwm_rozjezd = {}

        self.__min_pwm_dojezd = {}

        self.__min_rychlost_rozjezd[Konstanty.LEVY] = -1
        self.__min_pwm_rozjezd[Konstanty.LEVY] = -1
        self.__min_pwm_dojezd[Konstanty.LEVY] = -1

        self.__min_rychlost_rozjezd[Konstanty.PRAVY] = -1
        self.__min_pwm_rozjezd[Konstanty.PRAVY] = -1
        self.__min_pwm_dojezd[Konstanty.PRAVY] = -1

    def kalibruj(self):
        """
        Zmeri zavislost mezi PWM a uhlovou rychlosti
        """

        self.__levy_motor.__smer = self.__smer
        self.__pravy_motor.__smer = self.__smer

        navratova_hodnota = 0

        if self.__akcelerace == "zrychluj":
            rozsah = range(50,256)
        elif self.__akcelerace == "zpomaluj":
            rozsah = range(255,30, -1)
        else:
            print("spatne akcelerace, hodnoty jsou: zrychluj nebo zpomaluj")
            return

        for pwm in rozsah:
            if self.__nastav_pwm(pwm) != 0:
                break

            cas_minule = ticks_us()
            cas_ted = cas_minule

            while ticks_diff(cas_ted, cas_minule) < 1000000:
                cas_ted = ticks_us()
                navratova_hodnota = self.__aktualizuj_se()
                if navratova_hodnota < 0:
                    break
                sleep(5)

            if navratova_hodnota < 0:
                break

            self.__vycti_rychlosti(pwm)

        navratova_hodnota = self.__levy_motor.__jed_PWM(0)
        navratova_hodnota = self.__pravy_motor.__jed_PWM(0)

        print("\n\n\n")
        if self.__akcelerace == "zrychluj":
            print("min_rychlost_rozjezd_levy", self.__min_rychlost_rozjezd[Konstanty.LEVY])
            print("min_pwm_rozjezd_levy", self.__min_pwm_rozjezd[Konstanty.LEVY])
            print()
            print("min_rychlost_rozjezd_pravy", self.__min_rychlost_rozjezd[Konstanty.PRAVY])
            print("min_pwm_rozjezd_pravy", self.__min_pwm_rozjezd[Konstanty.PRAVY])
        elif self.__akcelerace == "zpomaluj":
            print("min_pwm_dojezd_levy", self.__min_pwm_dojezd[Konstanty.LEVY])
            print()
            print("min_pwm_dojezd_pravy", self.__min_pwm_dojezd[Konstanty.PRAVY])


        # TODO udelej kalibraci automaticky

        self.__limity = [4.705, 12.37498]
        self.__primky_par_a = [17.07965]
        self.__primky_par_b = [28.63963]
        return 0

    def __nastav_pwm(self, pwm):

        navratova_hodnota = self.__levy_motor.__jed_PWM(pwm)
        if navratova_hodnota != 0:
            print("chyba v __levy_motor.__jed_PWM", navratova_hodnota)
            return navratova_hodnota

        navratova_hodnota = self.__pravy_motor.__jed_PWM(pwm)
        if navratova_hodnota != 0:
            print("chyba v __pravy_motor.__jed_PWM", navratova_hodnota)
            return navratova_hodnota

        return 0

    def __aktualizuj_se(self):
        navratova_hodnota = self.__levy_motor.__enkoder.aktualizuj_se()
        if navratova_hodnota < 0:
            print("chyba v levem enkoderu - aktualizuj_se", navratova_hodnota)
            return navratova_hodnota

        navratova_hodnota = self.__pravy_motor.__enkoder.aktualizuj_se()
        if navratova_hodnota < 0:
            print("chyba v pravem enkoderu - aktualizuj_se", navratova_hodnota)
            return navratova_hodnota

        return 0

    def __vycti_rychlosti(self, pwm):
        aktualni_rychlost_leve = self.__levy_motor.__enkoder.vypocti_rychlost()
        aktualni_rychlost_prave = self.__pravy_motor.__enkoder.vypocti_rychlost()

        if self.__akcelerace == "zrychluj":
            self.__vypocti_min_rozjezd_rychlost(aktualni_rychlost_leve, pwm, Konstanty.LEVY)
            self.__vypocti_min_rozjezd_rychlost(aktualni_rychlost_prave, pwm, Konstanty.PRAVY)
        elif self.__akcelerace == "zpomaluj":
            self.__vypocti_min_dojezd_rychlost(aktualni_rychlost_leve, pwm, Konstanty.LEVY)
            self.__vypocti_min_dojezd_rychlost(aktualni_rychlost_prave, pwm, Konstanty.PRAVY)
        else:
            print("spatny akcelerace")
            return -1

        print(aktualni_rychlost_leve, pwm, aktualni_rychlost_prave, pwm, sep=";")
        return 0

    def __vypocti_min_rozjezd_rychlost(self, rychlost, pwm, jmeno):

        if rychlost > 0:
            if self.__min_pwm_rozjezd[jmeno] == -1:
                self.__min_pwm_rozjezd[jmeno] = pwm
                self.__min_rychlost_rozjezd[jmeno] = rychlost
        elif rychlost == 0:
            # min rychlost byla protoze jsme do motoru stouchli
            # motor se ale same netoci
            if self.__min_pwm_rozjezd[jmeno] != -1:
                self.__min_pwm_rozjezd[jmeno] = -1
                self.__min_rychlost_rozjezd[jmeno] = 0

    def __vypocti_min_dojezd_rychlost(self, rychlost, pwm, jmeno):
        if rychlost == 0:
            if self.__min_pwm_dojezd[jmeno] == -1:
                self.__min_pwm_dojezd[jmeno] = pwm
        elif rychlost > 0:
            if self.__min_pwm_dojezd[jmeno] != -1:
                self.__min_pwm_dojezd[jmeno] = -1



