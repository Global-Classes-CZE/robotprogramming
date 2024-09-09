WHITE_COLOR = (255, 255, 255)
SOFT_WHITE_COLOR = (60,60,60)
ORANGE_COLOR = (100, 35, 0)
BREAK_COLOR = (255, 0, 0)
RED_COLOR = (60, 0, 0)
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

class Light:
    def __init__(self, led_index, color, np):
        self.led_index = led_index
        self.color = color
        self.np = np

    def start_led(self):
        self.np[self.led_index] = self.color
        self.np.show()

    def stop_led(self):
        self.np[self.led_index] = OFF_COLOR
        self.np.show()

    def set_led_color(self, color):
        self.color = color
