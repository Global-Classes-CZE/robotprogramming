from microbit import i2c, pin19, pin20


class I2cAdapter:
    __needInit = True

    @staticmethod
    def write(addr, buff, repeat=False):
        if I2cAdapter.__needInit:
            i2c.init(freq=400000, sda=pin20, scl=pin19)
        i2c.write(addr, buff, repeat)
