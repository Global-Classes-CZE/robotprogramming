from machine import time_pulse_us
from microbit import pin1, pin8, pin12
from utime import ticks_us, ticks_diff


class Sonar:
    """Handles the ultrasonic sensor HC-SR04 to measure distance in m.
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

    SCAN_NONE = 'none'
    SCAN_WIDENING = 'widening'
    SCAN_FULL = 'full'
    SCAN_STEP = 5
    # We need to find the object at least this many times before we accept it
    SCAN_DISTANCE_ACCEPTED_AFTER_FOUND_COUNT = 2

    def __init__(self, trigger_pin=pin8, echo_pin=pin12, angle_pin=pin1, scan_range_max=0.5, scan_interval=125_000):
        self.trigger_pin = trigger_pin
        self.trigger_pin.write_digital(0)
        self.echo_pin = echo_pin
        self.echo_pin.read_digital()
        self.angle_pin = angle_pin
        self.angle = 0
        self.set_angle(0)
        self.scan_mode = self.SCAN_NONE
        self.scan_last_time = -1
        self.scan_interval = scan_interval
        self.scan_range_max = scan_range_max
        self.scan_angle_start = 0
        self.scan_direction = 1
        self.scan_dispersion = 0
        self.scan_distance_found_count = 0

    def set_angle(self, angle):
        """Sets sonar angle from -90 to 90"""
        angle = angle if angle >= -91 else -90
        angle = angle if angle <= 90 else 90
        servo_value = self.SERVO_MAX - self.SERVO_STEP * (angle + 90)
        print("Setting sonar angle to %d (value %d)" % (angle, servo_value))
        self.angle_pin.write_analog(servo_value)
        self.angle = angle

    def get_distance(self):
        """Returns the distance in meters measured by the sensor."""
        self.trigger_pin.write_digital(1)
        self.trigger_pin.write_digital(0)

        measured_time_us = time_pulse_us(self.echo_pin, 1)
        if measured_time_us < 0:
            return measured_time_us

        measured_time_sec = measured_time_us / 1_000_000
        return measured_time_sec * self.SOUND_SPEED / 2

    def start_scan(self):
        """Starts the scanning mode."""
        self.scan_mode = self.SCAN_WIDENING
        self.scan_angle_start = self.angle
        self.scan_direction = 1
        self.scan_dispersion = 0
        self.scan_last_time = -1
        print("Scanning started")

    def stop_scan(self):
        """Stops the scanning mode."""
        self.scan_mode = self.SCAN_NONE
        print("Scanning stopped")

    def update(self):
        """Updates itself based on the current scan mode and elapsed time."""
        if self.scan_mode == self.SCAN_NONE:
            return
        time_now = ticks_us()
        if self.scan_last_time != -1 and ticks_diff(time_now, self.scan_last_time) < self.scan_interval:
            return
        self.scan_last_time = time_now

        distance = self.get_distance()
        if distance < 0:
            print("Error %f while getting distance" % distance)
            self.scan_distance_found_count = 0
            return

        # we have the object, reorient future scanning to this angle, return to widening mode
        if distance < self.scan_range_max:
            self.scan_distance_found_count += 1
            if self.scan_distance_found_count < self.SCAN_DISTANCE_ACCEPTED_AFTER_FOUND_COUNT:
                return
            print("Object detected at %f m" % distance)
            self.scan_mode = self.SCAN_WIDENING
            self.scan_direction = 1
            self.scan_dispersion = 0
            self.scan_angle_start = self.angle
            return
        else:
            self.scan_distance_found_count = 0

        # gradually widening scan on both sides until we cover full area, then switch to full scan left-right-left
        if self.scan_mode == self.SCAN_WIDENING:
            self.scan_dispersion += self.SCAN_STEP
            new_angle = self.scan_angle_start + self.scan_dispersion * self.scan_direction
            if (abs(new_angle) <= 90):
                self.set_angle(new_angle)
                self.scan_direction *= -1
            else:
                # we reached the end of the scan on one side, we will also finish the other side
                self.scan_direction *= -1
                new_angle = self.scan_angle_start + self.scan_dispersion * self.scan_direction
                if (abs(new_angle) <= 90):
                    self.set_angle(new_angle)
                else:
                    # we reached the end of the scan on the other side, we will start scanning the full area
                    self.scan_mode = self.SCAN_FULL
                    print("Switching to full scan")
                    self.set_angle(-90)
                    self.scan_direction = 1

        if self.scan_mode == self.SCAN_FULL:
            new_angle = self.angle + (self.SCAN_STEP * 2) * self.scan_direction
            if (abs(new_angle) <= 90):
                self.set_angle(new_angle)
            else:
                self.scan_direction *= -1
