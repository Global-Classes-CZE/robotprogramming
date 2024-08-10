from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

np = NeoPixel(pin0,8)
while True:
    np[0] = (255,255,255) # nastavim prvni ledku, tzn [0] na bilou (RGB hodnoty)
    np.write()
    sleep(1000)
    np[0] = (0,0,0) # nastavim prvni ledku, tzn [0] na cernou (RGB hodnoty)
    np.write()
    sleep(1000)

