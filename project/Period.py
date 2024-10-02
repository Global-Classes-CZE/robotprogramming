from utime import ticks_ms, ticks_diff


class Period:
    def __init__(self, period: int):
        self.__period = period
        self.__lastTime = 0
        self.__lastDiff = 0

    def isTime(self) -> bool:
        tickMs = ticks_ms()
        ticksDiff = ticks_diff(tickMs, self.__lastTime)

        if ticksDiff >= self.__period:
            self.__lastTime = tickMs
            self.__lastDiff = ticksDiff
            return True
        return False

    def getLastDiff(self) -> int:
        return self.__lastDiff
