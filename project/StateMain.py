from StateAbstract import StateAbstract
from Robot import Robot
from StateLight import StateLight
from Task import Task, Step
from StateMove import StateMove


class StateMain(StateAbstract):

    def __init__(self, robot: Robot, tasks, tick_time=None):
        self.__robot = robot
        super().__init__(tasks, tick_time)

    def __init(self):
        self.add2SMQ(StateLight(self.__robot.light(), [
            Step('allOff'),
            Step('allCarReady'),
        ]))

    def __run(self):
        sm = StateMove(self.__robot, [
            Step('stop',1000),
            Task('cruiseControl', 250),
            Step('stop'),
            # Step('right'),
        ], 1000)
        self.add2SMQ(sm)

    def tick(self):
        self.__robot.tick()
        super().tick()

    def smq_child_done(self, smq_no: int):
        print('smq_child_done', smq_no)
