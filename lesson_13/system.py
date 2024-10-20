from microbit import i2c, pin2, display


class System:
    I2C_ADDRESS = 0x70
    I2C_FREQ = 100_000
    I2C_SENSOR_DEVICE = 0x38

    MASK_LINE_LEFT = 0x04
    MASK_LINE_CENTER = 0x08
    MASK_LINE_RIGHT = 0x10
    MASK_IR_LEFT = 0x20
    MASK_IR_RIGHT = 0x40

    DRIVE_MODE_PICTOGRAMS = {
        ' ': [0b000, 0b000, 0b000],
        'T': [0b000, 0b111, 0b010],
        'Y': [0b101, 0b010, 0b010],
        '+': [0b010, 0b111, 0b010],
        '-': [0b000, 0b111, 0b000],
        '|': [0b010, 0b010, 0b010],
        '/': [0b000, 0b011, 0b010],
        '\\': [0b000, 0b110, 0b010],
        '.': [0b000, 0b000, 0b010],
        's': [0b010, 0b101, 0b010],
        'x': [0b101, 0b010, 0b101],
    }

    def __init__(self, i2c_freq=I2C_FREQ, voltage_pin=pin2):
        self.voltage_pin = voltage_pin
        i2c.init(freq=i2c_freq)

    def i2c_write(self, data):
        i2c.write(self.I2C_ADDRESS, data)

    def i2c_read_sensors(self):
        """Returns the current sensor data byte."""
        return i2c.read(self.I2C_SENSOR_DEVICE, 1)[0]

    def get_sensors(self):
        """Checks if line sensors (left, center, right, ) detected a line (true if line is present)
        or obstacle sensors (, left, right) detect an obstacle (true if [white] reflection is present)."""
        data = self.i2c_read_sensors()
        ll = bool(data & self.MASK_LINE_LEFT)
        lc = bool(data & self.MASK_LINE_CENTER)
        lr = bool(data & self.MASK_LINE_RIGHT)
        li = bool(data & self.MASK_IR_LEFT)
        ri = bool(data & self.MASK_IR_RIGHT)
        return ll, lc, lr, not li, not ri

    def get_supply_voltage(self):
        """Returns the current supply voltage of the robot."""
        adc = self.voltage_pin.read_analog()  # ADC value 0 - 1023
        # Convert ADC value to volts: 3.3 V / 1024 (max. voltage at ADC pin / ADC resolution)
        voltage = 0.00322265625 * adc
        # Multiply measured voltage by voltage divider ratio to calculate actual voltage
        # (10 kOhm + 5,6 kOhm) / 5,6 kOhm [(R1 + R2) / R2, Voltage divider ratio]
        return voltage * 2.7857142

    @staticmethod
    def display_text(label):
        """Sets a label on the robot display (prints in log, displays the first letter on the screen)."""
        display.show(label[0])
        print("Label: %s" % label)

    @staticmethod
    def display_sensors(ll, lc, lr, il, ir, y=4, lb=9, ib=5):
        """Displays the sensors in top line of the display as pixels for each sensor.
        Line sensors (left, center, right) are far left, center, far right, lb is line brightness 0-9, default 9.
        IR sensors (left, right) are interlaced among them, ib is IR brightness 0-9, default 5."""
        display.set_pixel(4, y, lb if ll else 0)
        display.set_pixel(2, y, lb if lc else 0)
        display.set_pixel(0, y, lb if lr else 0)
        display.set_pixel(3, y, ib if il else 0)
        display.set_pixel(1, y, ib if ir else 0)

    @staticmethod
    def display_drive_mode(mode):
        """Displays the detected drive mode in the lower left corner (3x3 pixels) depicting the current situation
        we are dealing with when driving on the line. Supported lines (other chars clear the area):
        T/Y/+ - intersections, | - straight line, / - right turn, \ - left turn."""
        lines = System.DRIVE_MODE_PICTOGRAMS[mode if mode in System.DRIVE_MODE_PICTOGRAMS else ' ']
        System.display_bitmap(0, 2, 3, lines)

    @staticmethod
    def display_bitmap(x_pos: int, y_pos: int, width: int, lines: list[int]):
        """Displays the bitmap on the display (0x0 = top left, max 5x5). Bitwise, each line int is right-aligned."""
        for y in range(len(lines)):
            for x in range(width):
                display.set_pixel(4 - (x_pos + x), 4 - (y_pos + y), 9 if lines[y] & (1 << x) else 0)

    @staticmethod
    def display_clear():
        """Clears the display."""
        display.clear()

    @staticmethod
    def display_on():
        """Enables the display."""
        display.on()
        display.clear()

    @staticmethod
    def display_off():
        """Disables the display."""
        display.off()
