from joycar import Robot
from neopixel import NeoPixel
from microbit import sleep
from microbit import pin0, pin8, pin12, pin14, pin15
from microbit import i2c
from microbit import button_a

robot = Robot(
    wheelDiameterInMeters=0.067,
    axleTrackInMetres=0.15,
    i2cBus=i2c,
    neopixel=NeoPixel,
    pin0=pin0,
    pin8=pin8,
    pin12=pin12,
    pin14=pin14,
    pin15=pin15,
)

robot.powerOn()
robot.motorController.init()

robot.motorController.driveByVelocity(0, 0)
sleep(1000)

robot.motorController.driveByVelocity(0.15, 0)
sleep(1000)

while not button_a.was_pressed():

    speed = robot.speedController.checkSpeed()
    distance = robot.ultrasonicController.checkDistanceInMetres()

    robot.motorController.onClock(
        [
            (lambda: robot.motorController.driveWithRegulator(speed, P=10), 500000),
            (lambda: robot.motorController.driveWithSonar(distance), 1000000),
        ]
    )
    sleep(5)
robot.motorController.driveByVelocity(0, 0)

robot.powerOff()
