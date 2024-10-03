from Period import Period
from QItem import QItem


class StateAbstract:
    STATE_START = 'start'
    STATE_END = 'end'

    def __init__(self, period: int = 1000, queue: list[QItem] = None):
        self.__period = Period(period)
        self.__periodQueue = Period()
        self.__curState = None
        self.__queue = queue if isinstance(queue, list) else []  # type: list[QItem]
        self.__curQItem = None  # type: [QItem, None]
        self.__instances = []  # type: list[StateAbstract]

    def __start(self):
        pass

    def __end(self):
        print('END')
        self.__curQItem = None
        self.__queue = []
        self.setPeriod(0)
        self.setPeriodQueue(0)

    def tick(self):
        if self.__period.isTime() and self.__curState is not None:
            fce = getattr(self, '__' + self.__curState)
            if fce: fce()

        if self.__periodQueue.isTime():
            if self.__curQItem:

                newPeriod = self.__curQItem.getPeriod()
                self.setPeriodQueueTemporary(newPeriod if newPeriod > 0 else None)

                self.__curQItem.getName()
                fce = getattr(self, '__' + self.__curQItem.getName())
                if fce: fce()
                self.__curQItem.decreaseRepeat()
                if self.__curQItem.getRepeat() is 0:
                    if self.__queue:
                        self.__curQItem = self.__queue.pop(0)
                    else:
                        self.__curQItem = None

        for index, item in enumerate(self.__instances):
            item.tick()
            if item.isEmpty():
                del self.__instances[index]

    def setState(self, state: str):
        if self.__curState is not None:
            outFce = getattr(self, '__' + self.__curState + '__leave', None)
            if outFce: outFce()

        self.__curState = state

        inFce = getattr(self, '__' + state + '__init', None)
        if inFce: inFce()
        return self

    def setQueue(self, queue: [list[QItem], None] = None, periodQueue: [int, None] = None):
        if periodQueue is not None: self.setPeriodQueue(periodQueue)
        self.__queue = queue if isinstance(queue, list) else []
        if self.__queue:
            self.__curQItem = self.__queue.pop(0)

    def setPeriod(self, n: int):
        self.__period.setPeriod(n)

    def setPeriodQueue(self, n: int):
        self.__periodQueue.setPeriod(n)

    def setPeriodQueueTemporary(self, n: [int, None]):
        self.__periodQueue.setPeriodTemporary(n)

    def addInstance(self, *args, **kwargs) -> 'StateAbstract':
        newInstance = self.__class__(*args, **kwargs)
        self.__instances.append(newInstance)
        return newInstance

    def isQueueEmpty(self):
        return self.__curQItem is None

    def isEmpty(self):
        return self.__curQItem is None and self.__curState is None
