from neopixel import NeoPixel
from microbit import pin0, sleep, button_a
from utime import ticks_ms, ticks_diff

class LedColors:
    BILA = (60, 60, 60)
    CERVENA_SLABA = (60, 0, 0)
    VYPNUTO = (0, 0, 0)
    CERVENA_SILNA = (255, 0, 0)
    ORANZOVA = (100, 35, 0)

class LedPins:
    HEADLIGHTS = (0, 3)
    BACKLIGHTS = (5, 6)
    INDICATOR_LEFT = (1, 4)
    INDICATOR_RIGHT = (2, 7)
    INDICATOR_WARNING = (1, 2, 4, 7)


class LedSettings:

    def __init__(self):
        self.np = NeoPixel(pin0, 8)

    def initialize(self):
        self.np.show()

    def setPinColor(self, pin, color):
        self.np[pin] = color

    def getPinColor(self, pin):
        return self.np[pin]

class Lights:

    def __init__(self):
        self.ledSettings = LedSettings()
        self.ledPins = LedPins()
        self.headlights = self.ledPins.HEADLIGHTS
        self.backlights = self.ledPins.BACKLIGHTS

    def lightsON(self):
        for pin in self.headlights:
            self.ledSettings.setPinColor(pin, LedColors.BILA)
        for pin in self.backlights:
            self.ledSettings.setPinColor(pin, LedColors.CERVENA_SLABA)
        self.ledSettings.initialize()

    def lightsOFF(self):
        for pin in self.headlights:
            self.ledSettings.setPinColor(pin, LedColors.VYPNUTO)
        for pin in self.backlights:
            self.ledSettings.setPinColor(pin, LedColors.VYPNUTO)
        self.ledSettings.initialize()

    def lightsBreakON(self):
        for pin in self.backlights:
            self.ledSettings.setPinColor(pin, LedColors.CERVENA_SILNA)
        self.ledSettings.initialize()

    def lightsBreakOFF(self):
        for pin in self.backlights:
            self.ledSettings.setPinColor(pin, LedColors.CERVENA_SLABA)
        self.ledSettings.initialize()

    def lightsBackON(self):
        for pin in self.backlights:
            self.ledSettings.setPinColor(pin, LedColors.BILA)
        self.ledSettings.initialize()

    def lightsBackOFF(self):
        for pin in self.backlights:
            self.ledSettings.setPinColor(pin, LedColors.CERVENA_SLABA)
        self.ledSettings.initialize()


    def lightsIndicator(self, direction, last_ind_act):
        if ticks_diff(ticks_ms(), last_ind_act) >= 400 and self.ledSettings.getPinColor(direction[0]) == LedColors.VYPNUTO:
            for pin in direction:
                self.ledSettings.setPinColor(direction[0], LedColors.ORANZOVA)
            self.ledSettings.initialize()
            return ticks_ms()
        elif ticks_diff(ticks_ms(), last_ind_act) >= 400 and self.ledSettings.getPinColor(direction[0]) == LedColors.ORANZOVA:
            for pin in direction:
                self.ledSettings.setPinColor(direction[0], LedColors.VYPNUTO)
            self.ledSettings.initialize()
            return ticks_ms()
        else:
            return last_ind_act

    def test(self):
        print(self.ledSettings.getPinColor(0))

if __name__ == "__main__":
    lights = Lights()
    while not button_a.was_pressed():

        lights.lightsON()
        sleep(1000)
        lights.lightsBreakON()
        sleep(1000)
        lights.lightsBreakOFF()
        sleep(1000)
        lights.lightsBackON()
        sleep(1000)
        lights.lightsBackOFF()
        sleep(1000)
        lights.lightsOFF()
        sleep(1000)

