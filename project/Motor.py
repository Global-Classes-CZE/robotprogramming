from time import sleep

from I2cAdapter import I2cAdapter


class Motor:
    def __init__(self, address, addressForward, addressBack):
        self.__address = address
        self.__addressForward = addressForward
        self.__addressBack = addressBack

    def go(self, speed):
        I2cAdapter.write(self.__address, self.__addressForward + bytes([speed if speed > 0 else 0]))
        I2cAdapter.write(self.__address, self.__addressBack + bytes([speed * -1 if speed < 0 else 0]))

    def stop(self):
        self.go(0)
