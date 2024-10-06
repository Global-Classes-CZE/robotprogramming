from utime import ticks_us, ticks_diff

from microbit import i2c

from wheel_encoder import WheelEncoder


class Wheel:
    """Handles single wheel capable of moving forward or backward
    with given (variable) speed and stop immediately or conditionally
    based on distance and time."""

    def __init__(self, name, i2c_address, motor_fwd_cmd, motor_rwd_cmd, sensor_pin,
                 pwm_min=60, pwm_max=255, pwm_multiplier=0, pwm_shift=0):
        """Initializes the wheel."""
        self.name = name
        self.i2c_address = i2c_address
        self.motor_fwd_cmd = motor_fwd_cmd
        self.motor_rwd_cmd = motor_rwd_cmd
        self.distance_remain_ticks = -1
        self.distance_req_time_us = -1
        self.distance_start_time_us = 0
        self.speed_pwm = 0
        self.enc = WheelEncoder(sensor_pin=sensor_pin)
        self.pwm_min = pwm_min
        self.pwm_max = pwm_max
        self.pwm_multiplier = pwm_multiplier
        self.pwm_shift = pwm_shift

    def move_pwm(self, speed_pwm):
        """Moves the wheel using given PWM speed (indefinite ticks, time).
        The wheel will continue to move until stop() is called.
        The PWM speed is a value between -255 and 255, where 0 means stop."""
        self.set_speed_pwm(speed_pwm)
        self.distance_remain_ticks = -1
        self.distance_req_time_us = -1

    def move_pwm_for_ticks(self, speed_pwm, distance_ticks):
        """Moves the wheel forward using given PWM speed for the given distance
        in sensor ticks. If the motor is already moving, the asked distance is added
        to the remaining distance and the motor continues until no distance remains."""
        self.set_speed_pwm(speed_pwm)
        print("Moving %s wheel with speed %d pwm for distance %f ticks" % (self.name, speed_pwm, distance_ticks))
        self.distance_remain_ticks += distance_ticks

    def move_pwm_for_time(self, speed_pwm, distance_time_us):
        """Moves the wheel forward using given PWM speed for the given time.
        If the motor is already moving, the distance in time is added to the current
        distance and the motor continues to move until the total time is reached."""
        self.set_speed_pwm(speed_pwm)
        self.distance_req_time_us += distance_time_us
        if self.distance_start_time_us == 0:
            self.distance_start_time_us = ticks_us()

    def move_pwm_for_distance(self, speed_pwm, distance):
        """Moves the wheel forward using given PWM speed for given distance in meters."""
        distance_ticks = int(distance * self.enc.TICKS_PER_M)
        self.move_pwm_for_ticks(speed_pwm, distance_ticks)

    def move_radsec_for_distance(self, radsec, distance):
        """Moves the wheel using given rad/s speed for given distance in meters."""
        print("Moving %s wheel with speed %f rad/s for distance %f m" % (self.name, radsec, distance))
        speed_pwm = self.radsec2pwm(radsec)
        distance_ticks = int(distance * self.enc.TICKS_PER_M) * 2
        self.move_pwm_for_ticks(speed_pwm, distance_ticks)

    def set_speed_pwm(self, speed_pwm):
        """Sets the wheel PWM speed (and direction). Does not affect the remaining
        distance or time previously set to perform. If the wheel was going
        in the other direction, resets the H-bridge other direction first."""
        if speed_pwm == 0:
            if self.speed_pwm != 0:
                # print("Stopping %s wheel" % self.name)
                i2c.write(self.i2c_address, bytes([self.motor_fwd_cmd, 0]))
                i2c.write(self.i2c_address, bytes([self.motor_rwd_cmd, 0]))
                self.speed_pwm = 0
            return
        speed_pwm = int(max(-255, min(255, speed_pwm)))
        if self.speed_pwm == speed_pwm:
            return
        self.enc.reset()
        if (self.speed_pwm < 0 < speed_pwm) or (self.speed_pwm > 0 > speed_pwm):
            # if we are changing the direction, we need to reset the motor first
            motor_reset_cmd = (self.motor_rwd_cmd
                               if speed_pwm >= 0 else self.motor_fwd_cmd)
            # print("Changing %s wheel direction" % self.name)
            i2c.write(self.i2c_address, bytes([motor_reset_cmd, 0]))
        motor_set_cmd = self.motor_fwd_cmd if speed_pwm > 0 else self.motor_rwd_cmd
        print("Setting %s wheel speed_pwm %d" % (self.name, speed_pwm))
        i2c.write(self.i2c_address, bytes([motor_set_cmd, abs(speed_pwm)]))
        self.speed_pwm = speed_pwm

    def radsec2pwm(self, radsec):
        """Returns the PWM speed for the given rad/s speed.
        We use the multiplier and shift values to calculate the PWM speed using formula:
        rad_per_sec = pwm * multiplier + shift, for us: pwm = (rad_per_sec - shift) / multiplier."""
        if self.pwm_multiplier == 0:
            print("error: wheel %s pwm_multiplier is 0" % self.name)
            return 0
        direction = 1 if radsec >= 0 else -1
        return direction * int((abs(radsec) - self.pwm_shift) / self.pwm_multiplier)

    def msec2pwm(self, msec):
        """Returns the PWM speed for the given m/s speed."""
        rad_per_sec = self.enc.m2rad(msec)
        return self.radsec2pwm(rad_per_sec)

    def stop(self):
        """Stops the wheel immediately."""
        self.set_speed_pwm(0)
        self.distance_remain_ticks = -1
        self.distance_req_time_us = -1
        self.enc.reset()

    def stop_on_no_work(self):
        """Stops the wheel if the remaining distance in ticks or time is reached."""
        stop_due_to_ticks = True
        if self.distance_remain_ticks > 0:
            stop_due_to_ticks = False
        stop_due_to_time = True
        if self.distance_req_time_us > 0:
            time_delta = ticks_diff(ticks_us(), self.distance_start_time_us)
            if time_delta < self.distance_req_time_us:
                stop_due_to_time = False
        # we stop only if both conditions are met
        # otherwise we keep the other condition finish as well
        if stop_due_to_ticks and stop_due_to_time:
            self.stop()

    def on_tick(self):
        """Updates the wheel state based on a new tick,
        checks the remaining distance in ticks."""
        if self.distance_remain_ticks > 0:
            self.distance_remain_ticks -= 1

    def update(self):
        """Updates the encoder and general wheel state."""
        if self.enc.update() is True:
            self.on_tick()
        self.stop_on_no_work()
