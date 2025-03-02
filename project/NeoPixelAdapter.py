from neopixel import NeoPixel
from microbit import pin0


class NeoPixelAdapter:
    def __init__(self):
        self.np = NeoPixel(pin0, 8)

    def on(self, numbers, color):
        if isinstance(numbers, int):
            numbers = [numbers]
        for i in numbers:
            self.np[i] = color
        self.np.show()

    def off(self, numbers):
        self.on(numbers, (0, 0, 0))
