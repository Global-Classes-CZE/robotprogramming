from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

WHITE_COLOR = (255, 255, 255)
OFF_COLOR = (0, 0, 0)

led_map = {
    "LED_FRONT_LEFT_IN": 0,
    "LED_FRONT_LEFT_OUT": 1,
    "LED_FRONT_RIGHT_OUT": 2,
    "LED_FRONT_RIGHT_IN": 3,
    "LED_REAR_RIGHT_IN": 4,
    "LED_REAR_RIGHT_OUT": 5,
    "LED_REAR_LEFT_OUT": 6,
    "LED_REAR_LEFT_IN": 7
}

np = NeoPixel(pin0, 8)
led_index = led_map.get("LED_REAR_RIGHT_OUT")

def start_led(led_index):
    set_led_color(led_index, WHITE_COLOR)

def stop_led(led_index):
    set_led_color(led_index, OFF_COLOR)

def set_led_color(led_index, color):
    np[led_index] = color
    np.write()

while True:
    if led_index is not None:
        start_led(led_index)
        sleep(1000)
        stop_led(led_index)
        sleep(1000)
    else:
        print("Invalid LED name")

