from Task import Task
from SensorReader import UltrasoundReader
from StateAbstract import StateAbstract
from Robot import Robot


class StateMove(StateAbstract):
    def __init__(self, robot: Robot, tasks, tick_time):
        self.__robot = robot
        super().__init__(tasks, tick_time)

        self.__counter = 0

    def __cruiseControl(self):
        self.__robot.move().goV(0.4)

    def __cruiseControl__tick(self):  # Tempomat
        v_min_error = 0.005  # m/s - prepoctu 1 tik na radiany → prepoctu na rychlost
        distance_max_error = 0.01  # m error senzoru
        p = v_min_error / distance_max_error

        r = -0.2  # 20 cm pred prekazkou se chci zastavit
        v_max = 0.5  # rychleji jet nechci

        y = UltrasoundReader().getDistance()  # aktualni hodnota
        if y < 0:
            return

        e = r + y
        u = e * p

        v = max(min(v_max, u), v_max * -1)

        # print('y=' + str(y), 'e=' + str(e), 'p=' + str(p), 'u=' + str(u), 'v=' + str(v))
        self.__robot.move().goV(v)

    def __forward(self):
        self.__robot.move().goV(0)

    def __left(self):
        self.__robot.move().goV(0)

    def __right(self):
        self.__robot.move().goV(0)

    def __stop(self):
        self.__robot.move().goV(0)
