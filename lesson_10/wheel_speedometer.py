from time import ticks_ms, ticks_diff


class WheelSpeedometer:
    """Speedometer is able to monitor the wheel movement precisely
    and provide the actual wheel rotation speed over the ticks
    measured for X consecutive constant time intervals."""

    def __init__(self):
        """Initializes the wheel speedometer."""
        self.tick_last_time = 0
        self.tick_counter = 0
        self.tick_counter_history = []
        self.tick_counter_history_length = 10
        self.tick_counter_history_interval_ms = 100
        self.ticks_per_wheel_rotation = 40
        self.wheel_radius_cm = 3.75
        self.wheel_circumference_cm = 2 * 3.14159265359 * self.wheel_radius_cm

    def reset(self):
        """Resets the speedometer state."""
        self.tick_last_time = 0
        self.tick_counter = 0
        self.tick_counter_history = []

    def on_tick(self):
        """Updates the speedometer state based on a new tick."""
        self.tick_counter += 1
        now = ticks_ms()
        time_delta = ticks_diff(now, self.tick_last_time)
        # if the last tick was too long ago, we reset the history
        history_too_old = time_delta >= self.tick_counter_history_interval_ms * 10
        if self.tick_last_time == 0 or history_too_old:
            self.tick_last_time = now
            self.tick_counter_history = []
        else:
            self.tick_counter += 1
            if time_delta >= self.tick_counter_history_interval_ms:
                self.tick_counter_history.append(self.tick_counter)
                if len(self.tick_counter_history) > self.tick_counter_history_length:
                    self.tick_counter_history.pop(0)
                self.tick_counter = 0
                # if we would be guarantied to be called all the time,
                # it would be better to just increase the last tick by interval
                # however, this can lead to incorrect values if we are too far behind
                self.tick_last_time = now

    def get_speed_cm_per_sec(self):
        """Returns the current wheel speed in cm/s."""
        speed = 0
        if len(self.tick_counter_history) > 0:
            speed = (sum(self.tick_counter_history) * self.wheel_circumference_cm
                     / self.ticks_per_wheel_rotation)
            speed /= (len(self.tick_counter_history)
                      * self.tick_counter_history_interval_ms / 1000)
        return speed

    def get_speed_radians_per_sec(self):
        """Returns the current wheel speed in radians/s."""
        return self.get_speed_cm_per_sec() / self.wheel_radius_cm

    def cm_to_radians(self, cm):
        """Converts cm to radians."""
        return cm / self.wheel_radius_cm

    def radians_to_cm(self, radians):
        """Converts radians to cm."""
        return radians * self.wheel_radius_cm

    def get_ticks_per_cm(self):
        """Returns the number of ticks per cm."""
        return self.ticks_per_wheel_rotation / self.wheel_circumference_cm

    def __str__(self):
        params = (self.get_speed_cm_per_sec(), self.tick_counter_history)
        return "speed: %.2f cm/s, tick history: %s" % params
