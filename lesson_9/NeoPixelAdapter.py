from neopixel import NeoPixel
from microbit import pin0

class NeoPixelAdapter:
    __np = None
    def __init__(self):
        if(NeoPixelAdapter.__np == None):
            NeoPixelAdapter.__np = NeoPixel(pin0, 8)

    def on(self, number, color):
        NeoPixelAdapter.__np[number] = color
        NeoPixelAdapter.__np.write()

    def onAll(self, color):
        for key, value in enumerate(NeoPixelAdapter.__np):
            NeoPixelAdapter.__np[key] = color
        NeoPixelAdapter.__np.write()

    def off(self, number):
        NeoPixelAdapter.__np[number] = (0, 0, 0)
        NeoPixelAdapter.__np.write()

    def offAll(self):
        for key, value in enumerate(NeoPixelAdapter.__np):
            NeoPixelAdapter.__np[key] = (0, 0, 0)
        NeoPixelAdapter.__np.write()
