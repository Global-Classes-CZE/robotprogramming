from utime import ticks_ms, ticks_us, ticks_diff
from machine import time_pulse_us
import math


class Controller:
    def __init__(self):
        pass


class LIGHT_STATUS:
    STATUS_ON = 1
    STATUS_OFF = 0


class LIGHT_POSITION:
    FRONT_LEFT_INNER = "FLI"
    FRONT_LEFT_OUTER = "FLO"
    FRONT_RIGHT_INNER = "FRI"
    FRONT_RIGHT_OUTER = "FRO"
    REAR_LEFT_INNER = "RLI"
    REAR_LEFT_OUTER = "RLO"
    REAR_RIGHT_INNER = "RRI"
    REAR_RIGHT_OUTER = "RRO"


class LineSensor:
    def __init__(self, key: str):
        self.key = key
        self.__status: bool = False

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: bool):
        self.__status = status


class DIRECTION:
    FORWARD = 0
    BACKWARD = 1
    NONE = -1


class ObstacleSensor:
    pass


class Robot:
    def __init__(
        self,
        wheelDiameterInMeters: float,
        axleTrackInMetres: float,
        i2cBus,
        neopixel,
        pin0,
        pin8,
        pin12,
        pin14,
        pin15,
    ):
        self.__wheelDiameterInMeters = wheelDiameterInMeters
        self.__axleTrackInMetres = axleTrackInMetres / 2
        self.__i2cBus = i2cBus
        self.motorController = MotorController(
            self.__wheelDiameterInMeters, self.__axleTrackInMetres, self.__i2cBus
        )
        self.lightController = LightController(neopixel, pin0)
        self.obstacleController = ObstacleController(self.__i2cBus)
        self.ultrasonicController = UltrasonicController(pin8, pin12)
        self.speedController = SpeedController(pin14, pin15)
        self.lineController = LineController(self.__i2cBus)

    def powerOn(self):
        print("Powering on...")
        if self.__i2cBus is not None:
            self.__i2cBus.init()
        self.lightController.offAll()

    def powerOff(self):
        print("Powering off...")
        self.lightController.offAll()


class SpeedSensor:
    def __init__(self, key: str, pin):
        self.key = key
        self.__pin = pin
        self.__ticks = 0
        self.__ticksPerRotation = 42
        self.__data = -1
        self.__clock = ticks_us()
        self.__period = 1000000
        self.__radiansPerSecond = 0

    def __output(self):
        return self.__pin.read_digital()

    def init(self):
        self.__data = self.__output()
        pass

    def angleSpeed(self):
        ticksNow = ticks_us()
        ticksDiff = ticks_diff(ticksNow, self.__clock)
        if ticksDiff > self.__period:
            rotations = self.__ticks / self.__ticksPerRotation
            radians = (rotations * 2) * math.pi
            self.__radiansPerSecond = radians / (ticksDiff / 1000000)
            self.__clock = ticksNow
            self.__ticks = 0
        return self.__radiansPerSecond

    def readData(self):
        data = self.__output()
        if data >= 0:
            if data != self.__data:
                self.__data = data
                self.__ticks += 1


class UltrasonicSensor:
    def __init__(self):
        self.currentDistance = 0


class Light:
    def __init__(self, key: str, index: int, color: tuple = (0, 0, 0)):
        self.key = key
        self.index = index
        self.color = color
        self.status = LIGHT_STATUS


