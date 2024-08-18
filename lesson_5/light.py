"""
Soubor: light.py

Autor: Alexandr Ulybin

Popis:
Domácí úkol Lekce 5, zadání č.3 velmi pokročilý.
Modul je využíván v robot.py.
"""


class Light:
    def __init__(self, key: str, index: int, color: tuple = (0, 0, 0)):
        self.key = key
        self.index = index
        self.color = color
        self.status = LightController.STATUS_OFF


class LightController:
    FRONT_LEFT_INNER = "FLI"
    FRONT_LEFT_OUTER = "FLO"
    FRONT_RIGHT_INNER = "FRI"
    FRONT_RIGHT_OUTER = "FRO"

    REAR_LEFT_INNER = "RLI"
    REAR_LEFT_OUTER = "RLO"
    REAR_RIGHT_INNER = "RRI"
    REAR_RIGHT_OUTER = "RRO"

    STATUS_ON = 1
    STATUS_OFF = 0

    def __init__(self, np):
        self.np = np
        self.lights = {}

    def add(self, light: Light):
        self.lights[light.key] = light

    def on(self, key: str, color: tuple):
        light: Light = self.lights[key]
        light.status = self.STATUS_ON
        light.color = color
        self.np[light.index] = color
        self.np.show()
        print("{} : {}".format(light.key, light.status))

    def off(self, key: str):
        light: Light = self.lights[key]
        light.status = self.STATUS_OFF
        light.color = (0, 0, 0)
        self.np[light.index] = light.color
        self.np.show()
        print("{} : {}".format(light.key, light.status))

    def offAll(self):
        for light in self.lights.values():
            self.off(light.key)
        self.np.show()
