from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from datetime import datetime

ON_TIME = 500
OFF_TIME = 500

# ALL = [0,1,2,3,4,5,6,7]
class Front:
    BOTH=[0,1,2,3]
    LEFT = [0,1]
    RIGHT = [2,3]

class Back:
    LEFT = [4,5]
    RIGHT = [6,7]
    BACK = [4,5,6,7]

class Color:
    BLACK = ( 0, 0, 0 )
    RED = ( 255, 0, 0 )
    GREEN = ( 60, 179, 113 )
    YELLOW = ( 255, 165, 0 )
    BLUE = ( 0, 0, 255 )
    WHITE = ( 255, 255, 255 )

class Light:

    FRONT = Front()
    BACK = Front()

    def __init__(self):
        self.np = NeoPixel(pin0, 8)

    def on(self, poradi_led, barva):
        for x in poradi_led:
            self.np[x] = barva
        self.np.write()

    def off(self, poradi_led):
        self.on(poradi_led, Color.BLACK)

    def blink(self, poradi_led, barva, duration):
        start=datetime.now()
        while not duration or (datetime.now() - start < duration):
            self.on(poradi_led, barva)
            sleep(ON_TIME)
            self.off(poradi_led)
            sleep(OFF_TIME)