class LineController(Controller):
    def __init__(self, i2cBus, i2cAddress: bytes = 56):
        super().__init__()
        self.i2cBus = i2cBus
        self.i2cAddress = i2cAddress
        self.__clock = ticks_us()
        self.__period = 1000000
        self.sensors = {
            "LEFT": LineSensor("LEFT"),
            "CENTER": LineSensor("CENTER"),
            "RIGHT": LineSensor("RIGHT"),
        }

    def __output(self):
        return self.i2cBus.read(56, 1)

    def __readData(self):
        data = self.__output()
        data = int.from_bytes(data, "big")
        data = bin(data)
        self.sensors["LEFT"].status = bool(int(data[7]))
        self.sensors["CENTER"].status = bool(int(data[6]))
        self.sensors["RIGHT"].status = bool(int(data[5]))

    def checkStatus(self):
        ticksNow = ticks_us()
        ticksDiff = ticks_diff(ticksNow, self.__clock)
        if ticksDiff > self.__period:
            self.__readData()
            self.__clock = ticksNow
            return (
                self.sensors["LEFT"].status,
                self.sensors["CENTER"].status,
                self.sensors["RIGHT"].status,
            )


class Motor:
    def __init__(self, key: str, position: str):
        self.key = key
        self.position = position
        self.__channelForward = bytes([0])
        self.__channelBackward = bytes([0])
        self.__velocity: float = 0
        self.__pwm: int = 0
        self.__direction = DIRECTION.NONE
        self.__paramA: float = 0
        self.__paramB: float = 0
        if position == "left":
            self.__channelForward = bytes([5])
            self.__channelBackward = bytes([4])
            self.__paramA = 15.15431538
            self.__paramB = 29.85786607
        if position == "right":
            self.__channelForward = bytes([3])
            self.__channelBackward = bytes([2])
            self.__paramA = 15.75436641
            self.__paramB = 35.30530063

    @property
    def channelForward(self):
        return self.__channelForward

    @property
    def channelBackward(self):
        return self.__channelBackward

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value: float):
        self.__velocity = value

    @property
    def pwm(self):
        return self.__pwm

    @pwm.setter
    def pwm(self, value):
        self.__pwm = value

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value

    @property
    def paramA(self):
        return self.__paramA

    @property
    def paramB(self):
        return self.__paramB


class ObstacleController(Controller):
    def __init__(self, i2cBus, i2cAddress: bytes = 56):
        super().__init__()
        self.i2cBus = i2cBus
        self.i2cAddress = i2cAddress
        self.sensors = {"LEFT": ObstacleSensor(), "RIGHT": ObstacleSensor()}

    def checkObstacle(self):
        pass


class SpeedController(Controller):
    def __init__(self, pin14, pin15):
        super().__init__()
        self.__pin14 = pin14
        self.__pin15 = pin15
        self.sensors = {
            "LEFT": SpeedSensor("LEFT", pin14),
            "RIGHT": SpeedSensor("RIGHT", pin15),
        }
        self.sensors["LEFT"].init()
        self.sensors["RIGHT"].init()

    def checkSpeed(self):
        self.sensors["LEFT"].readData()
        self.sensors["RIGHT"].readData()
        return self.sensors["LEFT"].angleSpeed(), self.sensors["RIGHT"].angleSpeed()


class UltrasonicController(Controller):
    def __init__(self, pin8, pin12):
        super().__init__()
        self.__trigger = pin8
        self.__echo = pin12
        self.__clock = ticks_us()
        self.__period = 1000000
        self.sensor = UltrasonicSensor()
        self.soundSpeed = 340
        self.__trigger.write_digital(0)
        self.__echo.read_digital()

    def checkDistanceInMetres(self):
        ticksNow = ticks_us()
        ticksDiff = ticks_diff(ticksNow, self.__clock)
        if ticksDiff > self.__period:
            self.__trigger.write_digital(1)
            self.__trigger.write_digital(0)
            self.__echo.read_digital()
            measuredTimeUs = time_pulse_us(self.__echo, 1)
            if measuredTimeUs < 0:
                return measuredTimeUs
            measuredTimeS = measuredTimeUs / 1000000
            distance = measuredTimeS * self.soundSpeed
            distance = distance / 2
            self.sensor.currentDistance = distance
            self.__clock = ticksNow
        return self.sensor.currentDistance


