from light import Light, led_map, WHITE_COLOR  # Import WHITE_COLOR here
from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

class Main:
    def __init__(self):
        self.np = NeoPixel(pin0, 8)
        self.light_left_front = Light(led_map["LED_FRONT_LEFT_IN"], WHITE_COLOR, self.np)

    def run(self):
        while True:
            self.light_left_front.start_led()
            sleep(1000)
            self.light_left_front.stop_led()
            sleep(1000)
        

if __name__ == "__main__":
    main = Main()
    main.run()
