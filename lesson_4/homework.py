from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

def nastav_barvu(poradi_led, barva):
    np[poradi_led] = (barva)
    np.write()
    
def zapni(poradi_led):
    nastav_barvu(poradi_led, (255,255,255))
    
def vypni(poradi_led):
    nastav_barvu(poradi_led, (0,0,0))

#jen tak pro legraci    
def pr_blinkr():   
    nastav_barvu(2, (255, 100, 0))
    sleep(250)
    vypni(2)
    sleep(250)

np = NeoPixel(pin0,8)
while True:
    zapni(0)
    sleep(1000)
    vypni(0)
    sleep(1000)
    pr_blinkr() #jen tak pro legraci