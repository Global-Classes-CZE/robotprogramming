from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from microbit import button_a
from utime import ticks_ms, ticks_diff

class Svetlo:

    # konstruktror
    def __init__(self, neopixel, poradi_led, barva):
        self.np = neopixel
        self.poradi_led = poradi_led
        self.barva = barva
        self.zapnuto = -1  # pouzivam int, abych rozlisila tri stavy:
        # 1 - zapnuto
        # 0 - vypnuto
        # -1 neurcity stav

    def zapni(self):
        self.nastav_barvu(self.barva)
        self.np.write()
        self.zapnuto = 1

    def vypni(self):
        barva = (0, 0, 0)
        self.nastav_barvu(barva)
        self.np.write()
        self.zapnuto = 0

    def nastav_barvu(self, barva):
        np[self.poradi_led] = barva

class Blinkr(Svetlo):

    def __init__(self, neopixel, poradi_led):
        super().__init__(neopixel, poradi_led, (100, 35, 0))
        self.cas_minule = ticks_ms()
        self.perioda_blikani = 500  # cas v ms

    def blikni(self):
        cas_ted = ticks_ms()
        # POZOR! ticks_diff vraci i negativni cislo,
        # tzn vzdy musite napsat ten vetsi cas jako prvni
        kolik_ubehlo_od_minula = ticks_diff(cas_ted, self.cas_minule)

        # rozdil casu je vetsi nez perioda_blikani, tzn chceme bliknout
        if kolik_ubehlo_od_minula > self.perioda_blikani:
            # bliknuti znamena zmenit stav - kdyz je ledka zapla, tak ji chceme vypnout
            if self.zapnuto == 1:
                self.vypni()
            elif self.zapnuto == 0:
                self.zapni()
            else:
                print("Blinkr neni inicializovan!")
                print("Zavolejte nejprve vypni() pred prvnim pouzitim!")

            self.cas_minule = cas_ted

if __name__ == "__main__":

    np = NeoPixel(pin0,8)
    poradi_led = 0
    predni_leve = Svetlo(np, poradi_led, (60, 60, 60))
    predni_levy_blinkr = Blinkr(np, 1)

    # inicializace, aby svetla byla vzdy na zacatku vypla
    predni_leve.vypni()
    predni_levy_blinkr.vypni()

    # chceme ziskat, aby predni_leve svetlo se rozvitilo, svitilo 1s,
    # pak zhaslo na 1s, pak se rozsvitilo atd...
    # do toho chceme aby predni blinkry blikaly s jejich frekvenci

    # pro predni svetlo jsme meli v DU4 takovouto smycku:
    # while not button_a.was_pressed():
    #    predni_leve.zapni()
    #    sleep(1000)
    #    predni_leve.vypni()
    #    sleep(1000)

    # nabizelo by se blinkr pridat takto:
    # while not button_a.was_pressed():
    #    predni_leve.zapni()
    #    predni_levy_blinkr.blikni()
    #    sleep(1000)
    #    predni_leve.vypni()
    #    sleep(1000)

    # ale sleep(1000) nam BLOKUJE celou exekuci a nedostali bychom
    # pozadavanou frekvenci blikni Blinkrem (ted 500ms)
    # musi tu while smycku predelat, abychom omezeli blokaci v case, tedy:
    cas_zapnuti = 0
    cas_vypnuti = 0

    while not button_a.was_pressed():
        # zapni pokud od vypnuti uplynulo vice nez 1000 ms
        if ticks_diff(ticks_ms(), cas_vypnuti) > 1000 and cas_zapnuti <= cas_vypnuti:
            predni_leve.zapni()
            cas_zapnuti = ticks_ms()
        # vypni pokud od vypnuti uplynulo vice nez 1000 ms
        if ticks_diff(ticks_ms(), cas_zapnuti) > 1000 and cas_vypnuti < cas_zapnuti :
            predni_leve.vypni()
            cas_vypnuti = ticks_ms()

        predni_levy_blinkr.blikni()
        sleep(50) # pouze kratka pauza, takze funkce se mohou vyhodnocovat casto, ale ne zbytecne prilis casto

