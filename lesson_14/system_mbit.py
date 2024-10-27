from microbit import button_a, button_b, display, i2c, pin1, pin2, pin8, pin12, pin14, pin15
from machine import time_pulse_us
from utime import ticks_us, ticks_diff, sleep

from system import System as SystemBase


class System(SystemBase):
    DRIVE_MODE_PICTOGRAMS = {
        ' ': [0b000, 0b000, 0b000],
        'TL': [0b000, 0b110, 0b010],  # sharp turn to left
        'TR': [0b000, 0b011, 0b010],  # sharp turn to right
        'IT': [0b000, 0b111, 0b010],  # intersection left-right (T)
        'IL': [0b010, 0b110, 0b010],  # intersection left-straight (T to left)
        'IR': [0b010, 0b011, 0b010],  # intersection right-straight (T to right)
        'IY': [0b101, 0b010, 0b010],  # split in the road (Y)
        'I+': [0b010, 0b111, 0b010],  # intersection all directions (+)
        '-': [0b000, 0b111, 0b000],
        '_': [0b000, 0b000, 0b111],
        '.': [0b000, 0b000, 0b010],
        '|': [0b010, 0b010, 0b010],
        '/': [0b001, 0b010, 0b100],
        '\\': [0b100, 0b010, 0b001],
        's': [0b011, 0b010, 0b110],
        'x': [0b101, 0b010, 0b101],
    }

    def __init__(self, i2c_freq=SystemBase.I2C_FREQ):
        super().__init__()
        i2c.init(freq=i2c_freq)
        print("System %s initialized, voltage %sV" % (self.get_system_type(), self.get_supply_voltage()))

    def get_system_type(self):
        return self.SYS_MBIT

    def ticks_us(self):
        return ticks_us()

    def ticks_diff(self, ticks1, ticks2):
        return ticks_diff(ticks1, ticks2)

    def sleep_us(self, us):
        sleep(us / 1_000_000)

    def i2c_read(self, addr: int, n: int) -> bytes:
        return i2c.read(addr, n)

    def i2c_write(self, addr: int, buf: bytes):
        i2c.write(addr, buf)

    def i2c_scan(self) -> list[int]:
        return i2c.scan()

    def pin_read_digital(self, pin):
        return pin.read_digital()

    def pin_write_digital(self, pin, value: int):
        pin.write_digital(value)

    def set_sonar_angle_pwm(self, angle_pwm: int):
        pin1.write_analog(angle_pwm)

    def get_sonar_echo_delay_us(self, timeout_us) -> int:
        self.pin_write_digital(pin8, 1)
        self.pin_write_digital(pin8, 0)
        return time_pulse_us(pin12, 1, timeout_us)

    def get_encoder_pin_left(self):
        return pin14

    def get_encoder_pin_right(self):
        return pin15

    def get_adc_value(self) -> int:
        return pin2.read_analog()

    def is_button_a_pressed(self):
        return button_a.is_pressed()

    def is_button_b_pressed(self):
        return button_b.is_pressed()

    def display_text(self, label):
        """Sets a label on the robot display (prints in log, displays the first letter on the screen)."""
        print("Label: %s" % label)
        display.show(label[0])

    def display_sensors(self, il, ir, ll, lc, lr, y=4, lb=9, ib=5):
        """Displays the sensors in top line of the display as pixels for each sensor.
        Line sensors (left, center, right) are far left, center, far right, lb is line brightness 0-9, default 9.
        IR sensors (left, right) are interlaced among them, ib is IR brightness 0-9, default 5."""
        display.set_pixel(4, y, lb if ll else 0)
        display.set_pixel(2, y, lb if lc else 0)
        display.set_pixel(0, y, lb if lr else 0)
        display.set_pixel(3, y, ib if il else 0)
        display.set_pixel(1, y, ib if ir else 0)

    def display_drive_mode(self, mode: str):
        """Displays the drive mode in the center (3x3 pixels), overriding choice, supporting
        all pictograms defined in DRIVE_MODE_PICTOGRAMS (other characters clear the area)."""
        lines = self.DRIVE_MODE_PICTOGRAMS[mode if mode in self.DRIVE_MODE_PICTOGRAMS else ' ']
        self.display_bitmap(1, 2, 3, lines)

    def display_choice(self, choice: str):
        """Displays the choice in the center (3x3 pixels), overriding drive mode, supporting
        all pictograms defined in DRIVE_MODE_PICTOGRAMS (other characters clear the area)."""
        self.display_drive_mode(choice)

    def get_drive_mode_symbol_keys(self):
        return list(self.DRIVE_MODE_PICTOGRAMS.keys())

    def display_speed(self, speed_now, speed_max, left: bool):
        """Displays the current speed on the display (represented as a 3-pixel bar) on the right side of display."""
        intensity = 3
        height_max = 4
        height = int(height_max * speed_now / speed_max)
        x_pos = 4 if left else 0
        for y in range(height_max):
            display.set_pixel(x_pos, y, intensity if y < height else 0)

    def display_bitmap(self, x_pos: int, y_pos: int, width: int, lines: list[int]):
        """Displays the bitmap on the display (0x0 = top left, max 5x5). Bitwise, each line int is right-aligned."""
        for y in range(len(lines)):
            for x in range(width):
                display.set_pixel(x_pos + x, 4 - (y_pos + y), 9 if lines[y] & (1 << x) else 0)

    def display_clear(self):
        """Clears the display."""
        display.clear()

    def display_on(self):
        """Enables the display."""
        display.on()
        display.clear()

    def display_off(self):
        """Disables the display."""
        display.off()
