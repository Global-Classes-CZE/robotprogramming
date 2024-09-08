from microbit import *
import neopixel
from utime import ticks_ms, ticks_diff


np = neopixel.NeoPixel(pin0, 8)
headlights = (0, 3)
backlights = (5, 6)
led_white = (60, 60, 60)
led_red = (60, 0, 0)
led_off = (0, 0, 0)
led_red_br = (255, 0, 0)
led_orange = (100, 35, 0)
indicator_left = (1, 4)
indicator_right = (2, 7)
indicator_warning = (1, 2, 4, 7)


def lightsON():
    for x in headlights:
        np[x] = led_white
    for x in backlights:
        np[x] = led_red
    np.show()

def lightsOFF():
    for x in headlights:
        np[x] = led_off
    for x in backlights:
        np[x] = led_off
    np.show()

def lightsBreakON():
    temp = np[backlights[1]]
    for x in backlights:
        np[x] = led_red_br
    np.show()
    return (temp)

def lightsBreakOFF():
    for x in backlights:
        np[x] = led_off
    np.show()

def lightsBackON():
    temp = np[backlights[0]]
    np[backlights[0]] = led_white
    np.show()
    return (temp)

def lightsBackOFF():
    np[backlights[0]] = led_off
    np.show()

def lightsIndicator(direction, last_ind_act):
    if ticks_diff(ticks_ms(), last_ind_act) >= 400 and np[direction[0]] == led_off:
        for x in direction:
            np[x] = led_orange
        np.show()
        return ticks_ms()
    elif ticks_diff(ticks_ms(), last_ind_act) >= 400 and np[direction[0]] == led_orange:
        for x in direction:
            np[x] = led_off
        np.show()
        return ticks_ms()
    else:
        return last_ind_act

while True:
    # Application example
    print("lightsON")
    lightsON()  # Light on
    sleep(1000)
    print("lightsBreakON")
    lightsBreakON()  # Brake light on
    sleep(1000)
    print("lightsBreakOFF")
    lightsBreakOFF()  # Brake light off
    sleep(1000)
    print("lightsBackON")
    lightsBackON()  # Reversing lights on
    sleep(1000)
    print("lightsBackOFF")
    lightsBackOFF()  # Reversing lights off
    sleep(1000)
    print("lightsOFF")
    lightsOFF()  # Light off
    sleep(1000)
