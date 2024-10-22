from NeoPixelAdapter import NeoPixelAdapter
from Period import Period


class LightController:
    __LED_FRONT_BLINKER_R = 0
    __LED_FRONT_R = 1
    __LED_FRONT_L = 2
    __LED_FRONT_BLINKER_L = 3
    __LED_BACK_BLINKER_L = 4
    __LED_BACK_L = 5
    __LED_BACK_R = 6
    __LED_BACK_BLINKER_R = 7

    def __init__(self):
        self.__neoPixel = NeoPixelAdapter()
        self.__period = Period(1000)
        self.__init()

    def __init(self):
        self.__neoPixel.off(range(0, 8))
        self.__neoPixel.on(range(0, 4), (200, 200, 200))

    def on(self, numbers, color):
        self.__neoPixel.on(numbers, color)
