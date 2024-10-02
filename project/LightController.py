from NeoPixelAdapter import NeoPixelAdapter

from utime import ticks_ms, ticks_diff


class LightController:
    __LED_FRONT_BLINKER_R = 0
    __LED_FRONT_R = 1
    __LED_FRONT_L = 2
    __LED_FRONT_BLINKER_L = 3
    __LED_BACK_BLINKER_L = 4
    __LED_BACK_L = 5
    __LED_BACK_R = 6
    __LED_BACK_BLINKER_R = 7

    __WHITE = (60, 60, 60)
    __WHITE_MAX = (255, 255, 255)
    __RED = (60, 0, 0)
    __RED_MAX = (255, 0, 0)
    __YELLOW = (247, 247, 1)
    __BLACK = (0, 0, 0)

    def __init__(self):
        self.neoPixel = NeoPixelAdapter()
        self.__init()

    def __init(self):
        self.neoPixel.off(range(0, 8))
