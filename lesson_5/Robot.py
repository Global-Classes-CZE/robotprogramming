from Light import Light
from microbit import sleep
from utime import ticks_ms, ticks_diff

class AnyLight:

    all_lights = (0, 1, 2, 3, 4, 5, 6, 7)
    color_led_off = (0, 0, 0)                   # vypnuto

    def __init__(self, svetla:Light):
        self.svetla = svetla

    def nastav_barvy(self, seznam_led, barva):
        for led in seznam_led:
            self.svetla.nastav_barvu(led, barva)

class MainLight(AnyLight):
    head_lights = (0, 3)                        # predni vnitrni LED
    back_lights = (5, 6)                        # zadni vnitni LED
    inside_light = (0, 3, 5, 6)                 # vsechny vnitrni LED
    reverse_lights = (5, )                      # leva zadni vnitni LED (zpatecka)
    color_led_white = (60, 60, 60)              # potkavaci svetla (a zpatecka)
    color_led_red = (60, 0, 0)                  # zadni svetla
    color_led_red_br = (255, 0, 0)              # brzda

    def __init__(self, svetla: Light):
        super().__init__(svetla)
        self.main = False                               # sviti hlavni svetla
        self.brake = False                              # sviti brzdy
        self.reverse = False                            # sviti zpatecka

    def setMain(self, value):
        self.main = value

    def setBrake(self, value):
        self.brake = value

    def setReverse(self, value):
        self.reverse = value

    def vykresli_led(self):
        headColor = self.color_led_off                  # zapamatuj si (pro predni svetla) zhasnutou barvu
        backColor = self.color_led_off                  # zapamatuj si (pro zadni svetla) zhasnutou barvu
        if self.main:                                   # jsou hlavni svetla zapnuta?
            headColor = self.color_led_white            # zapamatuj si (pro predni svetla) bilou barvu
            backColor = self.color_led_red              # zapamatuj si (pro zadni svetla) cervenou barvu
        if self.brake:                                  # je zapnuta brzda?
            backColor = self.color_led_red_br           # zapamatuj si (pro zadni svetla) silnejsi cervenou barvu

        self.nastav_barvy(self.head_lights,headColor)   # nastav barvu do prednich svetel
        self.nastav_barvy(self.back_lights,backColor)   # nastav barvu do zadnich svetel

        if self.reverse:                                # ma svitit zpatecka?
            self.nastav_barvy(self.reverse_lights,self.color_led_white) # nastav barvu pro zpatecku

        self.svetla.np.write()

class IndicatorDirectionEnum:
    NONE = 0
    LEFT = 1
    RIGHT = 2

class IndicatorStateEnum:
    NONE = 0
    SPACE = 1
    LIGHT = 2

class IndicatorLight(AnyLight):
    indicator_all = (1, 2, 4, 7)                        # vsechny vnejsi LED
    indicator_left = (1, 4)                             # leve vnejsi LED
    indicator_right = (2, 7)                            # prave vnejsi LED
    color_led_orange = (100, 35, 0)                     # blinkry

    def __init__(self, svetla: Light):
        super().__init__(svetla)
        self.direction = IndicatorDirectionEnum.NONE    # blinkry (hodnoty NONE, LEFT, RIGHT)
        self.warning = False                            # sviti vystrazny trojuhelnik (blokujeme cestu)
        self.setState(IndicatorStateEnum.NONE)

    def setState(self, state):
        self.state = state                              # nastavime novy stav
        self.start = ticks_ms()                         # a zapamatujeme start tohoto stavu

    def setDirection(self, value):
        self.direction = value

    def setWarning(self, value):
        self.direction = value

    def vykresli_led(self):
        backupState = self.state                        # zapamatuje stav pred vypoctem

        if self.direction != IndicatorDirectionEnum.NONE or self.warning:
            if self.state == IndicatorStateEnum.NONE:   # zatim se neblikalo?
                self.setState(IndicatorStateEnum.LIGHT) # zacneme blikat tim ze rozsvitime
            else:
                if ticks_diff(ticks_ms(), self.start) > 400: # stav uz trva moc dlouho => zmenime stav
                    self.setState(IndicatorStateEnum.SPACE if self.state == IndicatorStateEnum.LIGHT else IndicatorStateEnum.LIGHT)
        else:                                           # nemame blikat
            self.setState(IndicatorStateEnum.NONE)      # vypneme stav blikani

        if self.state != backupState:                   # zmenil se stav? pokud ano, budeme menit ledky
            if self.state == IndicatorStateEnum.LIGHT:  # blinkry maji svitit?
                if self.direction == IndicatorDirectionEnum.LEFT or self.warning:
                    self.nastav_barvy(self.indicator_left, self.color_led_orange)   # nastav levym blinkrum oranzovou barvu
                if self.direction == IndicatorDirectionEnum.RIGHT or self.warning:
                    self.nastav_barvy(self.indicator_right, self.color_led_orange)  # nastav pravym blinkrum oranzovou barvu
            else:
                self.nastav_barvy(self.indicator_all, self.color_led_off)           # nastav vsem blinkrum zhasnutou barvu
            self.svetla.np.write()

class Robot:

    def __init__(self):
        self.svetla = Light()
        self.main = MainLight(self.svetla)
        self.indicator = IndicatorLight(self.svetla)

    def indikuj(self, smer_zataceni):
        if smer_zataceni == "doleva":
            self.indicator.setDirection(IndicatorDirectionEnum.LEFT)
        elif smer_zataceni == "doprava":
            self.indicator.setDirection(IndicatorDirectionEnum.RIGHT)
        else:
            self.indicator.setDirection(IndicatorDirectionEnum.NONE)
        self.indicator.vykresli_led()

    def zapni_svetla(self):
        self.main.setMain(True)
        self.main.vykresli_led()

    def vypni_svetla(self):
        self.main.setMain(False)
        self.main.vykresli_led()

    def brzdi(self):
        self.main.setBrake(True)
        self.main.vykresli_led()

        sleep(1000)

        self.main.setBrake(False)
        self.main.vykresli_led()

def main():
    robot = Robot()
    while True:
        for i in range(100):
            robot.indikuj("doprava")
            sleep(50)
        for i in range(100):
            robot.indikuj("doleva")
            sleep(50)
        robot.indikuj("rovne")
        robot.zapni_svetla()
        sleep(4000)
        for i in range(100):
            robot.indikuj("doprava")
            sleep(50)
        for i in range(100):
            robot.indikuj("doleva")
            sleep(50)
        robot.indikuj("rovne")
        sleep(3000)
        robot.brzdi()
        sleep(2000)
        robot.main.setReverse(True)
        robot.main.vykresli_led()
        sleep(2000)
        robot.main.setReverse(False)
        robot.main.vykresli_led()
        sleep(2000)
        robot.vypni_svetla()

if __name__ == "__main__":
    main()

