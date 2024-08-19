from Light import Light
from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from microbit import button_a
import random

class Robot:
    directionLightColor = "orange"
    brakeLightColor = "red"
    beamLightColor = "white"
    
    def __init__(self, left_blinkers, right_blinkers, front_leds, back_leds):
        self.left_blinkers = left_blinkers
        self.right_blinkers = right_blinkers
        self.front_leds = front_leds
        self.back_leds = back_leds
        
    # Simulate blinking effect
    def blink(self, leds):
        blinkLength = 1000
        blinkPause = 900
        
        for i in range (0, 3):
            for l in leds:
                l.switch_on()
                
            sleep(blinkLength)
            
            for l in leds:
                l.switch_off()
                
            sleep(blinkPause)
            
        
    def turn(self, direction):
        if direction.lower() == "left":
            print("Turning left...")
            for led in self.left_blinkers:
                led.set_color(self.directionLightColor)
                
            self.blink(self.left_blinkers)
        elif direction.lower() == "right":
            print("Turning right...")
            for led in self.right_blinkers:
                led.set_color(self.directionLightColor)
            
            self.blink(self.right_blinkers)
        else:
            print("Invalid direction. Use 'Left' or 'Right'.")
    
    def turn_beams_on(self):
        print("Turning front beams on...")
        for led in self.front_leds:
            led.set_color(self.beamLightColor)
            led.switch_on()
    
    def turn_beams_off(self):
        print("Turning front beams off...")
        for led in self.front_leds:
            led.switch_off()
    
    def brakeNotificationOn(self):
        print("Braking... Turning on red lights in the back.")
        for led in self.back_leds:
            led.set_color(self.brakeLightColor)
            led.switch_on()
    
    def brakeNotificationOff(self):
        print("Stopping brake notification...")
        for led in self.back_leds:
            led.switch_off()

    def stop(self):
        self.brakeNotificationOn()
        sleep(1000)
        self.brakeNotificationOff()
    
def test():
    np = NeoPixel(pin0, 8)
    num_leds = 8
        
    leds = [Light(i, "LED-" + str(i), np[i], np) for i in range(num_leds)]
    
    left_blinkers = [leds[1], leds[4]]
    right_blinkers= [leds[2], leds[5]]
    front_leds = [leds[0], leds[3]]
    back_leds = [leds[4], leds[5], leds[6], leds[7]]
    
    robot = Robot(left_blinkers, right_blinkers, front_leds, back_leds)
    
    while not button_a.is_pressed():
        robot.turn("left")
        sleep(1000) 
        robot.turn("right")
        sleep(1000) 
        robot.turn_beams_on()
        sleep(1000 * 2) 
        robot.turn_beams_off()
        sleep(1000)
        robot.stop()
    
    for led in leds:
        led.switch_off()
    
    print("> Robot program ended")
    
          
def disco():
    np = NeoPixel(pin0, 8)
    num_leds = 8
    leds = [Light(i, "LED-" + str(i), np[i], np) for i in range(num_leds)]
    
    while not button_a.is_pressed():
        for l in leds:
            random_color = random.choice(list(Light.color_to_rgb.keys()))            
            l.set_color(random_color)
            l.switch_on()
            sleep(1000)
            
    for l in leds:
        l.switch_on

    print("> disco program ended")


if __name__ == "__main__":
    test()
#    disco()

