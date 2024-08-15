from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

class Color:
    BLACK = ( 0, 0, 0 )
    RED = ( 255, 0, 0 )
    GREEN = ( 60, 179, 113 )
    YELLOW = ( 255, 165, 0 )
    BLUE = ( 0, 0, 255 )
    WHITE = ( 255, 255, 255 )

ON_TIME = 500
OFF_TIME = 250

LIGHT_FRONT_LEFT = [0,1]
LIGHT_FRONT_RIGHT = [2,3]
LIGHT_FRONT = [0,1,2,3]
LIGHT_BACK_LEFT = [4,5]
LIGHT_BACK_RIGHT = [6,7]
LIGHT_BACK = [4,5,6,7]
LIGHT_ALL = [0,1,2,3,4,5,6,7]

ANIMATION_SEQ = [
    [LIGHT_FRONT, Color.WHITE],
    [LIGHT_BACK, Color.RED],
    [LIGHT_FRONT_LEFT, Color.GREEN],
    [LIGHT_FRONT_RIGHT, Color.GREEN],
    [LIGHT_BACK_RIGHT, Color.GREEN],
    [LIGHT_BACK_LEFT, Color.GREEN],
]

def zapni(poradi_led, barva):
    for x in poradi_led:
        np[x] = barva
    np.write()

def vypni(poradi_led):
    zapni(poradi_led, Color.BLACK)

# nie uplne rozumiem tejto vyznamu tejto metody
# def nastav_barvu(poradi_led, barva):
    #TODO

np = NeoPixel(pin0,8)

while True:
    for [poradi_led, barva] in ANIMATION_SEQ:
        zapni(poradi_led, barva)
        sleep(ON_TIME)
        vypni(poradi_led)
        sleep(OFF_TIME)

    # wait longer before restarting animation
    sleep(5000)

