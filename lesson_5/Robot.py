from microbit import sleep
from Light import Light, IndicatorDirectionEnum, HeadLightEnum


class Robot:
    def __init__(self):
        self.light = Light()

    def indikuj(self, smer_zataceni):
        if smer_zataceni == "doprava":
            self.light.indikuj(IndicatorDirectionEnum.RIGHT)
        elif smer_zataceni == "doleva":
            self.light.indikuj(IndicatorDirectionEnum.LEFT)
        else:
            self.light.indikuj(IndicatorDirectionEnum.NONE)

    def zapni_svetla(self):
        self.light.zapni_potkavaci()

    def brzdi(self):
        self.light.zapni_brzdy()
        sleep(2000)
        self.light.vypni_brzdy()

    def vypni_svetla(self):
        self.light.vypni_potkavaci()

if __name__ == "__main__":
    robot = Robot()
    while True:
        robot.vypni_svetla()
        sleep(3000)
        robot.zapni_svetla()
        sleep(3000)
        robot.brzdi()
        sleep(3000)
        for i in range(300):
            robot.indikuj("doleva")
            sleep(10)
        for i in range(300):
            robot.indikuj("doprava")
            sleep(10)
        for i in range(100):
            robot.indikuj("rovne")
            sleep(10)
