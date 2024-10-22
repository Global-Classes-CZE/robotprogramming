import math

from microbit import sleep

from Period import Period
from Servo import Servo
from Task import Task
from SensorReader import UltrasoundReader
from AbstractSM import AbstractSM
from Robot import Robot


class MoveSM(AbstractSM):
    def __init__(self, robot: Robot, tasks, tick_time):
        self.__robot = robot
        super().__init__(tasks, tick_time)

        self.__counter = 0

    __carrotChasingSM = None

    def __carrotChasing(self):
        self.__carrotChasingSM = CarrotChasingSM(self.__robot, [
            Task('run')
        ], 30)
        self.add2CPU(self.__carrotChasingSM)

    def __cruiseControl(self):
        Servo.rotate(0)
        self.__robot.move().goV(0.4)

    __lastY = 0

    def __cruiseControl__tick(self):  # Tempomat
        v_min_error = 0.005  # m/s - prepoctu 1 tik na radiany → prepoctu na rychlost
        distance_max_error = 0.01  # m error senzoru
        # p = v_min_error / distance_max_error
        p = 0.7

        r = -0.2  # 20 cm pred prekazkou se chci zastavit
        v_max = 0.5  # rychleji jet nechci

        y = UltrasoundReader().getDistance()  # aktualni hodnota
        if y < 0:
            return

        e = r + y
        u = e * p

        v = max(min(v_max, u), v_max * -1)

        # print('y=' + str(y), 'e=' + str(e), 'p=' + str(p), 'u=' + str(u), 'v=' + str(v))
        print((y, e, u, v))
        skip = y > 2 > self.__lastY
        self.__lastY = y
        if skip:
            print('SKIP')
            print((5, 5, 5, 5))
            return

        # print((y,))
        self.__robot.move().goV(v)

    def __forward(self):
        self.__robot.move().goV(0)

    def __left(self):
        self.__robot.move().goV(0)

    def __right(self):
        self.__robot.move().goV(0)

    def __stop(self):
        self.__robot.move().goV(0)


class CarrotChasingSM(AbstractSM):

    def __init__(self, robot, tasks, tick_time=None):
        self.__robot = robot
        self.__ul = UltrasoundReader()

        self.__curAngle = 0
        self.__rotate = True
        super().__init__(tasks, tick_time)

    def __run(self):
        pass

    __distances = {}


    def __run__tick(self):
        distance = self.__ul.getDistance() * 1000

        d = int(round(distance / 5)) * 5
        if not d in self.__distances:
            self.__distances[d] = []
        self.__distances[d].append(Servo.angle())

        self.__curAngle += 5 if self.__rotate else -5
        Servo.rotate(round(self.__curAngle))

        if abs(self.__curAngle) > 60:
            distance = min(self.__distances)
            arr = self.__distances[distance]
            direction = (max(arr) + min(arr)) / 2
            self.__distances = {}
            self.__rotate = not self.__rotate

            if distance == 0:
                return
            dx = math.cos(math.radians(direction)) * distance
            dy = math.sin(math.radians(direction)) * distance
            rel_x = dx + 70  # 7 cm je sensor predsunut
            rel_y = dy + 0
            robot_angle_rad = math.atan(rel_y / rel_x)
            print((robot_angle_rad * 10, direction, distance))
            self.__robot.move().goV(0.05 if distance > 100 else 0, robot_angle_rad)
