from wheel_driver import WheelDriver

# Naimplemenetujte funkci kalibrace() motoru,
# která změří závislost mezi PWM a rad/s a
# proloží ji přímkou
def kalibrace(wheel_driver: WheelDriver):
    wheel_driver.gather_pwm_to_real_speed_table()
    print("CSV calibration data for left wheel:")
    print("pwm,cm_sec,rad_sec")
    pwm_to_cm = wheel_driver.wheel_left.get_pwm_speed_to_cm_per_sec_table()
    pwm_table_start = wheel_driver.wheel_left.pwm_speed_to_cm_per_sec_start
    pwm_table_end = wheel_driver.wheel_left.pwm_speed_to_cm_per_sec_end
    for pwm in range(pwm_table_start, pwm_table_end + 1):
        cm = pwm_to_cm[pwm]
        rad = wheel_driver.wheel_left.speedometer.cm_to_radians(cm)
        print("%d,%f,%f" % (pwm, cm, rad))
    print("CSV calibration data for right wheel:")
    print("pwm,cm_sec,rad_sec")
    pwm_to_cm = wheel_driver.wheel_right.get_pwm_speed_to_cm_per_sec_table()
    pwm_table_start = wheel_driver.wheel_right.pwm_speed_to_cm_per_sec_start
    pwm_table_end = wheel_driver.wheel_right.pwm_speed_to_cm_per_sec_end
    for pwm in range(pwm_table_start, pwm_table_end + 1):
        cm = pwm_to_cm[pwm]
        rad = wheel_driver.wheel_right.speedometer.cm_to_radians(cm)
        print("%d,%f,%f" % (pwm, cm, rad))

if __name__ == "__main__":
    wheel_driver = WheelDriver()
    try:
        kalibrace(wheel_driver)
    except Exception:
        wheel_driver.stop()
        raise
