from senzory import Senzory
from microbit import button_a
from konstanty import Konstanty

class Naraznik:

    # jmeno muze byt jen levy_IR a nebo pravy_IR
    def __init__(self, jmeno):
        if jmeno != Konstanty.LV_IR and jmeno != Konstanty.PR_IR:
            return -1

        self.jmeno = jmeno
        self.senzory = Senzory(True)

    def narazil_jsem(self):
        data_Senzorov = self.senzory.precti_senzory()

        if int(data_Senzorov[Konstanty.LV_IR]) == 1:
            return False
        else:
            return True

if __name__ == "__main__":
    levy_naraznik = Naraznik(Konstanty.LV_IR)

    while not button_a.was_pressed():
        print(levy_naraznik.narazil_jsem())

