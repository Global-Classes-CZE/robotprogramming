from light import Light, led_map,SOFT_WHITE_COLOR, RED_COLOR,BREAK_COLOR, ORANGE_COLOR,OFF_COLOR,WHITE_COLOR 
from neopixel import NeoPixel
from microbit import pin0
from utime import ticks_ms, ticks_diff

class LightsController:
    def __init__(self):
        self.np = NeoPixel(pin0, 8)
        self.blinker_left_front = Light(led_map["LED_FRONT_LEFT_OUT"], ORANGE_COLOR, self.np)
        self.blinker_right_front = Light(led_map["LED_FRONT_RIGHT_OUT"], ORANGE_COLOR, self.np)
        self.blinker_left_rear = Light(led_map["LED_REAR_LEFT_OUT"], ORANGE_COLOR, self.np)
        self.blinker_right_rear = Light(led_map["LED_REAR_RIGHT_OUT"], ORANGE_COLOR, self.np)

        self.led_rear_left_in = Light(led_map["LED_REAR_LEFT_IN"], OFF_COLOR, self.np)
        self.led_rear_right_in = Light(led_map["LED_REAR_RIGHT_IN"], OFF_COLOR, self.np)

        self.led_front_left = Light(led_map["LED_FRONT_LEFT_IN"], SOFT_WHITE_COLOR, self.np)
        self.led_front_right = Light(led_map["LED_FRONT_RIGHT_IN"], SOFT_WHITE_COLOR, self.np)
        
        self.last_blink_time = ticks_ms()
        self.blinker_state = False
        self.left_color = None
        self.right_color = None  

    def indikuj(self, direction):
        current_time = ticks_ms()
        if ticks_diff(current_time, self.last_blink_time) >= 1000:
            if direction == "right":
                if self.blinker_state:
                    self.blinker_right_front.stop_led()
                    self.blinker_right_rear.stop_led()
                else:
                    self.blinker_right_front.start_led()
                    self.blinker_right_rear.start_led()
            elif direction == "left":
                if self.blinker_state:
                    self.blinker_left_front.stop_led()
                    self.blinker_left_rear.stop_led()
                else:
                    self.blinker_left_front.start_led()
                    self.blinker_left_rear.start_led()
            else:
                self.blinker_left_front.stop_led()
                self.blinker_left_rear.stop_led()

            self.blinker_state = not self.blinker_state
            self.last_blink_time = current_time

    def turn_on_lights(self):
        self.led_front_left.start_led()
        self.led_front_right.start_led()
        self.led_rear_left_in.set_led_color(RED_COLOR)
        self.led_rear_right_in.set_led_color(RED_COLOR)
        self.led_rear_right_in.start_led()
        self.led_rear_left_in.start_led()

    def start_breaking(self):
        self.left_color = self.led_rear_left_in.color
        self.right_color = self.led_rear_right_in.color
        
        self.led_rear_left_in.set_led_color(BREAK_COLOR)
        self.led_rear_right_in.set_led_color(BREAK_COLOR)
        self.led_rear_left_in.start_led()
        self.led_rear_right_in.start_led()

    def stop_breaking(self):
        if self.left_color and self.right_color:
            self.led_rear_left_in.set_led_color(self.left_color)
            self.led_rear_right_in.set_led_color(self.right_color)
            self.led_rear_left_in.start_led()
            self.led_rear_right_in.start_led()
        else:
            self.led_rear_left_in.set_led_color(OFF_COLOR)
            self.led_rear_right_in.set_led_color(OFF_COLOR)

    def start_reverse_light(self):
        self.left_color = self.led_rear_left_in.color
        self.led_rear_left_in.set_led_color(WHITE_COLOR)
        self.led_rear_left_in.start_led()

    def stop_reverse_light(self):
        if self.left_color:
            self.led_rear_left_in.set_led_color(self.left_color)
        else:
            self.led_rear_left_in.set_led_color(OFF_COLOR)

    def turn_off_lights(self):
        self.led_front_left.stop_led()
        self.led_front_right.stop_led()
        self.led_rear_left_in.stop_led()
        self.led_rear_right_in.stop_led()
