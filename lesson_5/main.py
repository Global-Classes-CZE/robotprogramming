"""
Soubor: main.py

Autor: Alexandr Ulybin

Popis:
Domácí úkol Lekce 5, zadání č.3 velmi pokročilý.
Používá se modul light.py a robot.py
"""
from neopixel import NeoPixel
from microbit import pin0
from microbit import sleep

from light import Light
from light import LightController
from robot import Robot

if __name__ == "__main__":
    np = NeoPixel(pin0, 8)

    lightController = LightController(np)

    lightController.add(Light(LightController.FRONT_LEFT_INNER, 0))
    lightController.add(Light(LightController.FRONT_LEFT_OUTER, 1))
    lightController.add(Light(LightController.FRONT_RIGHT_OUTER, 2))
    lightController.add(Light(LightController.FRONT_RIGHT_INNER, 3))
    lightController.add(Light(LightController.REAR_LEFT_OUTER, 4))
    lightController.add(Light(LightController.REAR_LEFT_INNER, 5))
    lightController.add(Light(LightController.REAR_RIGHT_INNER, 6))
    lightController.add(Light(LightController.REAR_RIGHT_OUTER, 7))

    robot = Robot(lightController)

    print(len(robot.light_controller.lights))

    robot.zapni_svetla()
    sleep(2000)
    robot.vypni_svetla()

    sleep(2000)

    robot.indikuj("doprava")
    sleep(2000)
    robot.indikuj("doleva")

    sleep(2000)

    robot.brzdi()
