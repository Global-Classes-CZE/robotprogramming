from microbit import button_a, sleep, i2c

from cely_projekt import Konstanty, KalibracniFaktory, Robot

def zakladni_test_spusteni():

    min_rychlost = 2.1658
    min_pwm_rozjezd = 79 # kalibrace vytiskne na konci pri "zrychluj"
    min_pwm_dojezd = 41 # kalibrace vytiskne na konci pri "zpomaluj"
    a = 24.3732783404646 # ziskej z excelu
    b = 8.21172006498485 # ziskej z excelu

    levy_faktor = KalibracniFaktory(min_rychlost, min_pwm_rozjezd, min_pwm_dojezd, a, b)

    min_rychlost = 2.171571
    min_pwm_rozjezd = 113
    min_pwm_dojezd = 113
    a = 27.4515630414309
    b = 61.3869817945568

    pravy_faktor = KalibracniFaktory(min_rychlost, min_pwm_rozjezd, min_pwm_dojezd, a, b)

    robot = Robot(0.15, 0.067, levy_faktor, pravy_faktor, True)
    robot.inicializuj()
    robot.jed(0.067*Konstanty.PI, 0)

    while not button_a.was_pressed():
        sleep(5)
        robot.aktualizuj_se()

    robot.jed(0,0)

if __name__ =="__main__":
    zakladni_test_spusteni()

