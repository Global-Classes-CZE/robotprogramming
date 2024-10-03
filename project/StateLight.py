from StateAbstract import StateAbstract
from Enum import Color
from LightController import LightController
from QItem import QItem


class StateLight(StateAbstract):
    def __init__(self, lightController: LightController):
        super().__init__()
        self.__lightController = lightController

    def __robotInit__init(self):
        self.addInstance(self.__lightController).setQueue([
            QItem('allWhite', 1000),
            QItem('allYellow'),
            QItem('allOff', 250),
            QItem('allCar'),
            QItem('allYellow',250),
            QItem('allWhite', 250),
            QItem('allYellow',250),
            QItem('allWhite', 250),
            QItem('allYellow',250),
            QItem('allWhite', 250),
            QItem('allCar'),
        ], 500)
        # self.setQueue([
        #     QItem('allWhite'),
        #     QItem('allYellow'),
        #     QItem('allOff', 2000),
        #     QItem('allCar'),
        # ], 500)

    def __robotInit(self):
        if self.isQueueEmpty():
            self.setState('end')

    def __allWhite(self):
        self.__lightController.on(range(0, 8), Color.WHITE)

    def __allYellow(self):
        self.__lightController.on(range(0, 8), Color.YELLOW)

    def __allOff(self):
        self.__lightController.on(range(0, 8), Color.BLACK)

    def __allCar(self):
        self.__lightController.on([1, 2], Color.WHITE)
        self.__lightController.on([5, 6], Color.RED)
