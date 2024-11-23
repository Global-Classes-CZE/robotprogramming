from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

np = NeoPixel(pin0, 8)

def zapni(poradi_led):
    nastav_barvu(poradi_led, (255, 255, 255))
    np.write()  # po zavolani tohoto prikazu se stav LED zmeni
    # proto je vice vhodne ho volat z teto funkce a ne z nastav_barvu
    # protoze jmeno "nastav_barvu" nerika nic o tom, ze se LED zmeni

def vypni(poradi_led):
    nastav_barvu(poradi_led, (0, 0, 0))
    np.write()

def nastav_barvu(poradi_led, barva):
    np[poradi_led] = barva

if __name__ == "__main__":

    while True:
        zapni(0)  # nastavim prvni ledku, tzn [0] na bilou (RGB hodnoty)
        sleep(1000)
        vypni(0)  # nastavim prvni ledku, tzn [0] na cernou (RGB hodnoty)
        sleep(1000)

