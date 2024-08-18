from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from utime import ticks_ms, ticks_diff

class HeadLightEnum:
    VYPNUTO = 0
    OBRYSOVA = 1
    POTKAVACI = 2
    DALKOVA = 3

class IndicatorDirectionEnum:
    NONE = 0
    LEFT = 1
    RIGHT = 2

class IndicatorStateEnum:
    NONE = 0
    SPACE = 1
    LIGHT = 2

class Light:

    all_lights = (0, 1, 2, 3, 4, 5, 6, 7)
    inside_light = (0, 3, 5, 6)                 # vsechny vnitrni LED
    head_lights = (0, 3)                        # predni vnitrni LED
    back_lights = (5, 6)                        # zadni vnitni LED
    reverse_lights = (6)                        # prava zadni vnitni LED
    indicator_warning = (1, 2, 4, 7)            # vsechny vnejsi LED
    indicator_head = (1, 2)                     # predni vnejsi LED
    indicator_back = (4, 7)                     # zadni vnejsi LED
    indicator_left = (1, 4)                     # leve vnejsi LED
    indicator_right = (2, 7)                    # prave vnejsi LED

    color_led_off = (0, 0, 0)                   # vypnuto
    color_led_white_lo = (20, 20, 20)           # obrysova svetla
    color_led_white = (60, 60, 60)              # potkavaci svetla
    color_led_white_hi = (255, 255, 255)        # dalkova svetla
    color_led_reverse = (60, 60, 60)            # zpatecka
    color_led_red = (60, 0, 0)                  # zadni svetla
    color_led_red_br = (255, 0, 0)              # brzda
    color_led_orange = (100, 35, 0)             # blinkry

    def __init__(self):
        self.np = NeoPixel(pin0, 8)
        self.head = HeadLightEnum.VYPNUTO
        self.back = False
        self.brake = False
        self.reverse = False
        self.indicator = IndicatorDirectionEnum.NONE
        self.indicatorState = IndicatorStateEnum.NONE
        self.indicatorStart = 0
        self.warning = False
        self.postarej_se_o_svetla()

    # ponechano kvuli zpetne kompatibilite (nepouzivat)
    def zapni(self, poradi_led):
        self.nastav_barvu(poradi_led, (255, 255, 255))
        self.np.write()

    # ponechano kvuli zpetne kompatibilite (nepouzivat)
    def vypni(self, poradi_led):
        self.nastav_barvu(poradi_led, (0, 0, 0))
        self.np.write()

    def nastav_barvu(self, poradi_led, barva):
        self.np[poradi_led] = barva

    def nastav_barvu_do_vice_led(self, seznam_led, barva):
        for led in seznam_led:
            self.nastav_barvu(led, barva)

    # metoda se bude pravidelne volat a nastavuje objekt np (NeoPixel)
    #   podle nastavenych vlastnosti (podminek)
    def postarej_se_o_svetla(self):
        backup_np = []                                  # zazalohuj si soucasne barvy v LEDkach
        for i in range(len(self.np)):
            backup_np.append(self.np[i])

        headColor = self.color_led_off                  # zapamatuj si (pro predni svetla) zhasnutou barvu
        backColor = self.color_led_off                  # zapamatuj si (pro zadni svetla) zhasnutou barvu
        markerColor = self.color_led_off                # zapamatuj si (pro obryskova svetla) zhasnutou barvu

        if self.head != HeadLightEnum.VYPNUTO:          # jsou hlavni svetla zavypnuta?
            backColor = self.color_led_red              # zapamatuj si (pro zadni svetla) cervenou barvu
