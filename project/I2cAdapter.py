from microbit import i2c, pin19, pin20


class I2cAdapter:
    __needInit = True

    @staticmethod
    def __initIfNeeded():
        if I2cAdapter.__needInit:
            i2c.init(freq=400000, sda=pin20, scl=pin19)
            I2cAdapter.__needInit = False

    @staticmethod
    def write(addr, buff, repeat=False):
        I2cAdapter.__initIfNeeded()
        i2c.write(addr, buff, repeat)

    @staticmethod
    def read(addr, n: int, repeat=False):
        I2cAdapter.__initIfNeeded()
        return i2c.read(addr, n, repeat)
