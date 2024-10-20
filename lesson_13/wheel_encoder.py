from utime import ticks_us, ticks_diff

class WheelEncoder:
    """Encoder is able to monitor the wheel movement precisely
    and provide the actual wheel rotation speed over the ticks
    measured for X consecutive constant time intervals."""
    USE_BOTH_EDGES = False
    TICKS_PER_WHEEL = 40 if USE_BOTH_EDGES else 20
    RAD_PER_WHEEL = 2 * 3.14159265359
    RAD_PER_TICK = RAD_PER_WHEEL / TICKS_PER_WHEEL
    WHEEL_CIRCUMFERENCE_M = 0.21
    WHEEL_RADIUS_M = WHEEL_CIRCUMFERENCE_M / RAD_PER_WHEEL
    WHEEL_CENTER_DISTANCE = 0.075
    M_PER_WHEEL = RAD_PER_WHEEL * WHEEL_RADIUS_M
    TICKS_PER_M = TICKS_PER_WHEEL / M_PER_WHEEL
    MIN_TICK_TIME_US = 5_000  # minimum possible tick time (switch instability detection under this value)
    MAX_TICK_TIME_US = 200_000  # maximum possible tick time (after which we consider speed to be zero)
    AVG_TICK_COUNT = 3

    def __init__(self, sensor_pin):
        """Initializes the wheel encoder."""
        self.sensor_pin = sensor_pin
        self.sensor_value = -1
        self.tick_last_time = -1
        self.tick_last_time_avg = -1
        self.update_count = 0
        self.tick_count = 0
        self.speed_radsec = 0
        self.speed_radsec_avg = 0
        self.calc_value = -1
        self.calc_tick = 0
        self.calc_update_count = -1

    def reset(self):
        """Resets the encoder state."""
        self.__init__(self.sensor_pin)

    def update(self):
        """Updates the encoder state based on the ongoing command."""
        """Retrieves the sensor value, checks for change and updates the wheel state
        based on the ongoing command."""
        self.update_count += 1
        time_now = ticks_us()
        last_time_diff = ticks_diff(time_now, self.tick_last_time)
        if self.tick_last_time != -1 and last_time_diff < self.MIN_TICK_TIME_US:
            return False
        sensor_value_now = self.sensor_pin.read_digital()
        if sensor_value_now == self.sensor_value:
            if last_time_diff >= self.MAX_TICK_TIME_US:
                self.speed_radsec = 0
            return False
        self.sensor_value = sensor_value_now
        if self.tick_last_time == -1:
            self.tick_last_time = time_now
            self.tick_last_time_avg = time_now
            return False
        if sensor_value_now == 1:
            if self.USE_BOTH_EDGES:
                # compensate for much shorter time when the sensor is down
                last_time_diff *= 1.8
            else:
                # we count just 1->0 change in this mode (to achieve uniformity between 0 and 1)
                return False
        self.tick_last_time = time_now
        self.speed_radsec = self.RAD_PER_TICK / (last_time_diff / 1_000_000)

        # calculate average speed (simplistic, just accumulate last several ticks once in a while)
        self.tick_count += 1
        if self.tick_count < self.AVG_TICK_COUNT:
            if self.speed_radsec_avg == 0:
                self.speed_radsec_avg = self.speed_radsec
        else:
            last_time_avg_diff = ticks_diff(time_now, self.tick_last_time_avg)
            self.speed_radsec_avg = self.RAD_PER_TICK * self.AVG_TICK_COUNT / (last_time_avg_diff / 1_000_000)
            self.tick_last_time_avg = time_now
            self.tick_count = 0

        self.calc_value = sensor_value_now
        self.calc_tick = self.tick_count
        self.calc_update_count = self.update_count
        if self.speed_radsec > 0 and self.update_count < (4 if self.USE_BOTH_EDGES else 2):
            print("Warning: wheel encoder updating slow, %s counts per change" % self.update_count)
        self.update_count = 0
        return True

    def speed_msec(self):
        """Returns the current wheel speed in m/s."""
        return self.M_PER_WHEEL * self.speed_radsec / self.RAD_PER_WHEEL

    def speed_msec_avg(self):
        """Returns the current wheel speed in m/s."""
        return self.M_PER_WHEEL * self.speed_radsec_avg / self.RAD_PER_WHEEL

    def m2rad(self, m):
        """Converts meters to radians."""
        return self.RAD_PER_WHEEL * m / self.M_PER_WHEEL

    def rad2m(self, rad):
        """Converts radians to meters."""
        return self.M_PER_WHEEL * rad / self.RAD_PER_WHEEL

    def __str__(self):
        return "speed: %f rad/s, %f m/s" % (self.speed_radsec, self.speed_msec())
