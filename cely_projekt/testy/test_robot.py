from microbit import button_a, sleep
from robot import Robot
from konstanty import Konstanty

def zakladni_test_spusteni():
    robot = Robot(0.15, 0.067)
    robot.inicializuj()
    navratova_hodnota = robot.jed(0.067*Konstanty.PI, 0)
    print("navratova hodnota jed", navratova_hodnota)
    while not button_a.was_pressed():
        sleep(5)

    robot.jed(0,0)

if __name__ =="__main__":
    zakladni_test_spusteni()
