from SensorReader import SensorReader
from Period import Period


class Encoder:
    def __init__(self, wheelDiameter):
        self.__wheelEncoder = WheelEncoder(wheelDiameter)

    def tick(self):
        self.__wheelEncoder.tick()


class WheelEncoder:
    TICK_PERIOD = 1000
    RIPS = 16  # pocet der

    def __init__(self, wheelDiameter: float):
        self.__period = Period(WheelEncoder.TICK_PERIOD)
        self.__lastData = [0, 0]
        self.__countData = [0, 0]
        self.__speed = [0, 0]
        ticks = 2 * WheelEncoder.RIPS
        resolutionDegree = 360 / ticks
        circumference = 3.141592 * wheelDiameter
        self.__oneTickDistance = (resolutionDegree / 360) * circumference

    def getSpeed(self) -> list:
        coef = (1000 / self.__speed[2]) * self.__oneTickDistance
        return [
            self.__speed[0] * coef,
            self.__speed[1] * coef,
        ]

    def tick(self):
        data = SensorReader.getWheelState()
        for i in [0, 1]:
            if data[i] != self.__lastData[i]:
                self.__countData[i] += 1
        self.__lastData = data

        if self.__period.isTime():
            self.__speed = self.__countData
            self.__speed += [self.__period.getLastDiff()]
            self.__countData = [0, 0]
