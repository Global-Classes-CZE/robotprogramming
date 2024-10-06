from microbit import pin14, pin15, i2c

from wheel import Wheel


class WheelDriver:
    """Handles the movement of the whole robot
        (forward, backward, turning). Activities are either
        indefinite or conditional based on ticks, time
        or real speed measured by the encoder on wheel level."""
    I2C_ADDRESS = 0x70

    def __init__(self,
                 left_pwm_min=50, left_pwm_max=255, left_pwm_multiplier=0, left_pwm_shift=0,
                 right_pwm_min=50, right_pwm_max=255, right_pwm_multiplier=0, right_pwm_shift=0):
        """Initializes the wheel driver."""
        i2c.init(freq=100000)
        i2c.write(self.I2C_ADDRESS, b"\x00\x01")
        i2c.write(self.I2C_ADDRESS, b"\xE8\xAA")
        self.left = Wheel(name="left", i2c_address=self.I2C_ADDRESS,
                                motor_fwd_cmd=5, motor_rwd_cmd=4, sensor_pin=pin14,
                                pwm_min=left_pwm_min, pwm_max=left_pwm_max,
                                pwm_multiplier=left_pwm_multiplier, pwm_shift=left_pwm_shift)
        self.right = Wheel(name="right", i2c_address=self.I2C_ADDRESS,
                                 motor_fwd_cmd=3, motor_rwd_cmd=2, sensor_pin=pin15,
                                 pwm_min=right_pwm_min, pwm_max=right_pwm_max,
                                 pwm_multiplier=right_pwm_multiplier, pwm_shift=right_pwm_shift)
        self.stop()

    # Please note: normally, we would have aggregate move...() methods here for both wheels, but
    # these got removed in favor of smaller code memory footprint + we control each wheel separately anyway.

    def stop(self):
        """Stops the robot."""
        self.left.stop()
        self.right.stop()

    def update(self):
        """Updates the wheel driver, propagating the changes to the hardware."""
        self.left.update()
        self.right.update()