#            markerColor = self.color_led_white_lo       # zapamatuj si malo svitici bilou (obrysovou)
            headColor = self.color_led_white_lo         # zapamatuj si (pro predni svetla) malo svitici bilou (obrysovou)
            if self.head == HeadLightEnum.POTKAVACI:    # zapnuta predni svetla potkavaci
                headColor = self.color_led_white        # zapamatuj si bilou barvu
            elif self.head == HeadLightEnum.DALKOVA:    # zapnuta predni svetla dalkova
                headColor = self.color_led_white_hi     # zapamatuj si hodne svitici bilou (dalkova svetla)

        if self.brake:                                  # je zapnuta brzda?
            backColor = self.color_led_red_br           # zapamatuj si (pro zadni svetla) silnejsi cervenou barvu

        self.nastav_barvu_do_vice_led(self.head_lights,headColor) # nastav barvu do prednich svetel
        self.nastav_barvu_do_vice_led(self.back_lights,backColor) # nastav barvu do zadnich svetel
        self.nastav_barvu_do_vice_led(self.indicator_head,markerColor) # nastav barvu do obrysovych svetel

        # vyreseni blinkru
        self.nastav_barvu_do_vice_led(self.indicator_back,self.color_led_off) # nastav "zadnou" barvu do zadnich blinkru

        if self.indicator != IndicatorDirectionEnum.NONE or self.warning:
            if self.indicatorState == IndicatorStateEnum.NONE:  # drive se neblikalo
                self.indicatorState = IndicatorStateEnum.LIGHT  # zacneme blikat tim ze svitime
                self.indicatorStart = ticks_ms()                # a zapamatujeme start tohoto stavu
            else:
                if ticks_diff(ticks_ms(), self.indicatorStart) > 400: # uz to trva moc dlouho => zmenime stav
                    if self.indicatorState == IndicatorStateEnum.LIGHT:
                        self.indicatorState = IndicatorStateEnum.SPACE
                    else:
                        self.indicatorState = IndicatorStateEnum.LIGHT
                    self.indicatorStart = ticks_ms()            # a zapamatujeme start tohoto stavu

            if self.indicatorState == IndicatorStateEnum.LIGHT:      # blinkry maji svitit?
                if self.indicator == IndicatorDirectionEnum.LEFT or self.warning:
                    self.nastav_barvu_do_vice_led(self.indicator_left, self.color_led_orange) # a nastav jim barvu pro blinkry
                if self.indicator == IndicatorDirectionEnum.RIGHT or self.warning:
                    self.nastav_barvu_do_vice_led(self.indicator_right, self.color_led_orange) # a nastav jim barvu pro blinkry
        else:                                               # nemame blikat
            self.indicatorState = IndicatorStateEnum.NONE   # vypneme stav blikani

        if self.reverse:                                # je zapnuta zpatecka?
            for led in self.reverse_lights:             # projdi LEDky pro zpatecku
                self.np[led] = self.color_led_reverse   # a nastav jim barvu pro zpatecku


#        start = ticks_ms()
#        print(start)
        for i in range(len(self.np)):                   # projdi postupne vsechny LEDky
#            print(i)
            if backup_np[i] != self.np[i]:              # a porovnej zalohovanou a aktualni barvu
#                print("diference")
                self.np.write()                         # nasli jsme rozdil => odesli barvy do LEDek
                break

 #       delta = ticks_diff(ticks_ms(), start)
 #       print(delta)

    def zapni_brzdova(self):
        self.brake = True
        self.postarej_se_o_svetla()

    def vypni_brzdova(self):
        self.brake = False
        self.postarej_se_o_svetla()

    def vypni_svetla(self):
        self.head = HeadLightEnum.VYPNUTO
        self.back = False
        self.postarej_se_o_svetla()

    def zapni_svetla_obryskova(self):
        self.head = HeadLightEnum.OBRYSOVA
        self.back = True
        self.postarej_se_o_svetla()

    def zapni_svetla_potkavaci(self):
        self.head = HeadLightEnum.POTKAVACI
        self.back = True
        self.postarej_se_o_svetla()

    def zapni_svetla_dalkova(self):
        self.head = HeadLightEnum.DALKOVA
        self.back = True
        self.postarej_se_o_svetla()

    def smer_jizdy(self, smer: IndicatorDirectionEnum):
        if smer != self.indicator:
            if smer != IndicatorDirectionEnum.NONE:
                self.indicatorStart = 0
        self.indicator = smer
        self.postarej_se_o_svetla()

if __name__ == "__main__" :
    svetla = Light()
    while True:
        svetla.zapni_svetla_obryskova()
        sleep(3000)
        svetla.zapni_svetla_potkavaci()
        sleep(3000)
        svetla.zapni_svetla_dalkova()
        sleep(3000)
        svetla.vypni_svetla()
        sleep(3000)
        svetla.zapni_brzdova()
        sleep(3000)
        svetla.vypni_brzdova()
        sleep(3000)
        for i in range(300):
            svetla.smer_jizdy(IndicatorDirectionEnum.LEFT)
            sleep(10)
        for i in range(300):
            svetla.smer_jizdy(IndicatorDirectionEnum.RIGHT)
            sleep(10)
        for i in range(300):
            svetla.smer_jizdy(IndicatorDirectionEnum.NONE)
            sleep(10)
        svetla.zapni_svetla_potkavaci()
        for i in range(300):
            svetla.smer_jizdy(IndicatorDirectionEnum.LEFT)
            sleep(10)
        for i in range(300):
            svetla.smer_jizdy(IndicatorDirectionEnum.RIGHT)
            sleep(10)
        for i in range(300):
            svetla.smer_jizdy(IndicatorDirectionEnum.NONE)
            sleep(10)
