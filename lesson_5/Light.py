from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

class Light:

    def __init__(self):
        self.np = NeoPixel(pin0, 8)

    # ponechano kvuli zpetne kompatibilite (nepouzivat)
    def zapni(self, poradi_led):
        self.nastav_barvu(poradi_led, (255, 255, 255))
        self.np.write()

    # ponechano kvuli zpetne kompatibilite (nepouzivat)
    def vypni(self, poradi_led):
        self.nastav_barvu(poradi_led, (0, 0, 0))
        self.np.write()

    # ponechano kvuli zpetne kompatibilite (nepouzivat)
    def nastav_barvu(self, poradi_led, barva):
        self.np[poradi_led] = barva

def main():
    svetla = Light()
    while True:
        svetla.zapni(0)
        sleep(500)
        svetla.vypni(0)
        sleep(500)

if __name__ == "__main__" :
    main()
