from StateAbstract import StateAbstract
from Enum import Color
from LightController import LightController
from Task import Task


class StateLight(StateAbstract):
    def __init__(self, lightController: LightController):
        super().__init__()
        self.__lightController = lightController

    def __robotInit(self):
        self.addInstance(StateLight(self.__lightController)).setTasks([
            Task('allOff'),
            Task('allCarReady'),
        ], 500)

    def __robotInit__tick(self):
        if self.isQueueEmpty():
            self.setTask('end')

    def __allOff(self):
        self.__lightController.on(range(0, 8), Color.BLACK)

    def __allCarReady(self):
        self.__lightController.on([1, 2], Color.WHITE)
        self.__lightController.on([5, 6], Color.RED)
