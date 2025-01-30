from AbstractSM import AbstractSM
from Robot import Robot
from LightSM import LightSM
from Task import Task, Step
from MoveSM import MoveSM


class MainSM(AbstractSM):

    def __init__(self, robot: Robot, tasks, tick_time=None):
        self.__robot = robot
        super().__init__(tasks, tick_time)

    def __init(self):
        self.add2CPU(LightSM(self.__robot.light(), [
            Step('allOff'),
            Step('allCarReady'),
        ]))

    def __run(self):
        sm = MoveSM(self.__robot, [
            Step('stop',1000),
            Task('cruiseControl', 250),
            # Task('carrotChasing', 2000),
            Step('stop'),
            # Step('right'),
        ], 1000)
        self.add2CPU(sm)

    def tick(self):
        self.__robot.tick()
        super().tick()

    def cpu_child_done(self, cpu_no: int):
        print('cpu_child_done', cpu_no)
