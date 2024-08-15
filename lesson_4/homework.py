from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

barva = (255, 255, 255)

def zapni(poradi_led):
    np[poradi_led] = (255, 255, 255)  # nastavim vybranou ledku na bilou (RGB hodnoty)
    np.write()

def vypni(poradi_led):
    np[poradi_led] = (0, 0, 0)  # nastavim vybranou ledku na cernou (RGB hodnoty)
    np.write()

def nastav_barvu(poradi_led, barva):
    np[poradi_led] = barva
    np.write()

np = NeoPixel(pin0, 8)
# TODO: predelejte smycku tak, aby volala vyse definovane funkce

while True:
    zapni(0)
    sleep(1000)

    vypni(0)
    sleep(1000)
