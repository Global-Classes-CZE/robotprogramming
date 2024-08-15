from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep
from microbit import button_a
import random

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

# Define the basic RGB triples
led_color_setup = {
    0: "magenta",
    1: "magenta",
    2: "green",
    3: "green",
    4: "yellow",
    5: "yellow",
    6: "orange",
    7: "orange"
}

def get_rgb(color_name):
    color_name = color_name.lower()
     # Return the RGB value if the color name exists in the dictionary
    if color_name in color_to_rgb:
        return color_to_rgb[color_name]
    else:
        raise Exception("an error occurred", "color not found", -1)

def zapni(np, poradi_led):
    print(">> switching on led#" + str(poradi_led) + " " + str(color_to_rgb.get(led_color_setup.get(poradi_led))))
    np[poradi_led] = color_to_rgb.get(led_color_setup.get(poradi_led))
    np.write()

def vypni(np, poradi_led):
    print(">> switching off led#" + str(poradi_led))
    nastav_barvu(poradi_led, "black")
    zapni(np, poradi_led)

def nastav_barvu(poradi_led, barva):
    print(">>> setting new color" + barva + " to " + str(poradi_led))
    led_color_setup.update({poradi_led: barva})

def disco():
    np = NeoPixel(pin0, 8)

    while not button_a.is_pressed():
        for i in range(8):
            random_color = "white"
            print(str(color_to_rgb.keys()))
            random_color = random.choice(list(color_to_rgb.keys()))
            print(random_color)

            nastav_barvu(i, random_color)
            zapni(np, i)
            sleep(1000)

    for i in range(8):
        vypni(np, i)

    print("> disco program ended")

if __name__ == "__main__":
    disco()
