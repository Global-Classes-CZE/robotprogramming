from Task import Task
from SensorReader import UltrasoundReader
from StateAbstract import StateAbstract
from Robot import Robot


class StateMove(StateAbstract):
    def __init__(self, robot: Robot, tasks, tick_time):
        self.__robot = robot
        super().__init__(tasks, tick_time)

    def __cruiseControl(self):
        self.__robot.goPWM(130)

    def __cruiseControl__tick(self):
        print('__cruiseControl__tick')



        r = -0.2  # reference 20 cm
        y = UltrasoundReader().getDistance()  # aktualni hodnota
        e = r - y  # error
        max_pwm = 135  # max PWM je 255, ale ja chci jen 135
        max_error = 1.2  # zpomaluj 1.2 m pred prekazkou
        p = max_pwm / max_error
        max_action_hit = p * max_error  # maximalni akcni zasah
        u = e * p  # akcni zasah
        pwm = min(max_pwm, int(u))
        print('y=' + str(y), 'e=' + str(e), 'p=' + str(p), 'u=' + str(u), 'pwn=' + str(pwm))
        self.__robot.goPWM(pwm)
    #
    #     # distance =
    #     # pwmBase = 130
    #     # error = distance - 20
    #     # self.__robot.goPWM(130)

    def __forward(self):
        self.__robot.goPWM(200)

    def __left(self):
        self.__robot.goPWM(0, -1000)

    def __right(self):
        self.__robot.goPWM(0, 1000)

    def __stop(self):
        self.__robot.goPWM(0)
