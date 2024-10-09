from utime import ticks_ms, ticks_diff


class Period:
    def __init__(self, tick_time: [int, None] = None):
        self.__tickTime = tick_time
        self.__lastTime = 0
        self.__lastDiff = 0

    def isTime(self) -> bool:
        if self.__tickTime is None:
            return True
        tickMs = ticks_ms()
        ticksDiff = ticks_diff(tickMs, self.__lastTime)
        if ticksDiff >= self.__tickTime:
            self.__lastTime = tickMs
            self.__lastDiff = ticksDiff
            return True
        return False

    def reset(self):
        self.__lastTime = ticks_ms()

    def getLastDiff(self) -> int:
        return self.__lastDiff

    def setTickTime(self, n: [int, None]):
        self.__tickTime = n
