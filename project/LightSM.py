from AbstractSM import AbstractSM
from Enum import Color
from LightController import LightController


class LightSM(AbstractSM):
    def __init__(self, lightController: LightController, tasks, tick_time=None):
        self.__lightController = lightController
        super().__init__(tasks, tick_time)

    def __allOff(self):
        self.__lightController.on(range(0, 8), Color.BLACK)

    def __allCarReady(self):
        self.__lightController.on([1, 2], Color.WHITE)
        self.__lightController.on([5, 6], Color.RED)
