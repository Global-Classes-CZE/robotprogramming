from microbit import pin14, pin15


class SensorReader:
    # def __init__(self):

    @staticmethod
    def getWheelState() -> list:
        return [pin14.read_digital(), pin15.read_digital()]