class LightController(Controller):
    def __init__(self, neopixel, pin0):
        super().__init__()
        self.__neopixel = None
        self.lights = {
            LIGHT_POSITION.FRONT_LEFT_INNER: Light(LIGHT_POSITION.FRONT_LEFT_INNER, 0),
            LIGHT_POSITION.FRONT_LEFT_OUTER: Light(LIGHT_POSITION.FRONT_LEFT_OUTER, 1),
            LIGHT_POSITION.FRONT_RIGHT_OUTER: Light(
                LIGHT_POSITION.FRONT_RIGHT_OUTER, 2
            ),
            LIGHT_POSITION.FRONT_RIGHT_INNER: Light(
                LIGHT_POSITION.FRONT_RIGHT_INNER, 3
            ),
            LIGHT_POSITION.REAR_LEFT_OUTER: Light(LIGHT_POSITION.REAR_LEFT_OUTER, 4),
            LIGHT_POSITION.REAR_LEFT_INNER: Light(LIGHT_POSITION.REAR_LEFT_INNER, 5),
            LIGHT_POSITION.REAR_RIGHT_INNER: Light(LIGHT_POSITION.REAR_RIGHT_INNER, 6),
            LIGHT_POSITION.REAR_RIGHT_OUTER: Light(LIGHT_POSITION.REAR_RIGHT_OUTER, 7),
        }
        self.__indicatorPeriod = 500
        self.__indicatorTime = ticks_ms()
        self.__cycle = 0
        if neopixel is not None:
            self.neopixel = neopixel(pin0, 8)

    def on(self, key: str, color: tuple):
        light: Light = self.lights[key]
        light.status = LIGHT_STATUS.STATUS_ON
        light.color = color
        if self.neopixel is not None:
            self.neopixel[light.index] = color
            self.neopixel.show()

    def off(self, key: str):
        light: Light = self.lights[key]
        light.status = LIGHT_STATUS.STATUS_OFF
        light.color = (0, 0, 0)
        if self.neopixel is not None:
            self.neopixel[light.index] = light.color
            self.neopixel.show()

    def offAll(self):
        for light in self.lights.values():
            self.off(light.key)
        if self.neopixel is not None:
            self.neopixel.show()

    def toggleHeadlightsOn(self):
        light1 = self.lights[LIGHT_POSITION.FRONT_LEFT_INNER]
        light2 = self.lights[LIGHT_POSITION.FRONT_RIGHT_INNER]
        self.on(light1.key, (255, 255, 255))
        self.on(light2.key, (255, 255, 255))

    def toggleHeadlightsOff(self):
        light1 = self.lights[LIGHT_POSITION.FRONT_LEFT_INNER]
        light2 = self.lights[LIGHT_POSITION.FRONT_RIGHT_INNER]
        self.off(light1.key)
        self.off(light2.key)

    def toggleBrakelightsOn(self):
        light1 = self.lights[LIGHT_POSITION.REAR_LEFT_INNER]
        light2 = self.lights[LIGHT_POSITION.REAR_RIGHT_INNER]
        self.on(light1.key, (255, 0, 0))
        self.on(light2.key, (255, 0, 0))

    def toggleBrakelightsOff(self):
        light1 = self.lights[LIGHT_POSITION.REAR_LEFT_INNER]
        light2 = self.lights[LIGHT_POSITION.REAR_RIGHT_INNER]
        self.off(light1.key)
        self.off(light2.key)

    def __turnIndicatorOn(self, light1: Light, light2: Light, cycle: int = 3):
        ticksNow = ticks_ms()
        ticksDiff = ticks_diff(ticksNow, self.__indicatorTime)
        if ticksDiff > self.__indicatorPeriod:
            if self.__cycle < (cycle + 3):
                if light1.status == LIGHT_STATUS.STATUS_ON:
                    self.off(light1.key)
                else:
                    self.on(light1.key, (255, 165, 0))
                self.__indicatorTime = ticksNow
                if light2.status == LIGHT_STATUS.STATUS_ON:
                    self.off(light2.key)
                else:
                    self.on(light2.key, (255, 165, 0))
                self.__indicatorTime = ticksNow
                self.__cycle += 1

    def turnIndicatorLeftOn(self, cycle: int = 3):
        self.turnIndicatorRightOff()
        light1 = self.lights[LIGHT_POSITION.FRONT_LEFT_OUTER]
        light2 = self.lights[LIGHT_POSITION.REAR_LEFT_OUTER]
        self.__turnIndicatorOn(light1, light2, cycle)

    def turnIndicatorLeftOff(self):
        self.off(self.lights[LIGHT_POSITION.FRONT_LEFT_OUTER].key)
        self.off(self.lights[LIGHT_POSITION.REAR_LEFT_OUTER].key)

    def turnIndicatorRightOn(self, cycle: int = 3):
        self.turnIndicatorLeftOff()
        light1 = self.lights[LIGHT_POSITION.FRONT_RIGHT_OUTER]
        light2 = self.lights[LIGHT_POSITION.REAR_RIGHT_OUTER]
        self.__turnIndicatorOn(light1, light2, cycle)

    def turnIndicatorRightOff(self):
        self.off(self.lights[LIGHT_POSITION.FRONT_RIGHT_OUTER].key)
        self.off(self.lights[LIGHT_POSITION.REAR_RIGHT_OUTER].key)


