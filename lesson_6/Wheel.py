from time import ticks_ms, ticks_diff

from microbit import i2c


class WheelTachometer:
    """Handles the wheel tachometer. The tachometer is able to monitor
    the wheel movement precisely and provide the actual wheel rotation speed."""

    def __init__(self):
        """Initializes the wheel tachometer."""
        self.tick_counter = 0
        self.tick_last_time = 0
        self.tick_history = []
        self.tick_history_max = 10
        self.tick_history_interval_ms = 50
        self.ticks_per_wheel_rotation = 40
        self.wheel_radius_cm = 3.75
        self.wheel_circumference_cm = 2 * 3.14159265359 * self.wheel_radius_cm

    def on_tick(self):
        """Updates the tachometer state based on a new tick."""
        self.tick_counter += 1
        now = ticks_ms()
        time_delta = ticks_diff(now, self.tick_last_time)
        # if the last tick was too long ago, we reset the history
        if self.tick_last_time == 0 or time_delta >= self.tick_history_interval_ms * 10:
            self.tick_last_time = now
            self.tick_history = []
        else:
            self.tick_counter += 1
            if time_delta >= self.tick_history_interval_ms:
                self.tick_history.append(self.tick_counter)
                if len(self.tick_history) > self.tick_history_max:
                    self.tick_history.pop(0)
                self.tick_counter = 0
                # if we would be guarantied to be called all the time,
                # it would be better to just increase the last tick by interval
                # however, this can lead to incorrect values if we are too far behind
                self.tick_last_time = now

    def get_speed_cm_per_sec(self):
        """Returns the current wheel speed in cm/s."""
        speed = 0
        if len(self.tick_history) > 0:
            speed = (sum(self.tick_history) * self.wheel_circumference_cm
                     / self.ticks_per_wheel_rotation)
            speed /= len(self.tick_history) * self.tick_history_interval_ms / 1000
        return speed

    def __str__(self):
        return "speed: %.2f cm/s, tick history: %s" % (self.get_speed_cm_per_sec(), self.tick_history)

class Wheel:
    """Handles a single wheel on the Joy Car robot. The wheel is capable
    of moving forward or backward with given (variable) speed.

    The wheel is able to monitor its movement precisely and provide the
    actual wheel rotation speed to the caller. The wheel is also able to
    stop itself after a given distance or time, or to stop immediately."""

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
        self.speed = 0
        self.tachometer = WheelTachometer()

    def move(self, speed):
        """Moves the wheel with the given speed (indefinite ticks, time).
        The wheel will continue to move until stop() is called.
        The speed is a value between -100 and 100, where 0 means stop."""
        self.set_speed(speed)
        self.distance_remain_ticks = -1
        self.distance_req_time_ms = -1

    def move_by_ticks(self, speed, distance_ticks):
        """Moves the wheel forward with the given speed for the given distance
        in sensor ticks. If the motor is already moving, the asked distance is added
        to the remaining distance and the motor continues until no distance remains."""
        self.set_speed(speed)
        self.distance_remain_ticks += distance_ticks

    def move_by_time(self, speed, distance_time_ms):
        """Moves the wheel forward with the given speed for the given time.
        If the motor is already moving, the distance in time is added to the current
        distance and the motor continues to move until the total time is reached."""
        self.set_speed(speed)
        self.distance_req_time_ms += distance_time_ms
        if self.distance_start_time_ms == 0:
            self.distance_start_time_ms = ticks_ms()

    def set_speed(self, speed):
        """Sets the wheel speed (and direction). Does not affect the remaining
        distance or time previously set to perform."""
        speed = max(-255, min(255, speed))
        direction = self.motor_fwd_cmd if speed >= 0 else self.motor_rwd_cmd
        print("Setting wheel cmd %d speed %d" % (direction, speed))
        i2c.write(self.i2c_address, bytes([direction, abs(speed)]))
        self.speed = speed

    def stop(self):
        """Stops the wheel immediately."""
        self.set_speed(0)
        self.distance_remain_ticks = -1
        self.distance_req_time_ms = -1

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
        self.tachometer.on_tick()
        if self.distance_remain_ticks > 0:
            self.distance_remain_ticks -= 1
            if self.distance_remain_ticks == 0:
                self.stop_on_no_work()

    def get_sensor_value(self):
        """Returns the current sensor value."""
        return self.sensor_pin.read_digital()

    def update(self):
        """Retrieves the sensor value, checks for change and updates the wheel state
        based on the ongoing command."""
        sensor_value_now = self.get_sensor_value()
        if sensor_value_now != self.sensor_value:
            self.sensor_value = sensor_value_now
            self.on_tick()
        self.stop_on_no_work()
