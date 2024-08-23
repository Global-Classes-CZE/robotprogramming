from Light import Light, Color

class Robot:
    def __init__(self):
        self.light = Light()

    def indikuj(self, smer_zataceni):
        if smer_zataceni == 'right':
            self.light.blink(Light.FRONT.RIGHT, Color.YELLOW)
            self.light.blink(Light.BACK.RIGHT, Color.YELLOW)
        else:
            self.light.blink(Light.FRONT.LEFT, Color.YELLOW)
            self.light.blink(Light.BACK.LEFT, Color.YELLOW)

    def zapni_svetla(self):
        self.light.on(Light.FRONT.BOTH, Color.WHITE)

    def brzdi(self):
        self.light.on(Light.BACK.BOTH, Color.RED)

    def vypni_svetla(self):
        self.light.off(Light.FRONT.BOTH)
        self.light.off(Light.BACK.BOTH)
