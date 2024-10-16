from time import ticks_ms, ticks_diff

from microbit import i2c

from wheel_speedometer import WheelSpeedometer


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
        self.distance_remain_ticks = 0
        self.distance_req_time_ms = 0
        self.distance_start_time_ms = 0
        self.speed_pwm = 0
        self.speedometer = WheelSpeedometer(sensor_pin=sensor_pin)
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
        self.distance_req_time_ms = -1

    def move_pwm_for_ticks(self, speed_pwm, distance_ticks):
        """Moves the wheel forward using given PWM speed for the given distance
        in sensor ticks. If the motor is already moving, the asked distance is added
        to the remaining distance and the motor continues until no distance remains."""
        self.set_speed_pwm(speed_pwm)
        self.distance_remain_ticks += distance_ticks

    def move_pwm_for_time(self, speed_pwm, distance_time_ms):
        """Moves the wheel forward using given PWM speed for the given time.
        If the motor is already moving, the distance in time is added to the current
        distance and the motor continues to move until the total time is reached."""
        self.set_speed_pwm(speed_pwm)
        self.distance_req_time_ms += distance_time_ms
        if self.distance_start_time_ms == 0:
            self.distance_start_time_ms = ticks_ms()

    def move_pwm_for_distance(self, speed_pwm, distance_cm):
        """Moves the wheel forward using given PWM speed for given distance in cm."""
        ticks_for_distance = int(distance_cm * self.speedometer.get_ticks_per_cm())
        self.move_pwm_for_ticks(speed_pwm, ticks_for_distance)

    def set_speed_pwm(self, speed_pwm):
        """Sets the wheel PWM speed (and direction). Does not affect the remaining
        distance or time previously set to perform. If the wheel was going
        in the other direction, resets the H-bridge other direction first."""
        if speed_pwm == 0:
            # print("Stopping %s wheel" % self.name)
            i2c.write(self.i2c_address, bytes([self.motor_fwd_cmd, 0]))
            i2c.write(self.i2c_address, bytes([self.motor_rwd_cmd, 0]))
            return
        speed_pwm = int(max(-255, min(255, speed_pwm)))
        if (self.speed_pwm < 0 < speed_pwm) or (self.speed_pwm > 0 > speed_pwm):
            # if we are changing the direction, we need to reset the motor first
            motor_reset_cmd = (self.motor_rwd_cmd
                               if speed_pwm >= 0 else self.motor_fwd_cmd)
            # print("Changing %s wheel direction" % self.name)
            i2c.write(self.i2c_address, bytes([motor_reset_cmd, 0]))
        motor_set_cmd = self.motor_fwd_cmd if speed_pwm > 0 else self.motor_rwd_cmd
        # print("Setting %s wheel speed_pwm %d" % (self.name, speed_pwm))
        i2c.write(self.i2c_address, bytes([motor_set_cmd, abs(speed_pwm)]))
        self.speed_pwm = speed_pwm

    def get_speed_pwm(self):
        """Returns the current PWM speed of the wheel."""
        return self.speed_pwm

    def get_speed_cm_per_sec(self):
        """Returns the current speed of the wheel."""
        return self.speedometer.get_speed_cm_per_sec()

    def get_speed_radians_per_sec(self):
        """Returns the current speed of the wheel in radians per second."""
        return self.speedometer.get_speed_radians_per_sec()

    def rad_per_sec_to_pwm_speed(self, rad_per_sec):
        """Returns the PWM speed for the given rad/s speed.
        We use the multiplier and shift values to calculate the PWM speed using formula:
        rad_per_sec = pwm * multiplier + shift, for us: pwm = (rad_per_sec - shift) / multiplier."""
        if self.pwm_multiplier == 0:
            print("error: wheel %s pwm_multiplier is 0" % self.name)
            return 0
        return int((rad_per_sec - self.pwm_shift) / self.pwm_multiplier)

    def cm_per_sec_to_pwm_speed(self, cm_per_sec):
        """Returns the PWM speed for the given cm/s speed.
        We just scan the existing table to find the closest speed instead
        of creating a reverse table due to the lack of memory."""
        rad_per_sec = self.speedometer.cm_to_radians(cm_per_sec)
        return self.rad_per_sec_to_pwm_speed(rad_per_sec)

    def get_pwm_ticks_for_distance_using_cm_per_sec(self, speed_cm_per_sec, distance_cm):
        """Moves the wheel forward using given cm/s speed for given distance in cm.
        Please note: this method can be used just if the wheel has been calibrated."""
        speed_pwm = self.cm_per_sec_to_pwm_speed(speed_cm_per_sec)
        distance_ticks = int(distance_cm * self.speedometer.get_ticks_per_cm())
        return speed_pwm, distance_ticks

    def stop(self):
        """Stops the wheel immediately."""
        self.set_speed_pwm(0)
        self.distance_remain_ticks = -1
        self.distance_req_time_ms = -1
        self.speedometer.reset()

    def stop_on_no_work(self):
        """Stops the wheel if the remaining distance in ticks or time is reached."""
        stop_due_to_ticks = False
        if self.distance_remain_ticks == 0:
            stop_due_to_ticks = True
        stop_due_to_time = False
        if self.distance_req_time_ms > 0:
            time_delta = ticks_diff(ticks_ms(), self.distance_start_time_ms)
            if time_delta >= self.distance_req_time_ms:
                stop_due_to_time = True
        # we stop only if both conditions are met
        # otherwise we keep the other condition finish as well
        if stop_due_to_ticks and stop_due_to_time:
            self.stop()

    def on_tick(self):
        """Updates the wheel state based on a new tick,
        checks the remaining distance in ticks."""
        self.speedometer.on_tick()
        if self.distance_remain_ticks > 0:
            self.distance_remain_ticks -= 1
            if self.distance_remain_ticks == 0:
                self.stop_on_no_work()

    def update(self):
        """Updates the speedometer and general wheel state."""
        if self.speedometer.update() is True:
            self.on_tick()
        self.stop_on_no_work()
