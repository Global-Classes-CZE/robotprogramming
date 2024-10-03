from LightController import LightController
from MoveController import MoveController

from Encoder import Encoder

from StateLight import StateLight


class Robot:
    def __init__(self, wheelSpan, wheelDiameter):
        self.__lightController = LightController()
        self.__moveController = MoveController(wheelSpan, wheelDiameter)
        self.__encoder = Encoder(wheelDiameter)
        self.__stateLight = StateLight(self.__lightController).setState('robotInit')
        # self.__init()

    # def __init(self):
    #     self.__stateLight = StateLight(self)

    #
    # def tick(self):

    def go(self, speed, rotation=0):
        self.__moveController.go(speed, rotation)

    def light(self) -> LightController:
        return self.__lightController

    def tick(self):
        self.__encoder.tick()
        self.__stateLight.tick()
