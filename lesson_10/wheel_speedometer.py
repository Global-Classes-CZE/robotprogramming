from time import ticks_ms, ticks_diff


class WheelSpeedometer:
    """Speedometer is able to monitor the wheel movement precisely
    and provide the actual wheel rotation speed over the ticks
    measured for X consecutive constant time intervals."""
    PI = 3.14159265359

    def __init__(self, sensor_pin):
        """Initializes the wheel speedometer."""
        self.sensor_pin = sensor_pin
        self.sensor_value = 0
        self.tick_last_time = 0
        self.tick_sampling_ms = 10
        self.tick_counter = 0
        self.tick_history = []
        self.tick_history_time = []
        self.tick_history_length = 5
        self.tick_history_interval_ms = self.tick_history_length * self.tick_sampling_ms
        self.tick_history_sum = 0
        self.ticks_per_wheel = 40
        self.radians_per_wheel = 2 * self.PI
        self.radians_per_tick = self.radians_per_wheel / self.ticks_per_wheel
        self.wheel_radius_cm = 3.75
        self.cm_per_wheel = 2 * self.PI * self.wheel_radius_cm
        self.speed_radians = 0
        self.speed_cm = 0
        self.on_tick_counter = 0

    def reset(self):
        """Resets the speedometer state."""
        self.tick_last_time = 0
        self.tick_counter = 0
        self.tick_history = []
        self.tick_history_time = []

    def update(self):
        """Updates the speedometer state based on the ongoing command."""
        """Retrieves the sensor value, checks for change and updates the wheel state
        based on the ongoing command."""
        sensor_value_now = self.sensor_pin.read_digital()
        if sensor_value_now == self.sensor_value:
            return False
        self.sensor_value = sensor_value_now
        self.on_tick()
        return True

    def on_tick(self):
        """Updates the speedometer state based on a new tick."""
        self.tick_counter += 1
        self.on_tick_counter += 1
        now = ticks_ms()
        time_delta = ticks_diff(now, self.tick_last_time)
        # if the last tick was too long ago, we reset the history
        history_too_old = time_delta >= self.tick_history_interval_ms * self.tick_history_length
        if self.tick_last_time == 0 or history_too_old:
            self.tick_last_time = now
            self.tick_history_time = []
            self.tick_history_time.append(now)
            self.tick_history = []
            self.tick_history.append(self.tick_counter)
            self.tick_history_sum = self.tick_counter
        elif time_delta >= self.tick_history_interval_ms:
            self.tick_history_time.append(now)
            self.tick_history.append(self.tick_counter)
            self.tick_history_sum += self.tick_counter
            if len(self.tick_history) > self.tick_history_length:
                self.tick_history_time.pop(0)
                tick_count_obsolete = self.tick_history.pop(0)
                self.tick_history_sum -= tick_count_obsolete
            self.tick_counter = 0
            self.tick_last_time = now

    def get_speed_radians_per_sec(self):
        """Returns the current wheel speed in radians/s."""
        if len(self.tick_history) == 0:
            return 0
        # print("history %s" % self.tick_history)
        elapsed_time = ticks_diff(self.tick_history_time[-1], self.tick_history_time[0])
        sec_fragment = (1000 / elapsed_time) if elapsed_time > 0 else 1
        speed = (self.tick_history_sum / self.ticks_per_wheel) * self.radians_per_wheel * sec_fragment
        return speed

    def get_speed_cm_per_sec(self):
        """Returns the current wheel speed in cm/s."""
        return (self.get_speed_radians_per_sec() / self.radians_per_wheel) * self.cm_per_wheel

    def cm_to_radians(self, cm):
        """Converts cm to radians."""
        return cm / self.cm_per_wheel * self.radians_per_wheel

    def radians_to_cm(self, radians):
        """Converts radians to cm."""
        return radians / self.radians_per_wheel * self.cm_per_wheel

    def get_ticks_per_cm(self):
        """Returns the number of ticks per cm."""
        return self.ticks_per_wheel / self.cm_per_wheel

    def __str__(self):
        params = (self.get_speed_cm_per_sec(), self.tick_history)
        return "speed: %.2f cm/s, tick history: %s" % params
