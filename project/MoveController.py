from Motor import Motor
from I2cAdapter import I2cAdapter


class MoveController:
    __ADDRESS = 0x70

    def __init__(self, wheelSpan, wheelDiameter):
        self.__motorL = Motor(MoveController.__ADDRESS, b'\x03', b'\x02')
        self.__motorR = Motor(MoveController.__ADDRESS, b'\x05', b'\x04')
        self.__d = wheelSpan / 2

    def __init(self):
        self.__i2cWrite(b'\x00\x01')
        self.__i2cWrite(b'\xE8\xAA')
        self.__motorL.stop()
        self.__motorR.stop()

    def __i2cWrite(self, buff):
        I2cAdapter.write(MoveController.__ADDRESS, buff)

    def go(self, speed, rotation):
        v_l = speed - self.__d * rotation
        v_r = speed + self.__d * rotation
        print(speed, rotation, v_l, v_r)
        if not -255 <= v_l <= 255:
            return -1
        if not -255 <= v_r <= 255:
            return -1
        self.__motorL.go(int(v_l))
        self.__motorR.go(int(v_r))
