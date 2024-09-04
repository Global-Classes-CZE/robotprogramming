from microbit import button_a, sleep

from enkoder import Enkoder
from konstanty import Konstanty

def zakladni_test_spusteni(nova_verze):
    hodnota_testu = -1
    lv_enkoder = Enkoder(Konstanty.LV_ENKODER, 1, nova_verze)
    lv_enkoder.inicializuj()
    while not button_a.was_pressed():
        navratova_hodnota = lv_enkoder.aktualizuj_se()
        print(lv_enkoder.vypocti_rychlost())
        if navratova_hodnota < 0:
            hodnota_testu = 0
            return hodnota_testu
        sleep(5)

    return 1

if __name__ == "__main__":

    print(zakladni_test_spusteni(False), "zakladni_test_spusteni")

