from microbit import button_a
from utime import ticks_us, ticks_diff

from sonar import Sonar
from wheel_driver import WheelDriver

if __name__ == "__main__":
    # Tries to maintain the robot around 20 cm in front of an obstacle.
    # We use Sonar to measure distance to the obstacle and gradually increase
    # the speed of the robot to 50 cm/s. We also support backing off when too close.
    # We allow for +/- 3 cm around the target distance to avoid oscillation.

    # The wheels are controlled individually and we are trying to keep the robot
    # going straight, so we are aiming at keeping speed in radians constant for both wheels.
    DISTANCE_DESIRED = 0.2
    DISTANCE_TOLERANCE = 0.03
    DISTANCE_MAX = 0.6
    # with 30 cm/s the robot was a bit sluggish and was not able to respond well
    SPEED_M_MAX = 0.5
    SPEED_M_MIN = 0.25
    SPEED_CHANGE_SLOPE = 1

    # We use three basic robot modes.
    # If the target is lost (distance too high), the robot stops and starts scanning for the target
    # in its surrounding area using sonar scanner feature. Once the target is found, the robot
    # reorients itself to the right angle and starts following the target again.
    ROBOT_MODE_FOLLOW = "follow"
    ROBOT_MODE_SCAN = "scan"
    ROBOT_MODE_TURN = "turn"

    wheels = WheelDriver(left_pwm_min=60, left_pwm_multiplier=0.08944848, left_pwm_shift=-2.722451,
                         right_pwm_min=60, right_pwm_multiplier=0.08349663, right_pwm_shift=-2.0864)
    sonar = Sonar()
    try:
        # Calculate the constants for radsec speed dependency on the distance to ensure
        # the robot won't go fast when the distance is small.
        # When the distance is 50 cm, the speed should be 0.4 m/s.
        # When the distance is 20 cm, the speed should be 0.2 m/s.
        speed_rad_max = wheels.left.enc.m2rad(SPEED_M_MAX)
        speed_rad_min = wheels.left.enc.m2rad(SPEED_M_MIN)
        distance_m_to_speed_radsec = (speed_rad_max - speed_rad_min) / (DISTANCE_MAX - DISTANCE_DESIRED)

        info_cycle_length = 1_000_000
        info_cycle_start = ticks_us()
        regulation_cycle_length = 50_000
        regulation_cycle_start = ticks_us()

        distance = None
        robot_mode = ROBOT_MODE_FOLLOW
        print("Switching robot mode to %s" % robot_mode)
        while not button_a.is_pressed():
            wheels.update()
            sonar.update()

            time_now = ticks_us()
            if ticks_diff(time_now, regulation_cycle_start) > regulation_cycle_length:
                regulation_cycle_start = time_now
                if robot_mode == ROBOT_MODE_TURN:
                    # We are in the turning mode, we need to wait until the robot reorients itself
                    # around its center using equal, but opposite left and right wheel speeds (after compensation).
                    print("Turning, left speed %d, right speed %d" % (wheels.left.speed_pwm, wheels.right.speed_pwm))
                    if wheels.left.speed_pwm == 0 and wheels.right.speed_pwm == 0:
                        robot_mode = ROBOT_MODE_FOLLOW
                        print("Switching robot mode to %s" % robot_mode)
                        sonar.set_angle(0)
                elif robot_mode == ROBOT_MODE_SCAN:
                    distance = sonar.get_distance()
                    if distance < 0:
                        # the distance is not valid, we might have lost the target, stop the robot
                        wheels.stop()
                    if distance < DISTANCE_MAX and sonar.angle != 0:
                        # the target is found, stop the scanner and reorient the robot
                        sonar.stop_scan()
                        print("Found target at distance %.04f at angle %s" % (distance, sonar.angle))
                        if sonar.angle == 0:
                            robot_mode = ROBOT_MODE_FOLLOW
                            print("Switching robot mode to %s" % robot_mode)
                        else:
                            robot_mode = ROBOT_MODE_TURN
                            print("Switching robot mode to %s" % robot_mode)
                            # we need to calculate circular distance to travel with each wheel to reorient the robot
                            # around its center using equal, but opposite left and right wheel speeds (after compensation).
                            # To do so, we need to know the wheel distance from the center of the robot.
                            angle_in_rad = sonar.angle * 3.141592653589793 / 180
                            rad_to_travel = wheels.left.enc.WHEEL_CENTER_DISTANCE * angle_in_rad
                            if sonar.angle > 0:
                                wheels.left.move_radsec_for_distance(speed_rad_min, rad_to_travel)
                                wheels.right.move_radsec_for_distance(-speed_rad_min, rad_to_travel)
                            elif sonar.angle < 0:
                                wheels.left.move_radsec_for_distance(-speed_rad_min, abs(rad_to_travel))
                                wheels.right.move_radsec_for_distance(speed_rad_min, abs(rad_to_travel))
                elif robot_mode == ROBOT_MODE_FOLLOW:
                    distance = sonar.get_distance()
                    if distance < 0:
                        # the distance is not valid, we might have lost the target, stop the robot
                        wheels.stop()
                    elif distance > DISTANCE_MAX:
                        # the target is lost, stop the robot, start the scanner
                        wheels.stop()
                        if sonar.scan_mode == sonar.SCAN_NONE:
                            sonar.start_scan()
                        robot_mode = ROBOT_MODE_SCAN
                        print("Switching robot mode to %s" % robot_mode)
                    else:
                        # the back-off distance is very small, we would normally probably use minimal speed,
                        # but it might not work due to the wheel calibration, so we still try to use the same error
                        # correction as for the forward movement. We can use the same mechanism and just indicate
                        # negative pwm speed to move backwards (thanks to our Wheel implementation).
                        if (distance > DISTANCE_DESIRED + DISTANCE_TOLERANCE) or \
                                (distance < DISTANCE_DESIRED - DISTANCE_TOLERANCE):
                            distance_error = distance - DISTANCE_DESIRED
                            desired_speed_radsec = abs(distance_error) * distance_m_to_speed_radsec + speed_rad_min

                            current_speed_radsec_left = wheels.left.enc.speed_radsec_avg
                            speed_error_radsec_left = desired_speed_radsec - current_speed_radsec_left
                            speed_change_radsec_left = SPEED_CHANGE_SLOPE * speed_error_radsec_left
                            # print("Current speed %f, Desired speed %f, Speed change left %f" % (current_speed_radsec_left, desired_speed_radsec, speed_change_radsec_left))
                            new_speed_radsec_left = min(current_speed_radsec_left + speed_change_radsec_left,
                                                        speed_rad_max)
                            new_speed_pwm_left = wheels.left.radsec2pwm(new_speed_radsec_left)

                            current_speed_radsec_right = wheels.right.enc.speed_radsec_avg
                            speed_error_radsec_right = desired_speed_radsec - current_speed_radsec_right
                            speed_change_radsec_right = SPEED_CHANGE_SLOPE * speed_error_radsec_right
                            new_speed_radsec_right = min(
                                current_speed_radsec_right + speed_change_radsec_right,
                                speed_rad_max
                            )
                            # print("Current speed %f, Desired speed %f, Speed change right %f" % (current_speed_radsec_right, desired_speed_radsec, speed_change_radsec_right))
                            new_speed_pwm_right = wheels.right.radsec2pwm(new_speed_radsec_right)

                            if distance_error > 0:
                                wheels.left.move_pwm_for_distance(new_speed_pwm_left, distance_error)
                                wheels.right.move_pwm_for_distance(new_speed_pwm_right, distance_error)
                            else:
                                wheels.left.move_pwm_for_distance(-new_speed_pwm_left, abs(distance_error))
                                wheels.right.move_pwm_for_distance(-new_speed_pwm_right, abs(distance_error))
                        else:
                            wheels.stop()

            if ticks_diff(time_now, info_cycle_start) > info_cycle_length:
                info_cycle_start = time_now
                speed_msec_left = wheels.left.enc.speed_msec()
                speed_msec_right = wheels.right.enc.speed_msec()
                print("Distance: %.04fm, speed: L=%.04fm/s, R=%.04fm/s" % (distance, speed_msec_left, speed_msec_right))
    finally:
        wheels.stop()
        sonar.set_angle(0)
        print("Finished")
