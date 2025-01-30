from microbit import pin1


class Servo:
    __isInited = False
    __angle = 0

    @staticmethod
    def angle():
        return Servo.__angle

    @staticmethod
    def rotate(angle):
        Servo.__angle = angle
        if Servo.__isInited is False:
            pin1.set_analog_period(20)
        # power = Servo.__scale(angle, -90, 90, 44, 248)
        power = Servo.__scale(angle, -90, 90, 22, 125)
        pin1.write_analog(power)
        # pin1.write_analog(Servo.__scale(angle, 90, -90, 90, 120))
        # pin1.write_analog(21)
        # pin1.write_analog(124)
        # pin1.write_analog(72.5)
        # pin1.write_analog(73)

    @staticmethod
    def __scale(num, in_min, in_max, out_min, out_max):
        return round(((num - in_min) * ((out_max - out_min) / (in_max - in_min))) + out_min)
