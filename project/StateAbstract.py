from Period import Period
from Task import Task
from SMQ import SMQ


class StateAbstract:
    STATE_START = 'start'
    STATE_END = 'end'

    def __init__(self, tasks: list[Task] | None = None, time_tick: int | None = None):
        self.__period = Period()
        self.__tickTimeDefault = 0
        self.__periodQueue = Period()
        self.__stack = []
        self.__curTask = None  # type: Task | None
        self.__smq_no = None  # type: int | None
        self.__reqNextTask = False
        if isinstance(tasks, list):
            self.setTasks(tasks, time_tick)

    def __start(self):
        pass

    def __end(self):
        self.__cleanSelf()

    def __cleanSelf(self):
        parent = SMQ.parentOf(self.__smq_no)
        if parent:
            parent.smq_child_done(self.__smq_no)
        SMQ.remove(self.__smq_no)

    def add2SMQ(self, sm: 'StateAbstract') -> 'StateAbstract':
        # prida noveho potomka do SQM
        return SMQ.add(sm, self.__smq_no)

    def smq_child_done(self, smq_no: int):
        # bude provolana, kdykoliv se dokonci ukoly v SQM potomkovi
        pass

    def smq_no(self, smq_no: int = None) -> int | None:
        if smq_no is None:
            return self.__smq_no
        self.__smq_no = smq_no

    def tick(self):
        if self.__curTask and self.__period.isTime():
            self.__reqNextTask = self.__curTask.autoNext()
            self.__callStep(self.__curTask.name() + '__tick')
            if self.__reqNextTask:
                self.nextTask()

    def setTask(self, task: Task):
        if self.__curTask is not None:
            self.__callStep(self.__curTask.name() + '__end')
        self.__curTask = task
        t = task.tickTime()
        self.setTickTime(self.__tickTimeDefault if t is None else t)
        self.__callStep(task.name())

    def setTasks(self, tasks: list[Task] | None = None, tick_time: int | None = None):
        self.__period.reset()
        self.__tickTimeDefault = tick_time
        self.__stack = tasks if isinstance(tasks, list) else []
        self.nextTask()

    def nextTask(self):
        self.__reqNextTask = False
        if self.__stack:
            self.setTask(self.__stack.pop(0))
            return
        self.setTask(Task('end'))

    def __callStep(self, name: str):
        n = '__' + name
        if hasattr(self, n):
            fce = getattr(self, n)
            fce()

    def setTickTime(self, n: int | None):
        self.__period.setTickTime(n)
