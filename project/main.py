# from time import sleep
import math

from Servo import Servo
from Task import Task, Step
from Robot import Robot
from microbit import button_a, sleep, button_b

from Period import Period
from SensorReader import UltrasoundReader

from MainSM import MainSM
from SensorReader import SensorReader
from CPU import CPU

# from StateMain import StateMain

if __name__ == "__main__":
    robot = Robot(0.147, 0.067)
    stateMain = MainSM(robot, [
        Step('init'),
        Task('run'),
    ])
    CPU.add(stateMain)
    # robot.goPWM(150)
    # period = Period(1000)
    # ul = UltrasoundReader()
    #
    # angle = -45
    # rotate = True
    # while not button_b.was_pressed():
    #     pass
    #
    # while not button_a.is_pressed():
    #     robot.move().goPWM(150)
    #     sleep(1)
    #     robot.move().goPWM(0)
    #     sleep(2)
    #
    # robot.move().goPWM(80)
    # while not button_b.is_pressed():
    #     pass



    while not button_a.was_pressed():
        CPU.tick()
        # angle += 1 if rotate else -1
        # Servo.otoc(angle)
        # sleep(5)
        # print(ul.getDistance())
        # if abs(angle) > 45:
        #     rotate = not rotate

        # min_angle = 45  # degree
        # distance = 0.6  # meter
        # dx = math.cos(min_angle) * distance
        # dy = math.sin(min_angle) * distance
        # rel_x = dx + 0.07  # 7 cm je sensor predsunut
        # rel_y = dy + 0
        # robot_angle_rad = math.atan(rel_y / rel_x)
        # print('rel_x', rel_x, 'rel_y', rel_y, 'robot_angle_rad', robot_angle_rad)
        # robot.move().goV(0.3, robot_angle_rad)
        # sleep(2000)
        # robot.move().goV(0)
        # sleep(5000)

        # print('D:', ul.getDistance())

        # for i in range(37, 160):
        #     print(i)
        #     Servo.otoc(i)
        #     sleep(1000)
        # Servo.otoc(45)
        # sleep(1000)
        # sleep(1000)
        # Servo.otoc(-45)
        # sleep(2000)
        # Servo.otoc(-90)
        # sleep(1000)
        # CPU.tick()
        # robot.tick()

        # if period.isTime():
        #     data = SensorReader.getSensors()
        #     print('SSS', data[SensorReader.LTL] + data[SensorReader.LTM] + data[SensorReader.LTR],
        #           data[SensorReader.OL] + data[SensorReader.OR])

    #
    #     robot.tick()
    #     stateMain.tick()
    #     if period.isTime():
    #         print(ul.getDistance())
    #         # print(robot.encoder().wheel().getDistance())

    # state = StateMain(robot)
    # state.tick()
    # state.tick()

    # sleep(1000)
    # robot.go(120, 0)
    # sleep(1000)
    # robot.go(0, 1350)
    # sleep(1000)
    # robot.go(0, -1350)
    # sleep(1000)
    # robot.go(0, 0)
    # sleep(1000)
    # robot.inicializuj()
    #
    # dopredna = 0.1
    # uhlovaRad = 0.5
    # perioda_regulace = 100
    # cas_minule = ticks_ms()
    #
    # robot.jed(dopredna, 0)

    # sleep(1)
    # data = senzory.precti_senzory()
    #
    # # jak casto vycitat hodnoty??
    # # cara_width = 0.018 # sirka cary 18 milimetru
    # # uhlovaRad 0.5 je 28,647889 stupnu → 28° … za 1 sec se bude otacet robot
    # # 0.058 m jsou senzory od stredu robota
    # # obvod (o=2πr) → 2*0.058*3.1415 = 0.3644 m ← obcod po kterém se pohybují senzory
    # # 0.3644 m .... 360°
    # # šířka čáry je 0.018 m → (0.018*360)/0.3644 → 17.78°
    # # ╰→ tzn. čára zabírá 17.78°.
    # # Musím tedy alespoň 2x do sekunty vyčítat hodnotum protože úhlová rychlost (jak rychle zatočí) je 0.5 rad → ±28°
    #
    # if ticks_diff(ticks_ms(), cas_minule) > perioda_regulace:
    #
    #     doprednaTmp = dopredna
    #     uhlovaTmp = 0
    #
    #     if data[Konstanty.LV_S_CARY]:
    #         uhlovaTmp = uhlovaRad
    #     elif data[Konstanty.PR_S_CARY]:
    #         uhlovaTmp = uhlovaRad * -1
    #     elif (data[Konstanty.LV_S_CARY] + data[Konstanty.PR_S_CARY] + data[Konstanty.PROS_S_CARY]) == 0:
    #         doprednaTmp = 0
    #         uhlovaTmp = 0
    #     robot.jed(doprednaTmp, uhlovaTmp)
    #     print("S", int(data[Konstanty.LV_S_CARY]), int(data[Konstanty.PROS_S_CARY]), int(data[Konstanty.PR_S_CARY]),
    #           " ", doprednaTmp, ",", uhlovaTmp)
    #
    # robot.aktualizuj_se()
    # sleep(5)
    # robot.go(0, 0)
    # robot.jed(0, 0)

    robot.move().goV(0)
