from Task import Task, Step
from Robot import Robot
from microbit import button_a
from MainSM import MainSM
from CPU import CPU

if __name__ == "__main__":
    robot = Robot(0.147, 0.067)
    stateMain = MainSM(robot, [
        Step('init'),
        Step('battery', 500),
        Task('run'),
    ])
    CPU.add(stateMain)

    while not button_a.was_pressed():
        CPU.tick()

    robot.move().goV(0)
