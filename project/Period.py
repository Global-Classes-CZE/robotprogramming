from utime import ticks_ms, ticks_diff


class Period:
    def __init__(self, period: int = 0):
        self.__period = period
        self.__periodOriginal = None
        self.__lastTime = 0
        self.__lastDiff = 0

    def isTime(self) -> bool:
        if self.__period == 0:
            return False
        tickMs = ticks_ms()
        ticksDiff = ticks_diff(tickMs, self.__lastTime)

        if ticksDiff >= self.__period:
            self.__lastTime = tickMs
            self.__lastDiff = ticksDiff
            return True
        return False

    def getLastDiff(self) -> int:
        return self.__lastDiff

    def setPeriod(self, n: int):
        self.__period = self.__periodOriginal = n

    def setPeriodTemporary(self, n: [int, None]):
        self.__period = n if n is not None else self.__periodOriginal
