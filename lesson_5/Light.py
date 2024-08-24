from neopixel import NeoPixel
from microbit import pin0, sleep
from utime import ticks_ms, ticks_diff

class Light:
    color_led_off = (0, 0, 0)                           # vypnuto
    color_led_orange = (100, 35, 0)                     # blinkry
    color_led_white = (60, 60, 60)                      # potkavaci svetla (a zpatecka)
    color_led_white_hi = (255, 255, 255)                # dalkova svetla
    color_led_red = (60, 0, 0)                          # zadni svetla
    color_led_red_br = (255, 0, 0)                      # brzda

    def __init__(self):
        self.np = NeoPixel(pin0, 8)
        self.main = MainLight()
        self.indicator = IndicatorLight()

    def nastav_barvu(self, poradi_led, barva):
        self.np[poradi_led] = barva

    def nastav_barvu_do_vice_led(self, seznam_led, barva):
        for poradi_led in seznam_led:
            self.nastav_barvu(poradi_led, barva)

    def zapni_potkavaci(self):
        self.main.setMain(HeadLightEnum.POTKAVACI)
        self.main.show_led(self)

    def vypni_potkavaci(self):
        self.main.setMain(HeadLightEnum.VYPNUTO)
        self.main.show_led(self)

    def zapni_dalkove(self):
        self.main.setMain(HeadLightEnum.DALKOVA)
        self.main.show_led(self)

    def zapni_brzdy(self):
        self.main.setBrake(True)
        self.main.show_led(self)

    def vypni_brzdy(self):
        self.main.setBrake(False)
        self.main.show_led(self)

    def zapni_zpatecku(self):
        self.main.setReverse(True)
        self.main.show_led(self)

    def vypni_zpatecku(self):
        self.main.setReverse(False)
        self.main.show_led(self)

    def indikuj(self, direction):
        self.indicator.setDirection(direction)
        self.indicator.show_led(self)

    def write(self):
        self.np.write()


class IndicatorState:
    NONE = 0
    SPACE = 1
    LIGHT = 2

    def __init__(self):
        self.reset()

    def reset(self):
        self.set(self.NONE)

    def set(self, value):
        self.value = value                              # nastav novy stav
        self.start = ticks_ms()                         # a zapamatuj si kdy to bylo

    def get(self):
        return self.value

    def isDiferent(self, other):
        return self.get() != other

    def timeout(self):                                  # trva stav uz moc dlouho?
        return ticks_diff(ticks_ms(), self.start) > 400

    def change(self):                                   # zmen stav na opacny LIGH <--> SPACE
        self.set(self.SPACE if self.value == self.LIGHT else self.LIGHT)

    def run(self):
        if self.get() != self.NONE:                     # uz blikame?
            if self.timeout():                          # ano -> vyprsel cas stavu?
                self.change()                           #        ano -> zmen stav
        else:                                           # ne
            self.set(self.LIGHT)                        #     ->zacneme blikat tim, ze rozsvitime


class IndicatorDirectionEnum:
    NONE = 0
    LEFT = 1
    RIGHT = 2

class IndicatorLight:
    led_all = (1, 2, 4, 7)                              # vsechny vnejsi LED
    led_left = (1, 4)                                   # leve vnejsi LED
    led_right = (2, 7)                                  # prave vnejsi LED

    def __init__(self):
        self.setDirection(IndicatorDirectionEnum.NONE)  # blinkry (hodnoty NONE, LEFT, RIGHT)
        self.setWarning(False)                          # sviti vystrazny trojuhelnik (blokujeme cestu)
        self.state = IndicatorState()                   # stav blikani

    def setDirection(self, value):
        self.direction = value

    def setWarning(self, value):
        self.warning = value

    def show_led(self, light):
        backupState = self.state.get()                  # zapamatuj si stav pred vypoctem

        if self.direction != IndicatorDirectionEnum.NONE or self.warning: # mame blikat?
            self.state.run()                            # ano -> tak blikej
        else:                                           # ne (nemame blikat)
            self.state.reset()                          #     -> vypneme blikani

        if self.state.isDiferent(backupState):          # zmenil se stav? pokud ano, budeme menit ledky
            if self.state.get() == IndicatorState.LIGHT:# blinkry maji svitit?
                if self.direction == IndicatorDirectionEnum.LEFT or self.warning:
                    light.nastav_barvu_do_vice_led(self.led_left, light.color_led_orange)
                    # nastav levym blinkrum oranzovou barvu
                if self.direction == IndicatorDirectionEnum.RIGHT or self.warning:
                    light.nastav_barvu_do_vice_led(self.led_right, light.color_led_orange)
                    # nastav pravym blinkrum oranzovou barvu
            else:                                       # blinkry maji byt zhasnute
                light.nastav_barvu_do_vice_led(self.led_all, light.color_led_off)
                # nastav vsem blinkrum zhasnutou barvu
            light.write()



class HeadLightEnum:
    VYPNUTO = 0
    POTKAVACI = 1
    DALKOVA = 2

class MainLight:
    head_lights = (0, 3)                                # predni vnitrni LED
    back_lights = (5, 6)                                # zadni vnitni LED
    inside_light = (0, 3, 5, 6)                         # vsechny vnitrni LED
    reverse_lights = (5,)                               # leva zadni vnitni LED (zpatecka)

    def __init__(self):
        self.setMain(HeadLightEnum.VYPNUTO)
        self.setBrake(False)
        self.setReverse(False)

    def setMain(self, value):
        self.main = value

    def setBrake(self, value):
        self.brake = value

    def setReverse(self, value):
        self.reverse = value

    def show_led(self, light):
        headColor = light.color_led_off                 # zapamatuj si (pro predni svetla) zhasnutou barvu
        backColor = light.color_led_off                 # zapamatuj si (pro zadni svetla) zhasnutou barvu
        if self.main == HeadLightEnum.POTKAVACI:        # jsou hlavni svetla zapnuta na potkavaci?
            headColor = light.color_led_white           # zapamatuj si (pro predni svetla) bilou barvu
            backColor = light.color_led_red             # zapamatuj si (pro zadni svetla) cervenou barvu
        if self.main == HeadLightEnum.DALKOVA:          # jsou hlavni svetla zapnuta na dalkova?
            headColor = light.color_led_white_hi        # zapamatuj si (pro predni svetla) bilou barvu
            backColor = light.color_led_red             # zapamatuj si (pro zadni svetla) cervenou barvu
        if self.brake:                                  # je zapnuta brzda?
            backColor = light.color_led_red_br          # zapamatuj si (pro zadni svetla) silnejsi cervenou barvu

        light.nastav_barvu_do_vice_led(self.head_lights, headColor)
                                                        # nastav barvu do prednich svetel
        light.nastav_barvu_do_vice_led(self.back_lights, backColor)
                                                        # nastav barvu do zadnich svetel

        if self.reverse:                                # ma svitit zpatecka?
            light.nastav_barvu_do_vice_led(self.reverse_lights, light.color_led_white)
                                                        # nastav barvu pro zpatecku
        light.write()
