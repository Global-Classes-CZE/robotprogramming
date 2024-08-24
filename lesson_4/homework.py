from neopixel import NeoPixel
from microbit import pin0, sleep, button_a


np = NeoPixel(pin0, 8)


def zapni(poradi_led):
    np[poradi_led] = (0, 255, 0)
    np.write()


def vypni(poradi_led):
    np[poradi_led] = (0, 0, 0)
    np.write()


def nastav_barvu(poradi_led, barva):
    np[poradi_led] = barva
    np.write()


while not button_a.is_pressed():
    zapni(0)
    sleep(500)
    vypni(0)
    sleep(500)
    zapni(2)
    sleep(500)
    vypni(2)
    sleep(500)
    nastav_barvu(0, (255, 0, 0))
    sleep(500)
    vypni(0)
    sleep(500)


