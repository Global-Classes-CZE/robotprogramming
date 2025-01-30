from SensorReader import SensorReader
from Period import Period


class WheelEncoder:
    RIPS = 20  # pocet der

    def __init__(self, wheelDiameter: float):
        self.__period = Period(500)
        self.__lastData = [0, 0]
        self.__countData = [0, 0, 0, 0, 0, 0, 0]  # [0,1][2,3,4][5,6]
        self.__speedData = [0, 0, 0]
        self.__speed = [0, 0]
        ticks = 2 * WheelEncoder.RIPS
        resolutionDegree = 360 / ticks
        circumference = 3.141592 * wheelDiameter
        self.__oneTickDistance = (resolutionDegree / 360) * circumference

    def getSpeed(self) -> list:
        return [
            self.__countData[5],
            self.__countData[6],
        ]

    def getDistance(self) -> list:
        return [
            self.__countData[0] * self.__oneTickDistance,
            self.__countData[1] * self.__oneTickDistance,
        ]

    # def getSpeed(self) -> list:
    #     coef = (1000 / self.__speed[2]) * self.__oneTickDistance
    #     return [
    #         self.__speed[0] * coef,
    #         self.__speed[1] * coef,
    #     ]

    def tick(self):
        data = SensorReader.getWheelState()
        for i in [0, 1]:
            if data[i] != self.__lastData[i]:
                self.__countData[i] += 1
        self.__lastData = data

        if self.__period.isTime():
            curTime = self.__period.getTime()
            diff = (curTime - self.__countData[4]) / 1000
            # print(self.__countData, diff, self.__oneTickDistance, (self.__countData[0] - self.__countData[2]))
            self.__countData[5] = ((self.__countData[0] - self.__countData[2]) * self.__oneTickDistance) / diff
            self.__countData[6] = ((self.__countData[1] - self.__countData[3]) * self.__oneTickDistance) / diff

            self.__countData[2] = self.__countData[0]
            self.__countData[3] = self.__countData[1]
            self.__countData[4] = curTime
        #     self.__speed = self.__countData
        #     self.__speed += [self.__period.getLastDiff()]
        #     self.__countData = [0, 0]


# class UltrasoundEncoder:
#     def __init__(self):


class Encoder:
    def __init__(self, wheelDiameter):
        self.__wheelEncoder = WheelEncoder(wheelDiameter)

    def wheel(self) -> WheelEncoder:
        return self.__wheelEncoder

    def tick(self):
        self.__wheelEncoder.tick()
