from time import sleep

from cely_projekt import Senzory, Konstanty
from microbit import button_a, sleep

class Naraznik:

    NAME_LEFT = "levy_IR"
    NAME_RIGHT = "pravy_IR"

    # jmeno muze byt jen levy_IR a nebo pravy_IR
    def __init__(self, name, senzory: Senzory):
        self.__name = name
        self.__senzory = senzory

    def narazil_jsem(self):
        data = self.__senzory.precti_senzory()

        if self.__name == Naraznik.NAME_LEFT:
            return data[Konstanty.LV_IR] == False
        elif self.__name == Naraznik.NAME_RIGHT:
            return data[Konstanty.PR_IR] == False

        return False


senzory = Senzory()
if __name__ == "__main__":
    levy_naraznik = Naraznik(Naraznik.NAME_LEFT, senzory)

    while not button_a.was_pressed():
        print("Narazil jsem?", levy_naraznik.narazil_jsem())
        sleep(1000)
