class System:
    """System class for the robot core system interface,
    with platform-specific implementations separate classes."""
    SYS_MBIT = "Micro:Bit"
    SYS_PICO = "Pico:Ed"

    I2C_FREQ = 100_000
    I2C_SENSOR_DEVICE = 0x38
    I2C_MOTOR_DEVICE = 0x70

    MASK_LINE_LEFT = 0x04
    MASK_LINE_CENTER = 0x08
    MASK_LINE_RIGHT = 0x10
    MASK_IR_LEFT = 0x20
    MASK_IR_RIGHT = 0x40

    SOUND_SPEED = 343  # m/s

    def __init__(self):
        """Initializes the system."""
        pass

    def get_system_type(self):
        """Returns the system type."""
        pass

    def ticks_us(self):
        """Returns the current time in microseconds."""
        pass

    def ticks_diff(self, ticks1, ticks2):
        """Returns the difference between two time values in microseconds."""
        pass

    def sleep_us(self, us):
        """Sleeps for the given time in microseconds."""
        pass

    def i2c_scan(self) -> list[int]:
        """Scans the I2C bus for devices and returns a list of addresses."""
        pass

    def i2c_read(self, addr: int, n: int) -> bytes:
        """Reads 'n' amount of data from the I2C device into a buffer."""
        pass

    def i2c_write(self, addr: int, buf: bytes):
        """Writes data to the I2C device from a buffer."""
        pass

    def i2c_write_motor(self, buf: bytes):
        """Writes data to the I2C motor device from a buffer."""
        self.i2c_write(self.I2C_MOTOR_DEVICE, buf)

    def i2c_init_motor(self):
        """Initializes the I2C motor device."""
        self.i2c_write_motor(b"\x00\x01")
        self.i2c_write_motor(b"\xE8\xAA")

    def i2c_read_sensors(self):
        """Returns the current sensor data byte."""
        return self.i2c_read(self.I2C_SENSOR_DEVICE, 1)[0]

    def get_sensors(self):
        """Checks if line sensors (..., left, center, right) detected a line (true if line is present)
        or obstacle sensors (left, right, ...) detect an obstacle (true if [white] reflection is present)."""
        data = self.i2c_read_sensors()
        li = bool(data & self.MASK_IR_LEFT)
        ri = bool(data & self.MASK_IR_RIGHT)
        ll = bool(data & self.MASK_LINE_LEFT)
        lc = bool(data & self.MASK_LINE_CENTER)
        lr = bool(data & self.MASK_LINE_RIGHT)
        return not li, not ri, ll, lc, lr

    def pin_read_digital(self, pin):
        """Reads the digital value of a pin."""
        pass

    def pin_write_digital(self, pin, value: int):
        """Writes a digital value to the pin."""
        pass

    def set_sonar_angle_pwm(self, angle_pwm: int):
        """Sets front sonar horizontal angle PWM value."""
        pass

    def get_sonar_echo_delay_us(self, timeout_us) -> int:
        """Measures the delay it takes for the sonar echo to return.
        Returns the delay in microseconds or a negative value if the timeout was reached."""
        pass

    def get_sonar_distance(self, max_distance=1.0) -> float:
        """Returns the distance in meters measured by the sonar,
        with the maximum time spent on detecting the echo based on the max distance we want to detect.
        This is by default set to 1m as the reasonable maximum distance for the sonar balanced to max time spent."""
        timeout_us = int((2 * max_distance / self.SOUND_SPEED) * 1_000_000)
        measured_time_us = self.get_sonar_echo_delay_us(timeout_us=timeout_us)
        if measured_time_us < 0:
            return measured_time_us
        measured_time_sec = measured_time_us / 1_000_000
        return measured_time_sec * self.SOUND_SPEED / 2

    def get_encoder_pin_left(self):
        """Returns the pin object for the left encoder."""
        pass

    def get_encoder_pin_right(self):
        """Returns the pin object for the right encoder."""
        pass

    def get_adc_value(self) -> int:
        """Returns the current ADC value of the robot (0 - 1023)."""
        pass

    def get_supply_voltage(self):
        """Returns the current supply voltage of the robot."""
        adc = self.get_adc_value()  # ADC value 0 - 1023
        # Convert ADC value to volts: 3.3 V / 1024 (max. voltage at ADC pin / ADC resolution)
        voltage = 0.00322265625 * adc
        # Multiply measured voltage by voltage divider ratio to calculate actual voltage
        # (10 kOhm + 5,6 kOhm) / 5,6 kOhm [(R1 + R2) / R2, Voltage divider ratio]
        return voltage * 2.7857142

    def is_button_a_pressed(self):
        """Returns whether button A is pressed."""
        pass

    def is_button_b_pressed(self):
        """Returns whether button B is pressed."""
        pass

    def display_text(self, label):
        """Sets a label on the robot display (prints in log, displays the first letter on the screen)."""
        pass

    def display_sensors(self, il, ir, ll, lc, lr, y=4, lb=9, ib=5):
        """Displays the sensors in top line of the display as pixels for each sensor.
        Line sensors (left, center, right) are far left, center, far right, lb is line brightness 0-9, default 9.
        IR sensors (left, right) are interlaced among them, ib is IR brightness 0-9, default 5."""
        pass

    def get_drive_mode_symbol_keys(self):
        """Returns the keys of the drive mode symbols."""
        pass

    def display_drive_mode(self, mode: str):
        """Displays the drive mode depicting the current situation we are in now.
        The form of the displaying of the mode is platform-dependent.
        Variable mode refers to the pictogram displayed, see each implementation (they should be in sync)."""
        pass

    def display_choice(self, choice: str):
        """Displays the choice depicting the current situation we are in now.
        The form of the displaying of the choice is platform-dependent.
        Variable mode refers to the pictogram displayed, see each implementation (they should be in sync)."""
        pass

    def display_position(self, x: float, y: float):
        """Displays the robot position on the display. The actual implementation depends on the platform."""
        pass

    def display_speed(self, speed_now, speed_max, left: bool):
        """Displays one of the two current wheel speeds on the display. Position and form is platform-dependent."""
        pass

    def display_bitmap(self, x_pos: int, y_pos: int, width: int, lines: list[int]):
        """Displays bitmap on display (0x0 = top left, max is platform-dependent: 5x5 on Micro:Bit, 27x7 Pico:Ed).
        Bitwise, each line int is right-aligned."""
        pass

    def display_clear(self):
        """Clears the display."""
        pass

    def display_on(self):
        """Enables the display."""
        pass

    def display_off(self):
        """Disables the display."""
        pass
