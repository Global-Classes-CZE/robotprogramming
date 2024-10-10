from time import ticks_ms, ticks_diff

from microbit import button_a

from sonar import Sonar
from wheel_driver import WheelDriver

#  Naimplementujte adaptivní tempomat s využitím třídy Robot
#  a dalších vzorových kódů. Využijte zpětné vazby a regulátoru P.
#
# Robot by měl
# - Udržovat minimální vzdálenost 0.2m před překážkou
# - Zastavit se a případně rozjet vzad, pokud je překážka moc blízko
# - Omezit maximální rychlost na 0.3 m/s
if __name__ == "__main__":
    wheel_driver = WheelDriver(left_pwm_min=60, left_pwm_multiplier=0.1809153, left_pwm_shift=-5.509312,
                               right_pwm_min=60, right_pwm_multiplier=0.1628194, right_pwm_shift=-5.216122)
    sonar = Sonar()
    try:
        # Tries to maintain the robot around 20 cm in front of an obstacle.
        # We use Sonar to measure distance to the obstacle and gradually increase
        # Speed of the robot to 30 cm/s. We also support backing off when too close.
        # We allow for +/- 2 cm around the target distance to avoid oscillation.

        # The wheels are controlled individually and we are trying to keep the robot
        # going straight, so we are aiming at keeping speed in radians constant for
        # both wheels.
        distance_cm_desired = 20
        distance_cm_tolerance = 2
        distance_cm_max = 50
        # with 30 cm/s the robot was a bit sluggish and was not able to respond well
        # (I might need to calibrate the wheels, try different batteries or verify the speedometer conversion code)
        speed_cm_max = 40
        speed_cm_min = 20
        # any wheel can provide below conversion
        speed_rad_max = wheel_driver.wheel_left.speedometer.cm_to_radians(speed_cm_max)
        speed_rad_min = wheel_driver.wheel_left.speedometer.cm_to_radians(speed_cm_min)
        speed_change_slope = 2

        # Calculate the constants for rad_sec speed dependency on the distance to ensure
        # the robot won't go fast when the distance is small.
        # When the distance is 50 cm, the speed should be 0.4 m/s.
        # When the distance is 20 cm, the speed should be 0.2 m/s.
        distance_cm_to_speed_rad_sec = (speed_rad_max - speed_rad_min) / (distance_cm_max - distance_cm_desired)

        info_cycle_length = 1000
        info_cycle_start = ticks_ms()
        regulation_cycle_length = 200
        regulation_cycle_start = ticks_ms()

        distance_cm = None
        while not button_a.is_pressed():
            wheel_driver.update()

            if ticks_diff(ticks_ms(), regulation_cycle_start) > regulation_cycle_length:
                regulation_cycle_start = ticks_ms()
                distance_cm = sonar.get_distance_cm()
                if distance_cm > distance_cm_max:
                    wheel_driver.stop()
                else:
                    # the back-off distance is very small, we would normally probably use minimal speed,
                    # but it might not work due to the wheel calibration, so we still try to use the same error
                    # correction as for the forward movement. We can use the same mechanism and just indicate
                    # negative pwm speed to move backwards (thanks to our Wheel implementation).
                    if (distance_cm > distance_cm_desired + distance_cm_tolerance) or \
                        (distance_cm < distance_cm_desired - distance_cm_tolerance):
                        distance_cm_error = distance_cm - distance_cm_desired
                        desired_speed_rad_sec = abs(distance_cm_error) * distance_cm_to_speed_rad_sec + speed_rad_min

                        current_speed_rad_sec_left = wheel_driver.wheel_left.speedometer.get_speed_radians_per_sec()
                        speed_error_rad_sec_left = desired_speed_rad_sec - current_speed_rad_sec_left
                        speed_change_rad_sec_left = speed_change_slope * speed_error_rad_sec_left
                        # print("Current speed %f, Desired speed %f, Speed change left %f" % (current_speed_rad_sec_left, desired_speed_rad_sec, speed_change_rad_sec_left))
                        new_speed_rad_sec_left = min(current_speed_rad_sec_left + speed_change_rad_sec_left, speed_rad_max)
                        new_speed_pwm_left = wheel_driver.wheel_left.rad_per_sec_to_pwm_speed(new_speed_rad_sec_left)

                        current_speed_rad_sec_right = wheel_driver.wheel_right.speedometer.get_speed_radians_per_sec()
                        speed_error_rad_sec_right = desired_speed_rad_sec - current_speed_rad_sec_right
                        speed_change_rad_sec_right = speed_change_slope * speed_error_rad_sec_right
                        new_speed_rad_sec_right = min(current_speed_rad_sec_right + speed_change_rad_sec_right, speed_rad_max)
                        # print("Current speed %f, Desired speed %f, Speed change right %f" % (current_speed_rad_sec_right, desired_speed_rad_sec, speed_change_rad_sec_right))
                        new_speed_pwm_right = wheel_driver.wheel_right.rad_per_sec_to_pwm_speed(new_speed_rad_sec_right)

                        if distance_cm_error > 0:
                            wheel_driver.move_pwm_for_distance(new_speed_pwm_left, new_speed_pwm_right, distance_cm_error)
                        else:
                            wheel_driver.move_pwm_for_distance(-new_speed_pwm_left, -new_speed_pwm_right, abs(distance_cm_error))
                    else:
                        wheel_driver.stop()

            if ticks_diff(ticks_ms(), info_cycle_start) > info_cycle_length:
                info_cycle_start = ticks_ms()
                speed_cm_left = wheel_driver.wheel_left.get_speed_cm_per_sec()
                speed_cm_right = wheel_driver.wheel_right.get_speed_cm_per_sec()
                print("Distance: %f cm, speed: L=%.2f cm/s, R=%.2f cm/s" % (distance_cm, speed_cm_left, speed_cm_right))
        print("Done")
    finally:
        wheel_driver.stop()
