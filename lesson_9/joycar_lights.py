from microbit import sleep
from utime import ticks_ms, ticks_diff
from light_placement import LightPlacement
from light_driver import LightDriver


lights = LightDriver()

def lightsON():
    lights.head_on()
    lights.back_on()
    lights.update()

def lightsOFF():
    lights.head_off()
    lights.back_off()
    lights.update()

def lightsBreakON():
    lights.brake_on()
    lights.update()

def lightsBreakOFF():
    lights.brake_off()
    lights.update()

def lightsBackON():
    lights.reverse_on()
    lights.update()

def lightsBackOFF():
    lights.reverse_off()
    lights.update()

def lightsIndicatorON(direction):
    lights.blink(direction, 400)
    lights.update()

def lightsIndicatorOFF(direction):
    lights.blink_off()
    lights.update()

if __name__ == "__main__":
    # Application example
    print("lightsON")
    lightsON()       # Light on
    sleep(5000)
    print("lightsBreakON")
    lightsBreakON()  # Brake light on
    sleep(5000)
    print("lightsBreakOFF")
    lightsBreakOFF()  # Brake light off
    sleep(5000)
    print("lightsBackON")
    lightsBackON()  # Reversing lights on
    sleep(5000)
    print("lightsBackOFF")
    lightsBackOFF()  # Reversing lights off
    sleep(5000)
    start_time = ticks_ms()
    print("lightIndicatorON")
    lightsIndicatorON(LightPlacement.LEFT_DIRECTION)  # Left indicator on
    while ticks_diff(ticks_ms(), start_time) < 5000:
        lights.update()
        sleep(0.01)
    print("lightIndicatorOFF")
    lightsIndicatorOFF(LightPlacement.LEFT_DIRECTION)  # Left indicator off
    sleep(5000)
    start_time = ticks_ms()
    print("lightEmergencyON")
    lights.blink_emergency(200)  # Emergency indicator, super fast
    while ticks_diff(ticks_ms(), start_time) < 5000:
        lights.update()
        sleep(0.01)
    print("lightBlinkOFF")
    lights.blink_off()
    sleep(5000)
    lightsIndicatorOFF(LightPlacement.LEFT_DIRECTION)  # Left indicator off
    print("lightsOFF")
    lightsOFF()  # Light off
