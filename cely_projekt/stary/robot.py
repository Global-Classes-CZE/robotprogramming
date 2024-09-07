from microbit import i2c

from konstanty import Konstanty
from motor import Motor

class Robot:


    def __init__(self, rozchod_kol: float, prumer_kola: float):
        """
        Konstruktor tridy
        """
        self.__d = rozchod_kol/2
        self.__prumer_kola = prumer_kola

        self.__levy_motor = Motor(Konstanty.LEVY, self.__prumer_kola)
        self.__pravy_motor = Motor(Konstanty.PRAVY, self.__prumer_kola)
        self.__inicializovano = False

    def inicializuj(self):
        i2c.init(400000)
        self.__levy_motor.inicializuj()
        self.__pravy_motor.inicializuj()
        self.__inicializovano = True

    # pokrocily ukol 7
    def jed(self, dopredna_rychlost: float, uhlova_rychlost: float):
        """Pohybuj se zadanym  pohybem slozenym z dopredne rychlosti v a uhlove rychlosti"""

        if not self.__inicializovano:
            return -1
        # kinematika diferencionalniho podvozku - lekce 7
        dopr_rychlost_leve = dopredna_rychlost - self.__d * uhlova_rychlost
        dopr_rychlost_prave = dopredna_rychlost + self.__d * uhlova_rychlost

        # nevolam povely i2c rovnou - to bych rozbijela zapouzdreni trid
        # vyuziji funkce tridy motor
        self.__levy_motor.jed_doprednou_rychlosti(dopr_rychlost_leve)
        self.__pravy_motor.jed_doprednou_rychlosti(dopr_rychlost_prave)

        return 0
