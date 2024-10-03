class QItem:
    def __init__(self, name: str, period: int = 0):
        self.__name = name
        self.__period = period
        self.__repeat = 1

    def getName(self) -> str:
        return self.__name

    def getPeriod(self) -> int:
        return self.__period

    def decreaseRepeat(self, n: int = 1):
        if self.__repeat > 0:
            self.__repeat = max(self.__repeat - n, 0)

    def getRepeat(self) -> bool:
        return self.__repeat

    def period(self, n: int):
        self.__period = n
        return self

    def repeat(self, n: int):
        self.__repeat = n
