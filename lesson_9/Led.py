from NeoPixelAdapter import NeoPixelAdapter

class Led:
    def __init__(self, number):
        self.npa = NeoPixelAdapter()
        self.number = number

    def on(self, color):
        self.npa.on(self.number, color)

    def off(self):
        self.npa.off(self.number)

