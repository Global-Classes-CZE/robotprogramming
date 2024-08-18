"""
Soubor: robot.py

Autor: Alexandr Ulybin

Popis:
Domácí úkol Lekce 5, zadání č.3 velmi pokročilý.
"""


from microbit import sleep


class Robot:
    def __init__(self, lc):
        self.light_controller = lc
        self.light_controller.offAll()

    def indikuj(self, smer_zataceni: str):

        if smer_zataceni == "doprava":
            for i in range(3):
                self.light_controller.on(
                    self.light_controller.FRONT_RIGHT_OUTER, (255, 165, 0)
                )
                self.light_controller.on(
                    self.light_controller.REAR_RIGHT_OUTER, (255, 165, 0)
                )
                sleep(500)
                self.light_controller.off(self.light_controller.FRONT_RIGHT_OUTER)
                self.light_controller.off(self.light_controller.REAR_RIGHT_OUTER)
                sleep(500)
        if smer_zataceni == "doleva":
            for i in range(3):
                self.light_controller.on(
                    self.light_controller.FRONT_LEFT_OUTER, (255, 165, 0)
                )
                self.light_controller.on(
                    self.light_controller.REAR_LEFT_OUTER, (255, 165, 0)
                )
                sleep(500)
                self.light_controller.off(self.light_controller.FRONT_LEFT_OUTER)
                self.light_controller.off(self.light_controller.REAR_LEFT_OUTER)
                sleep(500)

    def zapni_svetla(self):
        self.light_controller.on(
            self.light_controller.FRONT_LEFT_INNER, (255, 255, 255)
        )
        self.light_controller.on(
            self.light_controller.FRONT_RIGHT_INNER, (255, 255, 255)
        )

        self.light_controller.on(self.light_controller.REAR_LEFT_OUTER, (60, 0, 0))
        self.light_controller.on(self.light_controller.REAR_RIGHT_OUTER, (60, 0, 0))

    def brzdi(self):
        self.zapni_brzdova_svetla()
        sleep(1000)
        self.vypni_brzdova_svetla()

    def zapni_brzdova_svetla(self):
        self.light_controller.on(self.light_controller.REAR_LEFT_OUTER, (255, 0, 0))
        self.light_controller.on(self.light_controller.REAR_RIGHT_OUTER, (255, 0, 0))
        self.light_controller.on(self.light_controller.REAR_LEFT_INNER, (255, 0, 0))
        self.light_controller.on(self.light_controller.REAR_RIGHT_INNER, (255, 0, 0))

    def vypni_brzdova_svetla(self):
        self.light_controller.off(self.light_controller.REAR_LEFT_OUTER)
        self.light_controller.off(self.light_controller.REAR_RIGHT_OUTER)
        self.light_controller.off(self.light_controller.REAR_LEFT_INNER)
        self.light_controller.off(self.light_controller.REAR_RIGHT_INNER)

    def vypni_svetla(self):
        self.light_controller.off(self.light_controller.FRONT_LEFT_INNER)
        self.light_controller.off(self.light_controller.FRONT_RIGHT_INNER)

        self.light_controller.off(self.light_controller.REAR_LEFT_OUTER)
        self.light_controller.off(self.light_controller.REAR_RIGHT_OUTER)
