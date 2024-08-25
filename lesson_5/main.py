from Robot import Robot
from microbit import sleep

if __name__ == "__main__":
    robot = Robot()
    robot.zapni_svetla()
    sleep(2000)
    robot.vypni_svetla()
    robot.brzdi()
    sleep(2000)
    robot.vypni_svetla()
    robot.indikuj("left")
    sleep(5000)
    robot.vypni_svetla()
    robot.indikuj("right")
    sleep(5000)
    robot.vypni_svetla()
