from microbit import pin14, pin15, i2c

from wheel import Wheel
from wheel_calibrator import WheelCalibrator


class WheelDriver:
    """Handles the movement of the whole robot
        (forward, backward, turning). Activities are either
        indefinite or conditional based on ticks, time
        or real speed measured by the speedometer on wheel level."""
    I2C_ADDRESS = 0x70

    def __init__(self,
                 left_pwm_min=60, left_pwm_max=255, left_pwm_multiplier=0, left_pwm_shift=0,
                 right_pwm_min=60, right_pwm_max=255, right_pwm_multiplier=0, right_pwm_shift=0):
        """Initializes the wheel driver."""
        i2c.init(freq=100000)
        i2c.write(self.I2C_ADDRESS, b"\x00\x01")
        i2c.write(self.I2C_ADDRESS, b"\xE8\xAA")
        self.wheel_left = Wheel(name="left", i2c_address=self.I2C_ADDRESS,
                                motor_fwd_cmd=5, motor_rwd_cmd=4, sensor_pin=pin14,
                                pwm_min=left_pwm_min, pwm_max=left_pwm_max,
                                pwm_multiplier=left_pwm_multiplier, pwm_shift=left_pwm_shift)
        self.wheel_right = Wheel(name="right", i2c_address=self.I2C_ADDRESS,
                                 motor_fwd_cmd=3, motor_rwd_cmd=2, sensor_pin=pin15,
                                 pwm_min=right_pwm_min, pwm_max=right_pwm_max,
                                 pwm_multiplier=right_pwm_multiplier, pwm_shift=right_pwm_shift)
        self.wheel_calibrator_left = WheelCalibrator(wheel=self.wheel_left)
        self.wheel_calibrator_right = WheelCalibrator(wheel=self.wheel_right)

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
