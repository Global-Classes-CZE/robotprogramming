from microbit import i2c, pin0, pin8, pin12, sleep, button_a, button_b
from neopixel import NeoPixel
from utime import ticks_ms, ticks_diff
from machine import time_pulse_us


class Math:
    def clamp(self, n):
        return max(min(255, n), 0)

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


class Ultrazvuk:

    def __init__(self):
        self.__trigger = pin8
        self.__echo = pin12

        self.__trigger.write_digital(0)
        self.__echo.read_digital()

    def zmer_vzdalenost(self):

        rychlost_zvuku = 340 #m/s

        self.__trigger.write_digital(1)
        self.__trigger.write_digital(0)

        zmereny_cas_us = time_pulse_us(self.__echo, 1)
        if zmereny_cas_us < 0:
            return zmereny_cas_us

        zmereny_cas_s = zmereny_cas_us / 1000000
        vzdalenost = zmereny_cas_s * rychlost_zvuku / 2

        return vzdalenost


class Robot:
    def __init__(self):
        self.math = Math()
        self.lights = Lights()
        self.ultrazvuk = Ultrazvuk()

    def initialize(self):
        i2c.init(freq=400000)
        i2c.write(0x70, b"\x00\x01")
        i2c.write(0x70, b"\xE8\xAA")
        self.lights.lightsON()

    def jed(self, dopredna_rychlost:float, rotace:float):
        lights.lightsON()
        self.param_motor_prava_dozadu = b'\x02'
        self.param_motor_prava_dopredu = b'\x03'
        self.param_motor_leva_dozadu = b'\x04'
        self.param_motor_leva_dopredu = b'\x05'

        self.d = 0.075
        self.v_l = int(dopredna_rychlost - self.d * rotace)
        self.v_r = int(dopredna_rychlost + self.d * rotace)
        print(self.v_l, " ", self.v_r)

         # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r

        #kontrola rychlosti a smeru praveho kola
        if self.v_r > 0:
            i2c.write(0x70, self.param_motor_prava_dopredu + bytes([self.math.clamp(self.v_r)]))
        elif self.v_r < 0:
            i2c.write(0x70, self.param_motor_prava_dozadu + bytes([self.math.clamp(abs(self.v_r))]))
        elif self.v_r == 0:
            i2c.write(0x70, self.param_motor_prava_dozadu + bytes([0]))
            i2c.write(0x70, self.param_motor_prava_dopredu + bytes([0]))

        #kontrola rychlosti a smeru leveho kola
        if self.v_l > 0:
            i2c.write(0x70, self.param_motor_leva_dopredu + bytes([self.math.clamp(self.v_l)]))
        elif self.v_l < 0:
            i2c.write(0x70, self.param_motor_leva_dozadu + bytes([self.math.clamp(abs(self.v_l))]))
        elif self.v_l == 0:
            i2c.write(0x70, self.param_motor_leva_dozadu + bytes([0]))
            i2c.write(0x70, self.param_motor_leva_dopredu + bytes([0]))


    def zastav(self):
        self.jed(0, 0)
        lights.lightsBreakON()

    def couvej(self, rychlost):
        self.jed(-rychlost, 0)
        lights.lightsBackON()

    def jedPomalu(self, rychlost):
        self.jed(rychlost/2, 0)

    def tempomat(self, rychlost):

        if self.ultrazvuk.zmer_vzdalenost() > 0.2:
            self.zastav()
            self.jed(rychlost*self.ultrazvuk.zmer_vzdalenost()/0.2, 0)
        elif self.ultrazvuk.zmer_vzdalenost() <= 0.2:
            self.zastav()
            self.couvej(rychlost*(1-self.ultrazvuk.zmer_vzdalenost()/0.2))



if __name__ == "__main__":
    robot = Robot()
    lights = Lights()
    robot.initialize()
    while True:
        if button_a.was_pressed():
            while not button_b.was_pressed():
                robot.tempomat(200)

            robot.zastav()
            lights.lightsOFF()




