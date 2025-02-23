from wheel_driver import WheelDriver
from wheel_calibrator import WheelCalibrator


# Naimplemenetujte funkci kalibrace() motoru,
# která změří závislost mezi PWM a rad/s a
# proloží ji přímkou
def kalibrace_plna(wheel_calibrator: WheelCalibrator):
    wheel_calibrator.gather_pwm_to_real_speed_table_all()


# Stejna funkce, ale rychla varianta -
# scanuje nejmensi PWM od zvoleneho minima (60) po 10. Po nalezeni prvniho
# nenuloveho pohybu zmeri i nejrychlejsi pohyb.
def kalibrace_approx(wheel_calibrator: WheelCalibrator):
    wheel_calibrator.gather_pwm_to_real_speed_table_fast_approx()


def calibration_table_to_csv(wheel_name: str, wheel_calibrator):
    wheel = wheel_calibrator.wheel
    print("CSV calibration data for %s wheel (pwm_min = %s, multiplier = %s, shift = %s):"
          % (wheel_name, wheel.pwm_min, wheel.pwm_multiplier, wheel.pwm_shift))
    print("pwm,rad_sec,cm_sec")
    for pwm in range(wheel.pwm_min, wheel.pwm_max + 1):
        #  We just print the calibration data for the border values (min 5, max 5)
        if pwm < wheel.pwm_min + 5 or pwm > wheel.pwm_max - 5:
            rad = wheel_calibrator.pwm_speed_to_rad_per_sec[pwm]
            cm = wheel.speedometer.radians_to_cm(rad)
            print("%d,%f,%f" % (pwm, rad, cm))


if __name__ == "__main__":
    wheel_driver = WheelDriver()
    try:
        kalibrace_approx(wheel_driver.wheel_calibrator_left)
        calibration_table_to_csv(wheel_name="left", wheel_calibrator=wheel_driver.wheel_calibrator_left)

        kalibrace_approx(wheel_driver.wheel_calibrator_right)
        calibration_table_to_csv(wheel_name="right", wheel_calibrator=wheel_driver.wheel_calibrator_right)
    finally:
        wheel_driver.stop()
