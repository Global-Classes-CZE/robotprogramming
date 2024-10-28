from time import monotonic_ns, sleep

from analogio import AnalogIn
from board import P1, P2, P8, P12, P14, P15
from digitalio import DigitalInOut, Direction
from picoed import i2c, display, button_a, button_b
from pulseio import PulseIn
from pwmio import PWMOut

from system import System as SystemBase


class System(SystemBase):
    """Pico:Ed implementation of the System class.
    The Pico:Ed board (I2C, pins, buttons, display) use library at https://github.com/elecfreaks/circuitpython_picoed.
    Display uses IS31FL3731 library at https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3731.
    Light uses NeoPixel library at https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel.
    Sonar code is inspired by HC-SR04 library at https://github.com/adafruit/Adafruit_CircuitPython_HCSR04."""

    DRIVE_MODE_PICTOGRAMS = {
        ' ': [0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
        'TL': [0b00000, 0b00000, 0b11100, 0b00100, 0b00100],  # sharp turn to left
        'TR': [0b00000, 0b00000, 0b00111, 0b00100, 0b00100],  # sharp turn to right
        'IT': [0b00000, 0b00000, 0b11111, 0b00100, 0b00100],  # intersection left-right (T)
        'IL': [0b00100, 0b00100, 0b11100, 0b00100, 0b00100],  # intersection left-straight (T to left)
        'IR': [0b00100, 0b00100, 0b00111, 0b00100, 0b00100],  # intersection right-straight (T to right)
        'IY': [0b10001, 0b01010, 0b00100, 0b00100, 0b00100],  # split in the road (Y)
        'I+': [0b00100, 0b00100, 0b11111, 0b00100, 0b00100],  # intersection all directions (+)
        '<': [0b00010, 0b00100, 0b01111, 0b00100, 0b00010],  # interactive choice left
        '^': [0b00000, 0b00100, 0b01110, 0b10101, 0b00100],  # interactive choice forward
        '>': [0b00100, 0b00010, 0b01111, 0b00010, 0b00100],  # interactive choice right
        '-': [0b00000, 0b00000, 0b11111, 0b00000, 0b00000],
        '_': [0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
        '.': [0b00000, 0b00000, 0b00000, 0b00000, 0b00100],
        '|': [0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
        '/': [0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
        '\\': [0b10000, 0b01000, 0b00100, 0b00010, 0b00001],
        's': [0b00111, 0b01000, 0b01110, 0b00010, 0b11100],
        'x': [0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    }

    def __init__(self):
        super().__init__()
        # Sonar servo
        self.pin1 = PWMOut(P1, frequency=100)
        # ADC
        self.pin2 = AnalogIn(P2)
        # Sonar trigger
        self.pin8 = DigitalInOut(P8)
        self.pin8.direction = Direction.OUTPUT
        # Sonar echo
        self.pin12 = PulseIn(P12)
        # Encoder left
        self.pin14 = DigitalInOut(P14)
        self.pin14.direction = Direction.INPUT
        # Encoder right
        self.pin15 = DigitalInOut(P15)
        self.pin15.direction = Direction.INPUT
        print("System %s initialized, voltage %sV" % (self.get_system_type(), self.get_supply_voltage()))

    def get_system_type(self):
        return self.SYS_PICO

    def ticks_us(self):
        return monotonic_ns() // 1000

    def ticks_diff(self, ticks1, ticks2):
        return abs(ticks1 - ticks2)

    def sleep_us(self, us):
        sleep(us / 1_000_000)

    def i2c_scan(self) -> list[int]:
        while not i2c.try_lock():
            pass
        ret = i2c.scan()
        i2c.unlock()
        return ret

    def i2c_read(self, addr: int, n: int) -> bytes:
        while not i2c.try_lock():
            pass
        buffer = bytearray(n)
        i2c.readfrom_into(addr, buffer, start=0, end=n)
        i2c.unlock()
        return buffer

    def i2c_write(self, addr: int, buf: bytes):
        while not i2c.try_lock():
            pass
        i2c.writeto(addr, buf)
        i2c.unlock()

    def pin_read_digital(self, pin):
        return 1 if pin.value else 0

    def pin_write_digital(self, pin, value: int):
        pin.value = value != 1

    def set_sonar_angle_pwm(self, angle_pwm: int):
        scaled_value = int((angle_pwm / 128) * 16384)
        self.pin1.duty_cycle = scaled_value

    def get_sonar_echo_delay_us(self, timeout_us) -> int:
        # Trigger the sonar w/ 10ms pulse
        self.pin8.value = True
        self.sleep_us(10)
        self.pin8.value = False

        self.pin12.clear()
        self.pin12.resume()
        start_time = monotonic_ns()
        while not self.pin12:
            if (monotonic_ns() - start_time) > timeout_us * 1000:
                self.pin12.pause()
                return -1
        self.pin12.pause()
        return self.pin12[0] if len(self.pin12) > 0 else -1

    def get_encoder_pin_left(self):
        return self.pin14

    def get_encoder_pin_right(self):
        return self.pin15

    def get_adc_value(self) -> int:
        # scale ADC value to 10-bit value as expected by the caller
        return self.pin2.value * 1024 // 16384

    def is_button_a_pressed(self):
        return button_a.is_pressed()

    def is_button_b_pressed(self):
        return button_b.is_pressed()

    def display_text(self, label):
        print("Label: %s" % label)
        display.scroll(label[0:3])

    def display_sensors(self, il, ir, ll, lc, lr, y=6, lb=32, ib=3):
        """Displays the sensors in top line of the display as pixels for each sensor.
        Line sensors (left, center, right) are far left, center, far right, lb is line brightness 0-9, default 9.
        IR sensors (left, right) are interlaced among them, ib is IR brightness 0-9, default 5."""
        x_pos = 4
        stretch = 2
        display.pixel(x_pos + 4 * stretch, y, lb if ll else 0)
        display.pixel(x_pos + 2 * stretch, y, lb if lc else 0)
        display.pixel(x_pos + 0 * stretch, y, lb if lr else 0)
        display.pixel(x_pos + 3 * stretch, y, ib if il else 0)
        display.pixel(x_pos + 1 * stretch, y, ib if ir else 0)

    def display_drive_mode(self, mode: str):
        """Displays the drive mode in the display center (5x5 pixels), supporting
        all pictograms defined in DRIVE_MODE_PICTOGRAMS (other characters clear the area)."""
        lines = self.DRIVE_MODE_PICTOGRAMS[mode if mode in self.DRIVE_MODE_PICTOGRAMS else ' ']
        self.display_bitmap(6, 0, 5, lines)

    def display_choice(self, choice: str):
        """Displays the choice next to the drive mode (5x5 pixels), supporting
        all pictograms defined in DRIVE_MODE_PICTOGRAMS (other characters clear the area)."""
        lines = self.DRIVE_MODE_PICTOGRAMS[choice if choice in self.DRIVE_MODE_PICTOGRAMS else ' ']
        self.display_bitmap(1, 0, 5, lines)

    def get_drive_mode_symbol_keys(self):
        return list(self.DRIVE_MODE_PICTOGRAMS.keys())

    def display_speed(self, speed_now, speed_max, left: bool):
        """Displays the current speed as a horizontal bar on the left or right of the display."""
        intensity = 2
        height_max = 7
        height = int(height_max * speed_now / speed_max)
        x_pos = 16 if left else 0
        for y in range(height_max):
            display.pixel(x_pos, y, intensity if y < height else 0)

    def display_bitmap(self, x_pos: int, y_pos: int, width: int, lines: list[int]):
        for y in range(len(lines)):
            for x in range(width):
                display.pixel(x_pos + width - x - 1, y_pos + width - y - 1, 9 if lines[y] & (1 << (width - x - 1)) else 0)

    def display_clear(self):
        display.fill(0)

    def display_on(self):
        pass

    def display_off(self):
        self.display_clear()
