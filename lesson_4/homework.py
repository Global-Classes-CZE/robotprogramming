from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from microbit import button_a
from random import randint

np = NeoPixel(pin0, 8)
np_colors = [(255, 255, 255) for _ in range(8)]  # uvodni barva je bila

def zkontroluj_poradi_led(poradi_led):
    if poradi_led < 0 or poradi_led > 7:
        raise ValueError("Poradi ledky musi byt v rozmezi 0 az 7")

def zapni(poradi_led):
    print("zapni %d" % poradi_led)
    zkontroluj_poradi_led(poradi_led)
    np[poradi_led] = np_colors[poradi_led]
    np.write()

def vypni(poradi_led):
    print("vypni %d" % poradi_led)
    zkontroluj_poradi_led(poradi_led)
    np[poradi_led] = (0, 0, 0)
    np.write()

def nastav_barvu(poradi_led, barva):
    print("nastav_barvu %d, %s" % (poradi_led, barva))
    zkontroluj_poradi_led(poradi_led)
    np_colors[poradi_led] = barva
    np[poradi_led] = barva
    np.write()

# Prvních pet cyklu je pro demonstraci nacrtnuteho zadani
#   prvni reflektor, vychozi bila barva (nezmenena logika)

# V dalsich cyklech testujeme postupne na vsech reflektorech zmenu barev led,
#   pak vypneme a znovu zapneme (tedy zmena na cernou a zpet na puvodni barvu)
cyklus = 0
reflektor = 0
while True:
    cyklus += 1
    if button_a.is_pressed():
        nastav_barvu(0, (255, 255, 255))
        cyklus = 0
    if cyklus < 5:
        zapni(0)  # nastavim prvni ledku, tzn [0] na bilou (uvodni RGB hodnoty)
        sleep(500)
        vypni(0)  # nastavim prvni ledku, tzn [0] na cernou (RGB hodnoty)
        sleep(500)
    else:
        barva = (randint(0, 255), randint(0, 255), randint(0, 255))
        nastav_barvu(reflektor, barva)
        sleep(200)
        vypni(reflektor)
        sleep(200)
        zapni(reflektor)
        sleep(200)
        vypni(reflektor)
        sleep(200)
        reflektor = (reflektor + 1) & 7  # rotujeme mezi 0-7, jednou pri kazdem cyklu
