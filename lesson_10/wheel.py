from array import array
from time import ticks_ms, ticks_diff, sleep

from microbit import i2c

from wheel_speedometer import WheelSpeedometer


class Wheel:
    """Handles single wheel capable of moving forward or backward
    with given (variable) speed and stop immediately or conditionally
    based on distance and time."""

    def __init__(self, i2c_address, motor_fwd_cmd, motor_rwd_cmd, sensor_pin):
        """Initializes the wheel."""
        self.i2c_address = i2c_address
        self.motor_fwd_cmd = motor_fwd_cmd
        self.motor_rwd_cmd = motor_rwd_cmd
        self.sensor_pin = sensor_pin
        self.sensor_value = 0
        self.distance_remain_ticks = 0
        self.distance_req_time_ms = 0
        self.distance_start_time_ms = 0
        self.speed_pwm = 0
        self.speedometer = WheelSpeedometer()
        self.pwm_speed_to_cm_per_sec_start = 60
        self.pwm_speed_to_cm_per_sec_end = 255
        self.pwm_speed_to_cm_per_sec_table = [0.0 for _ in range(0, 256)]
        self.conversion_table_available = False

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

    def move_cm_per_sec_for_distance(self, speed_cm_per_sec, distance_cm):
        """Moves the wheel forward using given cm/s speed for given distance in cm.
        Please note: this method can be used just if the wheel has been calibrated."""
        speed_pwm = self.get_pwm_speed_for_cm_per_sec(speed_cm_per_sec)
        distance_ticks = int(distance_cm * self.speedometer.get_ticks_per_cm())
        self.move_pwm_for_ticks(speed_pwm, distance_ticks)

    def set_speed_pwm(self, speed_pwm):
        """Sets the wheel PWM speed (and direction). Does not affect the remaining
        distance or time previously set to perform. If the wheel was going
        in the other direction, resets the H-bridge other direction first."""
        if speed_pwm == 0:
            print("Stopping the wheel")
            i2c.write(self.i2c_address, bytes([self.motor_fwd_cmd, 0]))
            i2c.write(self.i2c_address, bytes([self.motor_rwd_cmd, 0]))
            return
        speed_pwm = max(-255, min(255, speed_pwm))
        if (self.speed_pwm < 0 < speed_pwm) or (self.speed_pwm > 0 > speed_pwm):
            # if we are changing the direction, we need to reset the motor first
            motor_reset_cmd = (self.motor_rwd_cmd
                               if speed_pwm >= 0 else self.motor_fwd_cmd)
            print("Changing wheel direction, resetting cmd %d speed_pwm %d" %
                  (motor_reset_cmd, 0))
            i2c.write(self.i2c_address, bytes([motor_reset_cmd, 0]))
        motor_set_cmd = self.motor_fwd_cmd if speed_pwm > 0 else self.motor_rwd_cmd
        print("Setting wheel cmd %d speed_pwm %d" % (motor_set_cmd, abs(speed_pwm)))
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

    def get_pwm_speed_for_cm_per_sec(self, cm_per_sec):
        """Returns the PWM speed for the given cm/s speed.
        We just scan the existing table to find the closest speed instead
        of creating a reverse table due to the lack of memory."""
        if not self.conversion_table_available:
            return 0
        pwm = 0
        cm_per_sec_delta_min = 255
        for idx in range(self.pwm_speed_to_cm_per_sec_start,
                         self.pwm_speed_to_cm_per_sec_end + 1):
            cm_per_sec_now = self.pwm_speed_to_cm_per_sec_table[idx]
            cm_per_sec_delta = abs(cm_per_sec_now - cm_per_sec)
            if cm_per_sec_delta < cm_per_sec_delta_min:
                cm_per_sec_delta_min = cm_per_sec_delta
                pwm = idx
        return pwm

    def get_pwm_speed_for_radians_per_sec(self, radians_per_sec):
        """Returns the PWM speed for the given rad/s speed."""
        cm_per_sec = self.speedometer.radians_to_cm(radians_per_sec)
        return self.get_pwm_speed_for_cm_per_sec(cm_per_sec)

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

    def get_sensor_value(self):
        """Returns the current sensor value."""
        return self.sensor_pin.read_digital()

    def get_speedometer(self):
        """Returns the speedometer of the wheel."""
        return self.speedometer

    def update(self):
        """Retrieves the sensor value, checks for change and updates the wheel state
        based on the ongoing command."""
        sensor_value_now = self.get_sensor_value()
        if sensor_value_now != self.sensor_value:
            self.sensor_value = sensor_value_now
            self.on_tick()
        self.stop_on_no_work()

    def gather_pwm_to_real_speed_table(self):
        """Gathers the real forward and reverse speeds for PWM speeds 0 to 255
        based on the speedometer readings. Each value is scanned after 1 second.
        The calibration fills conversion tables between PWM and cm/s + PWM and rad/s."""
        start = self.pwm_speed_to_cm_per_sec_start
        end = self.pwm_speed_to_cm_per_sec_end
        for speed_pwm in range(start, end + 1):
            start_time = ticks_ms()
            self.move_pwm(speed_pwm)
            while ticks_diff(ticks_ms(), start_time) < 1000:
                self.update()
                sleep(0.001)
            cm_per_sec = self.get_speed_cm_per_sec()
            radians_per_sec = self.get_speed_radians_per_sec()
            self.stop()
            print("PWM speed %d: %f cm/s (%f rad/s)" %
                  (speed_pwm, cm_per_sec, radians_per_sec))
            self.pwm_speed_to_cm_per_sec_table[speed_pwm] = cm_per_sec
            sleep(0.25)

    def get_pwm_speed_to_cm_per_sec_table(self):
        """Returns the PWM speed to cm/s conversion table."""
        return self.pwm_speed_to_cm_per_sec_table
