from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

def zapni(poradi_led, barva_on, prodleva_on):
    np[poradi_led] = barva_on
    nastav_barvu()
    sleep(prodleva_on)

def vypni(poradi_led, barva_off, prodleva_off):
    np[poradi_led] = barva_off
    nastav_barvu()
    sleep(prodleva_off)

def nastav_barvu():
    np.write()

np = NeoPixel(pin0,8)
poradi_led = 0
barva_on = (255, 255, 255)
barva_off = (0, 0, 0)
prodleva_on = 1000
prodleva_off = 1000


while True:
    zapni(poradi_led, barva_on, prodleva_on)
    vypni(poradi_led, barva_off, prodleva_off)

