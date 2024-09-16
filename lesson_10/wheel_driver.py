from microbit import pin14, pin15, i2c

from wheel import Wheel


class WheelDriver:
    """Handles the movement of the whole robot
        (forward, backward, turning). Activities are either
        indefinite or conditional based on ticks, time
        or real speed measured by the speedometer on wheel level."""
    I2C_ADDRESS = 0x70

    def __init__(self):
        """Initializes the wheel driver."""
        i2c.init(freq=100000)
        i2c.write(self.I2C_ADDRESS, b"\x00\x01")
        i2c.write(self.I2C_ADDRESS, b"\xE8\xAA")
        self.wheel_left = Wheel(i2c_address=self.I2C_ADDRESS,
                                motor_fwd_cmd=5, motor_rwd_cmd=4, sensor_pin=pin14)
        self.wheel_right = Wheel(i2c_address=self.I2C_ADDRESS,
                                 motor_fwd_cmd=3, motor_rwd_cmd=2, sensor_pin=pin15)

    def move_pwm(self, speed_pwm_left, speed_pwm_right):
        """Moves the robot with the PWM given speed for each wheel."""
        self.wheel_left.move_pwm(speed_pwm_left)
        self.wheel_right.move_pwm(speed_pwm_right)

    def move_pwm_for_ticks(self, speed_pwm_left, speed_pwm_right,
                           distance_ticks_left, distance_ticks_right):
        """Moves robot using PWM speed to given distance in ticks, for each wheel."""
        self.wheel_left.move_pwm_for_ticks(speed_pwm_left, distance_ticks_left)
        self.wheel_right.move_pwm_for_ticks(speed_pwm_right, distance_ticks_right)

    def move_pwm_for_time(self, speed_pwm_left, speed_pwm_right, time_ms):
        """Moves robot using PWM speed for each wheel for given time."""
        self.wheel_left.move_pwm_for_time(speed_pwm_left, time_ms)
        self.wheel_right.move_pwm_for_time(speed_pwm_right, time_ms)

    def move_pwm_for_distance(self, speed_pwm_left, speed_pwm_right, distance_cm):
        """Moves robot using PWM speed for each wheel to given distance."""
        self.wheel_left.move_pwm_for_distance(speed_pwm_left, distance_cm)
        self.wheel_right.move_pwm_for_distance(speed_pwm_right, distance_cm)

    def stop(self):
        """Stops the robot."""
        self.wheel_left.stop()
        self.wheel_right.stop()

    def update(self):
        """Updates the wheel driver, propagating the changes to the hardware."""
        self.wheel_left.update()
        self.wheel_right.update()

    def get_speed_pwm(self):
        """Returns the current speed of the robot."""
        return self.wheel_left.speed_pwm, self.wheel_right.speed_pwm

    def get_speed_cm_per_sec(self):
        """Returns the current speed of the robot in cm/s."""
        speed_left = self.wheel_left.get_speed_cm_per_sec()
        speed_right = self.wheel_right.get_speed_cm_per_sec()
        return speed_left, speed_right

    def get_speed_radians_per_sec(self):
        """Returns the current speed of the robot in radians per second."""
        speed_left = self.wheel_left.get_speed_radians_per_sec()
        speed_right = self.wheel_right.get_speed_radians_per_sec()
        return speed_left, speed_right

    def get_speedometer(self):
        """Returns the left and right speedometer of the robot's wheels."""
        return self.wheel_left.speedometer, self.wheel_right.speedometer

    def gather_pwm_to_real_speed_table(self):
        """Calibrates (gathers) the real forward and reverse speeds for PWM speeds
        based on the speedometer readings, for each wheel. Each value is scanned
        2 seconds after establishing the PWM speed.

        The calibration fills two sets of conversion tables:
        PWM<->cm/s and PWM<->rad/s, on each wheel separately. These can then
        be used to drive the robot with a predetermined speed w/o worrying about PWM."""
        print("Calibrating left wheel")
        self.wheel_left.gather_pwm_to_real_speed_table()
        print("Calibrating right wheel")
        self.wheel_right.gather_pwm_to_real_speed_table()
        print("Calibration done")