class MotorController(Controller):
    def __init__(
        self,
        wheelDiameterInMeters: float,
        axleTrackInMeters: float,
        i2cBus,
        i2cAddress: bytes = 112,
    ):
        super().__init__()
        self.__wheelDiameterInMeters = wheelDiameterInMeters
        self.__axleTrackInMeters = axleTrackInMeters
        self.__i2cBus = i2cBus
        self.__i2cAddress = i2cAddress
        self.__clocks = {}
        self.__pwm0 = 0
        self.__pwm1 = 0
        self.__pwm2 = 0
        self.__pwm3 = 0
        self.__metersPerSecondInitial: float = 0
        self.__angleSpeedInitial: float = 0
        self.__sonarIsOn: bool = False
        self.motors = {"LEFT": Motor("LEFT", "left"), "RIGHT": Motor("RIGHT", "right")}

    def __normalizePWM(self, pwm: int, minPwm: int = 0, maxPwm: int = 255):
        return max(minPwm, min(pwm, maxPwm))

    def init(self):
        self.__i2cBus.write(self.__i2cAddress, bytes([0, 1]))
        self.__i2cBus.write(self.__i2cAddress, bytes([232, 170]))

    def onClock(self, callbackPeriods=None):
        currentTime = ticks_us()
        if callbackPeriods:
            for (i, (callback, period)) in enumerate(callbackPeriods):
                if i not in self.__clocks:
                    self.__clocks[i] = currentTime
                lastTime = self.__clocks[i]
                if ticks_diff(currentTime, lastTime) > period:
                    callback()
                    self.__clocks[i] = currentTime

    def driveByPWM(self, *args):
        if not args:
            if self.motors["LEFT"].direction == DIRECTION.FORWARD:
                self.__pwm0 = self.motors["LEFT"].pwm
                self.__pwm1 = 0
            else:
                self.__pwm1 = self.motors["LEFT"].pwm
                self.__pwm0 = 0
            if self.motors["RIGHT"].direction == DIRECTION.FORWARD:
                self.__pwm2 = self.motors["RIGHT"].pwm
                self.__pwm3 = 0
            else:
                self.__pwm3 = self.motors["RIGHT"].pwm
                self.__pwm2 = 0
        elif len(args) == 4:
            (self.__pwm0, self.__pwm1, self.__pwm2, self.__pwm3) = args
        self.__i2cBus.write(
            self.__i2cAddress,
            (
                self.motors["LEFT"].channelForward
                + bytes([self.__normalizePWM(self.__pwm0)])
            ),
        )
        self.__i2cBus.write(
            self.__i2cAddress,
            (
                self.motors["LEFT"].channelBackward
                + bytes([self.__normalizePWM(self.__pwm1)])
            ),
        )
        self.__i2cBus.write(
            self.__i2cAddress,
            (
                self.motors["RIGHT"].channelForward
                + bytes([self.__normalizePWM(self.__pwm2)])
            ),
        )
        self.__i2cBus.write(
            self.__i2cAddress,
            (
                self.motors["RIGHT"].channelBackward
                + bytes([self.__normalizePWM(self.__pwm3)])
            ),
        )

    def driveByVelocity(self, metersPerSecond: float, angleSpeed: float):
        if self.__metersPerSecondInitial == 0:
            self.__metersPerSecondInitial = metersPerSecond
        if self.__angleSpeedInitial == 0:
            self.__angleSpeedInitial = angleSpeed
        self.motors["LEFT"].velocity = metersPerSecond - (
            self.__axleTrackInMeters * angleSpeed
        )
        self.motors["LEFT"].velocity /= self.__wheelDiameterInMeters / 2
        self.motors["RIGHT"].velocity = metersPerSecond + (
            self.__axleTrackInMeters * angleSpeed
        )
        self.motors["RIGHT"].velocity /= self.__wheelDiameterInMeters / 2
        self.motors["LEFT"].pwm = int(
            (
                (self.motors["LEFT"].paramA * abs(self.motors["LEFT"].velocity))
                + self.motors["LEFT"].paramB
            )
        )
        self.motors["RIGHT"].pwm = int(
            (
                (self.motors["RIGHT"].paramA * abs(self.motors["RIGHT"].velocity))
                + self.motors["RIGHT"].paramB
            )
        )
        if self.motors["LEFT"].velocity == 0:
            self.motors["LEFT"].pwm = 0
        if self.motors["RIGHT"].velocity == 0:
            self.motors["RIGHT"].pwm = 0
        if self.motors["LEFT"].velocity > 0:
            self.motors["LEFT"].direction = DIRECTION.FORWARD
        else:
            self.motors["LEFT"].direction = DIRECTION.BACKWARD
        if self.motors["RIGHT"].velocity > 0:
            self.motors["RIGHT"].direction = DIRECTION.FORWARD
        else:
            self.motors["RIGHT"].direction = DIRECTION.BACKWARD
        self.driveByPWM()

    def driveWithRegulator(self, speed: tuple, P: int = 28):
        (y1, y2) = speed
        if (round(float(y1), 1) != 0.0) and (round(float(y2), 1) != 0.0):
            if self.motors["LEFT"].velocity < 0:
                y1 *= -1
            if self.motors["RIGHT"].velocity < 0:
                y2 *= -1
            error1 = self.motors["LEFT"].velocity - y1
            error2 = self.motors["RIGHT"].velocity - y2
            u1 = int((P * error1))
            u2 = int((P * error2))
            if self.motors["LEFT"].direction == DIRECTION.BACKWARD:
                u1 *= -1
            if self.motors["RIGHT"].direction == DIRECTION.BACKWARD:
                u2 *= -1
            self.motors["LEFT"].pwm += u1
            self.motors["RIGHT"].pwm += u2
            self.driveByPWM()

    def driveWithSonar(
        self, distanceInMetres: float, metersFromObstacle: float = 0.2, P: float = 0.5
    ):
        if distanceInMetres > 0:
            r = -metersFromObstacle
            y = -distanceInMetres
            e = r - y
            u = P * e
            if u > self.__metersPerSecondInitial:
                u = self.__metersPerSecondInitial
            self.driveByVelocity(u, self.__angleSpeedInitial)

    def driveWithLineDetection(self, status: tuple, angleSpeed: float):
        (left, center, right) = status
        if left:
            self.driveByVelocity(self.__metersPerSecondInitial, angleSpeed)
        if right:
            self.driveByVelocity(self.__metersPerSecondInitial, (-angleSpeed))
