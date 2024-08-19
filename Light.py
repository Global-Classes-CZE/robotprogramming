from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from microbit import button_a
import random

class Light:    
    # Static utility maps
    # Define the basic RGB triples
    color_to_rgb = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "gray": (128, 128, 128),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "brown": (165, 42, 42),
    }
    
    def __init__(self, id, name, physical_led, ledController):
        """
        Initializes the Light object.
        
        :param id: The ID of the LED.
        :param name: The name of the LED for logging purposes.
        :param physical_led: an object controlling the actual hardware.
        """
        self.id = id
        self.name = name
        self.physical_led = physical_led
        self.color = "black"  # Default to black (off)
        self.ledController = ledController
    
    def setLight(self, colorCode):
        self.ledController[self.id] = colorCode
        self.ledController.write()
        
    def switch_on(self):
        print("LED " + self.name + " is now ON with color " + str(self.color))
        self.setLight(self.color_to_rgb.get(self.color))

    def switch_off(self):
        print("LED " + self.name + " is now ON with color black")
        self.setLight(self.color_to_rgb.get("black"))
        
    def set_color(self, color):
        if color.lower() in Light.color_to_rgb.keys():
            self.color = color
            print("LED " + str(self.name) + " set to color " + str(color) + " with RGB value " + str(self.color_to_rgb.get(color)))
        else:
            print("Color " + str(color) + " is not recognized.")
        
        
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
    disco()
