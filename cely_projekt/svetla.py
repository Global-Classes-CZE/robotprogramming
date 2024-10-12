class Svetlo:
    def __init__(self, poradi_led, neopixel_pole, barva):
        self.poradi = poradi_led
        self.barva = barva
        self.np = neopixel_pole

    def zapni(self):
        self.nastav_barvu(self.barva)
        self.np.write()

    def vypni(self):
        self.nastav_barvu((0, 0, 0))  #nastavim ledku na dane pozici na cernou (RGB hodnoty)
        self.np.write()

    def nastav_barvu(self, barva):
        self.np[self.poradi] = barva  #nastavim ledku na dane pozici na zadanou barvu (RGB hodnoty)

class PredniSvetlo(Svetlo):
    def __init__(self, poradi_led, neopixel):
        super().__init__(poradi_led, neopixel, (60, 60, 60))
        self.vypni()

    def zapni_dalkove(self):
        self.nastav_barvu((255, 255, 255))
        self.np.write()

class Blinkr(Svetlo):
    def __init__(self, poradi_led, neopixel):
        super().__init__(poradi_led, neopixel, (100, 35, 0))
        self.cas_minule = ticks_us()
        self.perioda_blikani = 500000  # cas v us
        self.vypni()
        self.zapnuto = False

    def blikej(self):
        cas_ted = ticks_us()
        kolik_ubehlo_od_minula = ticks_diff(cas_ted, self.cas_minule)

        if kolik_ubehlo_od_minula > self.perioda_blikani:
            # bliknuti znamena zmenit stav - kdyz je ledka zapla, tak ji chceme vypnout
            if self.zapnuto:
                self.vypni()
                self.zapnuto = False
            else:
                self.zapni()
                self.zapnuto = True

            self.cas_minule = cas_ted

class ZadniSvetlo(Svetlo):
    def __init__(self, poradi_led, neopixel):
        super().__init__(poradi_led, neopixel, (60, 0, 0))
        self.vypni()

    def zapni_brzdove(self):
        self.nastav_barvu(poradi_led, (255, 0, 0))
        self.np.write()

class ZpatecniSvetlo(ZadniSvetlo):
    def __init__(self, poradi_led, neopixel):
        super().__init__(poradi_led, neopixel)

    def zapni_zpatecni(self):
        self.nastav_barvu(poradi_led, (60, 60, 60))
        self.np.write()

class SvetelnyModul:

    def __init__(self):
        neopixel = NeoPixel(pin0, 8)

        self.predni_svetla = []
        self.predni_svetla.append(PredniSvetlo(0, neopixel))
        self.predni_svetla.append(PredniSvetlo(3, neopixel))

        self.zadni_svetlo = ZadniSvetlo(6, neopixel)
        self.zpatecni_svetlo = ZpatecniSvetlo(5, neopixel)

        self.blinkry = []
        self.blinkry.append(Blinkr(1, neopixel))
        self.blinkry.append(Blinkr(2, neopixel))
        self.blinkry.append(Blinkr(4, neopixel))
        self.blinkry.append(Blinkr(7, neopixel))

    def zapni_obrysova(self):
        for svetlo in self.predni_svetla:
            svetlo.zapni()

        self.zadni_svetlo.zapni()
        self.zpatecni_svetlo.zapni()

    def vypni_obrysova(self):
        for svetlo in self.predni_svetla:
            svetlo.vypni()

        self.zadni_svetlo.vypni()
        self.zpatecni_svetlo.vypni()

    def zapni_zpatecni(self):
        self.zpatecni_svetlo.zapni_zpatecni()

    def vypni_zpatecni(self):
        self.zadni_svetlo.vypni()

    def zapni_brzdova(self):
        self.zadni_svetlo.zapni_brzdove()
        self.zpatecni_svetlo.zapni_brzdove()

    def vypni_brzdova(self):
        self.zadni_svetlo.vypni()
        self.zpatecni_svetlo.vypni()

    def blinkry_blikej(self, smer):

        if smer == K.LEVY:
            self.blinkry[0].blikej()
            self.blinkry[2].blikej()
        elif smer == K.PRAVY:
            self.blinkry[1].blikej()
            self.blinkry[3].blikej()
        elif smer == K.VSE:
            self.blinkry[0].blikej()
            self.blinkry[2].blikej()
            self.blinkry[1].blikej()
            self.blinkry[3].blikej()

    def vypni_blinkry(self):
        self.blinkry[0].vypni()
        self.blinkry[2].vypni()
        self.blinkry[1].vypni()
        self.blinkry[3].vypni()
