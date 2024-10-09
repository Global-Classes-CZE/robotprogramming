class Task:
    def __init__(self, name: str, tick_time: int | None = None):
        self.__name = name
        self.__tickTime = tick_time
        self._autoNext = False

    def name(self) -> str:
        return self.__name

    def tickTime(self) -> int:
        return self.__tickTime

    def autoNext(self) -> bool:
        return self._autoNext


class Step(Task):
    def __init__(self, name: str, tick_time: int | None = None):
        super().__init__(name, tick_time)
        self._autoNext = True
