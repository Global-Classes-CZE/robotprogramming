from LightController import LightController
from MoveController import MoveController
from microbit import sleep

from Encoder import Encoder
from utime import ticks_ms, ticks_diff

class Robot:
    def __init__(self, wheelSpan, wheelDiameter):
        self.__lightController = LightController()
        self.__moveController = MoveController(wheelSpan, wheelDiameter)
        self.__encoder = Encoder(wheelDiameter)
        # self.__init()

    # def __init(self):
    #
    # def tick(self):

    def go(self, speed, rotation=0):
        self.__moveController.go(speed, rotation)

    def tick(self):
        self.__encoder.tick()
        sleep(5)

