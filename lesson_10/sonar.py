from microbit import pin1, pin8, pin12, button_a
from machine import time_pulse_us
from time import sleep

class Sonar:
    """Handles the ultrasonic sensor HC-SR04 to measure distance in cm.
    Based on https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf,
    The sensor operates at freq 40Hz and supports ranges from 2cm to 400cm,
    with 0.3cm resolution and 3mm precision, providing a viewing angle of 15 degrees.
    The sensor uses the speed of sound in the air to calculate the distance.
    Trigger Input Signal 10uS TTL pulse is used to start the ranging,
    and the module will send out an 8 cycle burst of ultrasound at 40 kHz
    and raise its echo. The Echo Output Signal is an input TTL lever signal
    and the range in proportion to the duration of the echo signal."""
    SOUND_SPEED = 343  # m/s
    SERVO_MIN = 20  # right
    SERVO_MAX = 128  # left
    SERVO_STEP = (SERVO_MAX - SERVO_MIN) / 180

    def __init__(self, trigger_pin=pin8, echo_pin=pin12, angle_pin=pin1):
        self.trigger_pin = trigger_pin
        self.trigger_pin.write_digital(0)
        self.echo_pin = echo_pin
        self.echo_pin.read_digital()
        self.angle_pin = angle_pin
        self.set_angle(0)

    def set_angle(self, angle):
        """Sets sonar angle, use -90 to 90"""
        angle = angle if angle >= -91 else -90
        angle = angle if angle <= 90 else 90
        servo_value = self.SERVO_MAX - self.SERVO_STEP * (angle + 90)
        print("Setting sonar angle to %d (value %d)" % (angle, servo_value))
        self.angle_pin.write_analog(servo_value)

    def get_distance_cm(self):
        self.trigger_pin.write_digital(1)
        self.trigger_pin.write_digital(0)

        measured_time_us = time_pulse_us(self.echo_pin, 1)
        if measured_time_us < 0:
            return measured_time_us

        measured_time_sec = measured_time_us / 1000000
        distance_cm = 100 * measured_time_sec * self.SOUND_SPEED / 2
        return distance_cm


if __name__ == "__main_test_sonar_angles__":
    sonar = Sonar()
    for angle in range(-90, 90):
        sonar.set_angle(angle)
        sleep(0.25)

if __name__ == "__main_get_distance__":
    sonar = Sonar()
    while not button_a.is_pressed():
        distance_cm = sonar.get_distance_cm()
        if distance_cm < 0:
            # Error processing the distance, stop the movement
            print("Error %f while getting distance value" % distance_cm)
        else:
            print("Distance %f" % sonar.get_distance_cm())
        sleep(0.25)
