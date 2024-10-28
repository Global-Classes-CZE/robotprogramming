from wheel import Wheel
from system import System


class WheelCalibrator:
    def __init__(self, system: System, wheel: Wheel):
        """Initializes the wheel calibrator."""
        self.system = system
        self.wheel = wheel
        self.p2m2radsec = [0.0 for _ in range(wheel.pwm_min, wheel.pwm_max + 1)]
        self.pwm_min = 0
        self.pwm_max = 0
        self.conversion_table_available = False

    def gather_pwm_to_real_speed_table_full(self):
        """Gathers the real forward and reverse speeds for a desired PWM range
        based on the encoder readings. Each value is scanned after half a second.
        The calibration fills the conversion table between PWM and rad/s."""
        self.pwm_min = 0.0
        for speed_pwm in range(self.wheel.pwm_min, self.wheel.pwm_max + 1):
            self.calibrate_pwm(speed_pwm=speed_pwm, gather_min=True)
        self.calculate_pwm_value_multiplier_and_shift()
        self.conversion_table_available = True

    def gather_pwm_to_real_speed_table_approx(self):
        """Gathers the approximate forward and reverse speeds for a desired PWM range
        based on the encoder readings. The range is sampled from bottom to top
        in 10 PWM step intervals to find the lowest moving speed. As a follow-up step,
        the top speed is scanned as well to find the highest moving speed.
        The calibration fills the conversion table between PWM and rad/s using a linear
        approximation. Multiplier (a) and shift (b) are calculated for the equation
        y = a * x + b."""
        #  minimum speed
        speed_pwm = self.wheel.pwm_min
        while speed_pwm <= self.wheel.pwm_max:
            radsec, msec = self.gather_rad_msec_for_pwm(speed_pwm)
            self.p2m2radsec[speed_pwm - self.wheel.pwm_min] = radsec
            if radsec > 0.0:
                self.pwm_min = speed_pwm
                break
            speed_pwm += 10
        if self.pwm_min == 0:
            print("No movement detected when going through pwm_min .. pwm_max range, %s wheel calibration failed"
                  % self.wheel.name)
            return -1
        if self.pwm_min > self.wheel.pwm_min:
            print("Altering %s wheel pwm_min from %s to %s" % (self.wheel.name, self.wheel.pwm_min, self.pwm_min))
            self.wheel.pwm_min = self.pwm_min

        # maximum speed
        speed_pwm = self.wheel.pwm_max
        radsec, msec = self.gather_rad_msec_for_pwm(speed_pwm)
        self.p2m2radsec[speed_pwm - self.wheel.pwm_min] = radsec
        if radsec > 0.0:
            self.pwm_max = speed_pwm
        else:
            print("No movement detected on pwm_max speed, %s wheel calibration failed" % self.wheel.name)
            return -1

        # linear approximation in radians per second
        rad_speed_delta = (self.p2m2radsec[self.pwm_max - self.wheel.pwm_min]
                           - self.p2m2radsec[0])
        a = rad_speed_delta / (self.pwm_max - self.pwm_min)
        b = self.p2m2radsec[0] - a * self.pwm_min
        for speed_pwm in range(self.wheel.pwm_min, self.wheel.pwm_max + 1):
            speed_write = a * speed_pwm + b
            self.p2m2radsec[speed_pwm - self.wheel.pwm_min] = speed_write
        self.calculate_pwm_value_multiplier_and_shift()
        self.conversion_table_available = True

    def calibrate_pwm(self, speed_pwm, gather_min):
        radsec, msec = self.gather_rad_msec_for_pwm(speed_pwm)
        self.p2m2radsec[speed_pwm - self.wheel.pwm_min] = radsec
        if gather_min and radsec > 0.0 and self.pwm_min == 0:
            self.pwm_min = speed_pwm

    def gather_rad_msec_for_pwm(self, speed_pwm):
        """Moves the wheel forward using given PWM speed for half a second,
        returns the speed in rad/s and m/s."""
        start_time = self.system.ticks_us()
        self.wheel.move_pwm(speed_pwm)
        while self.system.ticks_diff(self.system.ticks_us(), start_time) <= 500_000:
            self.wheel.update()
        radsec = self.wheel.enc.speed_radsec
        msec = self.wheel.enc.speed_msec()
        self.wheel.stop()
        return radsec, msec

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
            sum_rad += self.p2m2radsec[pwm - self.wheel.pwm_min]
            sum_pwm_mult_rad += pwm * self.p2m2radsec[pwm - self.wheel.pwm_min]
        self.wheel.pwm_multiplier = (count * sum_pwm_mult_rad - sum_pwm * sum_rad) / \
                                    (count * sum_pwm_mult_pwm - sum_pwm * sum_pwm)
        self.wheel.pwm_shift = (sum_rad - self.wheel.pwm_multiplier * sum_pwm) / count
        print("Altering %s wheel multiplier: %s, shift: %s" %
              (self.wheel.name, self.wheel.pwm_multiplier, self.wheel.pwm_shift))

    def calibration_table_to_csv(self):
        print("CSV calibration data for %s wheel (pwm_min = %s, multiplier = %s, shift = %s):"
              % (self.wheel.name, self.wheel.pwm_min, self.wheel.pwm_multiplier, self.wheel.pwm_shift))
        print("pwm,radsec,msec")
        for pwm in range(self.wheel.pwm_min, self.wheel.pwm_max + 1):
            #  We just print the calibration data for the border values (min 5, max 5)
            if pwm < self.wheel.pwm_min + 5 or pwm > self.wheel.pwm_max - 5:
                radsec = self.p2m2radsec[pwm - self.wheel.pwm_min]
                msec = self.wheel.enc.rad2m(radsec)
                print("%d,%f,%f" % (pwm, radsec, msec))
