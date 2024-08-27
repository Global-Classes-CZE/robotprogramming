from microbit import pin14, pin15, i2c

from Wheel import Wheel


class WheelDriver:
    """Handles the movement of the Joy Car robot. The driver is capable
    of moving the robot forward or backward, turning left or right, or
    stopping the robot completely. The driver is able to move the robot
    indefinitely, for a given distance or for a given time.

    Future iterations will be able to handle more complex movement patterns
    like curves, circles or real distance-based commands."""
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

    def move(self, speed_left, speed_right):
        """Moves the robot with the given speed for each wheel."""
        self.wheel_left.move(speed_left)
        self.wheel_right.move(speed_right)

    def move_by_ticks(self, speed_left, speed_right, distance_ticks):
        """Moves the robot with the given speed for each wheel for given distance."""
        self.wheel_left.move_by_ticks(speed_left, distance_ticks)
        self.wheel_right.move_by_ticks(speed_right, distance_ticks)

    def move_by_time(self, speed_left, speed_right, distance_time_ms):
        """Moves the robot with the given speed for each wheel for the given time."""
        self.wheel_left.move_by_time(speed_left, distance_time_ms)
        self.wheel_right.move_by_time(speed_right, distance_time_ms)

    def stop(self):
        """Stops the robot."""
        self.wheel_left.stop()
        self.wheel_right.stop()

    def update(self):
        """Updates the wheel driver, propagating the changes to the hardware."""
        self.wheel_left.update()
        self.wheel_right.update()

    def get_speed(self):
        """Returns the current speed of the robot."""
        return self.wheel_left.speed, self.wheel_right.speed

    def get_ticks(self):
        """Returns the current ticks of the robot."""
        return self.wheel_left.tick_counter, self.wheel_right.tick_counter
