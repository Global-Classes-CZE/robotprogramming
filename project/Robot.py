from LightController import LightController
from MoveController import MoveController

from Encoder import Encoder

from StateLight import StateLight


class Robot:
    def __init__(self, wheelSpan, wheelDiameter):
        self.__lightController = LightController()
        self.__moveController = MoveController(wheelSpan, wheelDiameter)
        self.__encoder = Encoder(wheelDiameter)
        # self.__stateLight = StateLight(self.__lightController).setTask('robotInit')
        # self.__init()

    # def __init(self):
    #     self.__stateLight = StateLight(self)

    #
    # def tick(self):

    def goPWM(self, pwm, rotation=0):
        self.__moveController.go(pwm, rotation)

    def light(self) -> LightController:
        return self.__lightController

    def encoder(self) -> Encoder:
        return self.__encoder

    def tick(self):
        self.__encoder.tick()
        # self.__stateLight.tick()
