from  Led import Led
from  LedColor import LedColor
from microbit import sleep

class Lights:
    def __init__(self):
        self.headlights = (Led(1), Led(2))
        self.backlights = (Led(5), Led(6))    
    def lightsON(self):
        for x in self.headlights:
            x.on(LedColor.WHITE)
        for x in self.backlights:
            x.on(LedColor.RED)

    def lightsOFF(self):
        for x in self.headlights:
            x.off()
        for x in self.backlights:
            x.off()

    def lightsBreakON(self):
        for x in self.backlights:
            x.on(LedColor.RED_MAX)

    def lightsBreakOFF(self):
        for x in self.backlights:
            x.on(LedColor.RED)  

lights = Lights()
while True:
    lights.lightsON()  #Light on
    sleep(1000)
    lights.lightsBreakON()  #Brake light on
    sleep(1000)
    lights.lightsBreakOFF()  #Brake light off
    sleep(1000)
    lights.lightsOFF()  #Light off
    sleep(1000)