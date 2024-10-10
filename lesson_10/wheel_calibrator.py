from time import ticks_ms, ticks_diff, sleep

from wheel import Wheel


class WheelCalibrator:
    def __init__(self, wheel: Wheel):
        """Initializes the wheel calibrator."""
        self.wheel = wheel
        self.pwm_speed_to_rad_per_sec = [0.0 for _ in range(0, 256)]
        self.pwm_speed_min = 0
        self.pwm_speed_max = 0
        self.conversion_table_available = False

    def gather_pwm_to_real_speed_table_all(self):
        """Gathers the real forward and reverse speeds for a desired PWM range
        based on the speedometer readings. Each value is scanned after half a second.
        The calibration fills the conversion table between PWM and rad/s."""
        self.pwm_speed_min = 0.0
        for speed_pwm in range(self.wheel.pwm_min, self.wheel.pwm_max + 1):
            self.calibrate_pwm(speed_pwm=speed_pwm, gather_min=True)
        self.calculate_pwm_value_multiplier_and_shift()
        self.conversion_table_available = True

    def gather_pwm_to_real_speed_table_fast_approx(self):
        """Gathers the approximate forward and reverse speeds for a desired PWM range
        based on the speedometer readings. The range is sampled from bottom to top
        in 10 PWM step intervals to find the lowest moving speed. As a follow-up step,
        the top speed is scanned as well to find the highest moving speed.
        The calibration fills the conversion table between PWM and rad/s using a linear
        approximation. Multiplier (a) and shift (b) are calculated for the equation
        y = a * x + b."""
        #  minimum speed
        speed_pwm = self.wheel.pwm_min
        while speed_pwm <= self.wheel.pwm_max:
            rad_per_sec, cm_per_sec = self.gather_rad_cm_per_sec_for_pwm(speed_pwm)
            self.pwm_speed_to_rad_per_sec[speed_pwm] = rad_per_sec
            if rad_per_sec > 0.0:
                self.pwm_speed_min = speed_pwm
                break
            speed_pwm += 10
        if self.pwm_speed_min == 0:
            print("No movement detected when going through pwm_min .. pwm_max range, %s wheel calibration failed"
                  % self.wheel.name)
            return -1
        if self.pwm_speed_min > self.wheel.pwm_min:
            print("Altering %s wheel pwm_min from %s to %s" % (self.wheel.name, self.wheel.pwm_min, self.pwm_speed_min))
            self.wheel.pwm_min = self.pwm_speed_min

        # maximum speed
        speed_pwm = self.wheel.pwm_max
        rad_per_sec, cm_per_sec = self.gather_rad_cm_per_sec_for_pwm(speed_pwm)
        self.pwm_speed_to_rad_per_sec[speed_pwm] = rad_per_sec
        if rad_per_sec > 0.0:
            self.pwm_speed_max = speed_pwm
        else:
            print("No movement detected on pwm_max speed, %s wheel calibration failed" % self.wheel.name)
            return -1

        # linear approximation in radians per second
        rad_speed_delta = self.pwm_speed_to_rad_per_sec[self.pwm_speed_max] - self.pwm_speed_to_rad_per_sec[
            self.pwm_speed_min]
        a = rad_speed_delta / (self.pwm_speed_max - self.pwm_speed_min)
        b = self.pwm_speed_to_rad_per_sec[self.pwm_speed_min] - a * self.pwm_speed_min
        for speed_pwm in range(self.wheel.pwm_min, self.wheel.pwm_max + 1):
            speed_write = a * speed_pwm + b
            self.pwm_speed_to_rad_per_sec[speed_pwm] = speed_write
        self.calculate_pwm_value_multiplier_and_shift()
        self.conversion_table_available = True

    def calibrate_pwm(self, speed_pwm, gather_min):
        rad_per_sec, cm_per_sec = self.gather_rad_cm_per_sec_for_pwm(speed_pwm)
        self.pwm_speed_to_rad_per_sec[speed_pwm] = rad_per_sec
        if gather_min and rad_per_sec > 0.0 and self.pwm_speed_min == 0:
            self.pwm_speed_min = speed_pwm

    def gather_rad_cm_per_sec_for_pwm(self, speed_pwm):
        """Moves the wheel forward using given PWM speed for half a second,
        returns the speed in rad/s and cm/s."""
        start_time = ticks_ms()
        self.wheel.move_pwm(speed_pwm)
        while ticks_diff(ticks_ms(), start_time) <= 500:
            self.wheel.update()
            sleep(0.001)
        rad_per_sec = self.wheel.get_speed_radians_per_sec()
        cm_per_sec = self.wheel.get_speed_cm_per_sec()
        self.wheel.stop()
        return rad_per_sec, cm_per_sec

    def calculate_pwm_value_multiplier_and_shift(self):
        """
        Calculates pwm multiplier and shift using least squares regression (from valid pwm range).
        multiplier = (count()*sum(pwd*rad) - sum(pwm)*sum(rad)) / (count()*sum(pwm*pwm) - sum(pwm)*sum(pwm))
        shift = (sum(rad) - multiplier*sum(pwm)) / count()
        """
        count = self.wheel.pwm_max - self.wheel.pwm_min + 1
        sum_pwm = 0
        sum_pwm_mult_pwm = 0
        sum_rad = 0
        sum_pwm_mult_rad = 0
        for pwm in range(self.wheel.pwm_min, self.wheel.pwm_max + 1):
            sum_pwm += pwm
            sum_pwm_mult_pwm += pwm * pwm
            sum_rad += self.pwm_speed_to_rad_per_sec[pwm]
            sum_pwm_mult_rad += pwm * self.pwm_speed_to_rad_per_sec[pwm]
        self.wheel.pwm_multiplier = (count * sum_pwm_mult_rad - sum_pwm * sum_rad) / \
                                    (count * sum_pwm_mult_pwm - sum_pwm * sum_pwm)
        self.wheel.pwm_shift = (sum_rad - self.wheel.pwm_multiplier * sum_pwm) / count
        print("Altering %s wheel multiplier: %s, shift: %s" %
              (self.wheel.name, self.wheel.pwm_multiplier, self.wheel.pwm_shift))
