from microbit import pin8, pin12, pin14, pin15
from machine import time_pulse_us

from I2cAdapter import I2cAdapter


class SensorReader:
    LTL = 'LTL'  # LINE_TRACKER_LEFT
    LTM = 'LTM'  # LINE_TRACKER_MIDDLE
    LTR = 'LTR'  # LINE_TRACKER_RIGHT
    OL = 'OL'  # OBSTACLE_LEFT
    OR = 'OR'  # OBSTACLE_RIGHT

    @staticmethod
    def getWheelState() -> list:
        return [pin14.read_digital(), pin15.read_digital()]

    @staticmethod
    def getSensors() -> object:
        # Read hexadecimal data and convert to binary
        data = "{0:b}".format(ord(I2cAdapter.read(0x38, 1)))
        return {
            # 'SpeedLeft': data[7],
            # 'SpeedRight': data[6],
            SensorReader.LTL: data[5],
            SensorReader.LTM: data[4],
            SensorReader.LTR: data[3],
            SensorReader.OL: data[2],
            SensorReader.OR: data[1],
            # 'Buzzer': data[0],
        }


class UltrasoundReader:
    def __init__(self):
        self.__triggerPin = pin8
        self.__echoPin = pin12

        self.__triggerPin.write_digital(0)
        self.__echoPin.read_digital()

    def getDistance(self) -> int:
        self.__triggerPin.write_digital(0)
        self.__triggerPin.write_digital(1)

        stopwatch = time_pulse_us(self.__echoPin, 1)
        if stopwatch < 0:
            return stopwatch

        duration = stopwatch / 1000000  # prevedeme na vteriny
        distance = (duration * 343) / 2  # rychlost zvuku 34300
        return round(distance, 3)
