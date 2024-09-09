from microbit import sleep
from Light import Light, Color

light = Light()

def lightsON():
    light.on(Light.FRONT.BOTH, Color.WHITE_50)
    light.on(Light.BACK.BOTH, Color.RED_50)

def lightsOFF():
    light.off(Light.FRONT.BOTH)
    light.off(Light.BACK.BOTH)

def lightsBreakON():
    light.on(Light.BACK.BOTH, Color.RED_100)

def lightsBreakOFF():
    light.off(Light.BACK.BOTH)

def lightsBackON():
    light.on(Light.BACK.BOTH, Color.WHITE_50)

def lightsBackOFF():
    light.off(Light.BACK.BOTH)

def lightsIndicator(direction):
    light.blink(direction, Color.YELLOW, 2500)

while True:
    # Application example
    lightsON()  #Light on
    sleep(1000)
    lightsBreakON()  #Brake light on
    sleep(1000)
    lightsBreakOFF()  #Brake light off
    sleep(1000)
    lightsBackON()  #Reversing lights on
    sleep(1000)
    lightsBackOFF()  #Reversing lights off
    sleep(1000)
    lightsOFF()  #Light off
    sleep(1000)
    lightsIndicator(Light.FRONT.LEFT)
    sleep(1000)
    lightsIndicator(Light.BACK.LEFT)
    sleep(1000)
