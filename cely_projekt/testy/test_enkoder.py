from microbit import button_a, sleep

from enkoder import Enkoder
from konstanty import Konstanty

def zakladni_test_spusteni(jmeno, nova_verze):
    hodnota_testu = -1
    enkoder = Enkoder(jmeno, 1, nova_verze)
    enkoder.inicializuj()
    while not button_a.was_pressed():
        navratova_hodnota = enkoder.aktualizuj_se()
        print(enkoder.vypocti_rychlost())
        if navratova_hodnota < 0:
            hodnota_testu = 0
            return hodnota_testu
        sleep(5)

    return 1

if __name__ == "__main__":

    print(zakladni_test_spusteni(Konstanty.LV_ENKODER, False), "zakladni_test_spusteni")
    print(zakladni_test_spusteni(Konstanty.PR_ENKODER, False), "zakladni_test_spusteni")

