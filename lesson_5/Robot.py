from light import led_map, Light, OFF_COLOR, ORANGE_COLOR, WHITE_COLOR, RED_COLOR, BREAK_COLOR
from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

class Robot:
    def __init__(self):
        self.np = NeoPixel(pin0, 8)
        self.blinker_left_front = Light(led_map["LED_FRONT_LEFT_OUT"], ORANGE_COLOR, self.np)
        self.blinker_right_front = Light(led_map["LED_FRONT_RIGHT_OUT"], ORANGE_COLOR, self.np)
        self.blinker_left_rear = Light(led_map["LED_REAR_LEFT_OUT"], ORANGE_COLOR, self.np)
        self.blinker_right_rear = Light(led_map["LED_REAR_RIGHT_OUT"], ORANGE_COLOR, self.np)

        self.led_rear_left_in = Light(led_map["LED_REAR_LEFT_IN"], OFF_COLOR, self.np)
        self.led_rear_right_in = Light(led_map["LED_REAR_RIGHT_IN"], OFF_COLOR, self.np)

        self.led_front_left = Light(led_map["LED_FRONT_LEFT_IN"], WHITE_COLOR, self.np)
        self.led_front_right = Light(led_map["LED_FRONT_RIGHT_IN"], WHITE_COLOR, self.np)


    def indikuj(self, direction):
        if(direction=="right"):
            self.blinker_right_front.start_led()
            self.blinker_right_rear.start_led()
            sleep(1000)
            self.blinker_right_front.stop_led()
            self.blinker_right_rear.stop_led()
            sleep(1000)
        elif(direction=="left"):
            self.blinker_left_front.start_led()
            self.blinker_left_rear.start_led()
            sleep(1000)
            self.blinker_left_front.stop_led()
            self.blinker_left_rear.stop_led()
            sleep(1000)
        else:
            self.blinker_left_front.stop_led()
            self.blinker_left_rear.stop_led()
            

    def turn_on_lights(self):
        self.led_front_left.start_led()
        self.led_front_right.start_led()
        self.led_rear_left_in.set_led_color(RED_COLOR)
        self.led_rear_right_in.set_led_color(RED_COLOR)
        self.led_rear_right_in.start_led()
        self.led_rear_left_in.start_led()

    def breaking(self):
        left_color = self.led_rear_left_in.color
        right_color = self.led_rear_right_in.color
        self.led_rear_left_in.set_led_color(BREAK_COLOR)
        self.led_rear_right_in.set_led_color(BREAK_COLOR)
        self.led_rear_left_in.start_led()
        self.led_rear_right_in.start_led()
        sleep(1000)
        self.led_rear_left_in.set_led_color(left_color)
        self.led_rear_right_in.set_led_color(right_color)
        self.led_rear_left_in.start_led()
        self.led_rear_right_in.start_led()

    def turn_off_lights(self):
        self.led_front_left.stop_led()
        self.led_front_right.stop_led()
        self.led_rear_left_in.stop_led()
        self.led_rear_right_in.stop_led()

