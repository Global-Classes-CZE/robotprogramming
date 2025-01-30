from Period import Period
from Task import Task
from CPU import CPU


class AbstractSM:
    STATE_START = 'start'
    STATE_END = 'end'

    def __init__(self, tasks: list[Task] | None = None, time_tick: int | None = None):
        self.__period = Period()
        self.__tickTimeDefault = 0
        self.__periodQueue = Period()
        self.__stack = []
        self.__curTask = None  # type: Task | None
        self.__cpu_no = None  # type: int | None
        self.__ntid = None  # Next Time ID
        self.__running = False
        self.__tic = 0  # task id counter
        if isinstance(tasks, list):
            self.setTasks(tasks, time_tick)

    def __start(self):
        pass

    def __end(self):
        self.__cleanSelf()

    def __cleanSelf(self):
        parent = CPU.parentOf(self.__cpu_no)
        if parent:
            parent.cpu_child_done(self.__cpu_no)
        CPU.remove(self.__cpu_no)

    def add2CPU(self, sm: 'AbstractSM') -> 'AbstractSM':
        # prida noveho potomka do SQM
        return CPU.add(sm, self.__cpu_no)

    def run(self):
        self.__period.reset()
        self.__running = True
        self.nextTask()

    def cpu_child_done(self, cpu_no: int):
        # bude provolana, kdykoliv se dokonci ukoly v SQM potomkovi
        pass

    def cpu_no(self, cpu_no: int = None) -> int | None:
        if cpu_no is None:
            return self.__cpu_no
        self.__cpu_no = cpu_no

    def tick(self):
        if self.__running is False:
            return
        if self.__curTask and self.__period.isTime():
            self.__ntid = self.__curTask.id()
            self.__callStep(self.__curTask.name() + '__tick')
            if self.__curTask.autoNext() and self.__ntid == self.__curTask.id():
                self.nextTask()

    def setTask(self, task: Task):
        if self.__curTask is not None:
            self.__callStep(self.__curTask.name() + '__end')
        self.__tic += 1
        task.id(self.__tic)
        self.__curTask = task
        t = task.tickTime()
        self.setTickTime(self.__tickTimeDefault if t is None else t)
        self.__callStep(task.name())

    def setTasks(self, tasks: list[Task] | None = None, tick_time: int | None = None):
        self.__period.reset()
        self.__tickTimeDefault = tick_time
        self.__stack = tasks if isinstance(tasks, list) else []
        if self.__running:
            self.nextTask()

    def nextTask(self):
        if self.__stack:
            self.setTask(self.__stack.pop(0))
            return
        self.setTask(Task('end'))

    def __callStep(self, name: str):
        n = '__' + name
        if hasattr(self, n):
            # print('call: ', n)
            fce = getattr(self, n)
            fce()

    def setTickTime(self, n: int | None):
        self.__period.setTickTime(n)
