"""
Soubor: motor.py

Autor: Alexandr Ulybin

Popis:
Nepovinný domácí úkol Lekce 5 z live codingu, zadání vytvoření konceptu objektu motoru a jeho řízení pomocí implementace I2C sběrnice
"""
from microbit import i2c
from microbit import sleep


class Motor:
    def __init__(self, key: str, position: str):
        self.key = key
        self.position = position
        self.last_command: bytes = bytes([0])

    def __str__(self):
        return "Motor(key={}, position={}, last_command={})".format(self.key, self.position, self.last_command)


class MotorController:
    def __init__(self, i2c_bus, i2c_address: bytes = 0x70, frequency: int = 400000):
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.motors = {}

        self.i2c_bus.init(freq=frequency)

        self.i2c_bus.write(self.i2c_address, bytes([0x00, 0x01]))
        self.i2c_bus.write(self.i2c_address, bytes([0xE8, 0xAA]))

    def add(self, motor: Motor):
        self.motors[motor.key] = motor

    def forwards(self, key: str, speed: int = 100):
        motor = self.motors[key]

        if motor.position == "left":
            motor.last_command = bytes([0x05])
            self.i2c_bus.write(self.i2c_address, motor.last_command + bytes([speed]))
        if motor.position == "right":
            motor.last_command = bytes([0x03])
            self.i2c_bus.write(self.i2c_address, motor.last_command + bytes([speed]))

    def backwards(self, key: str, speed: int = 100):
        motor = self.motors[key]

        if motor.position == "left":
            motor.last_command = bytes([0x04])
            self.i2c_bus.write(self.i2c_address, motor.last_command + bytes([speed]))
        if motor.position == "right":
            motor.last_command = bytes([0x02])
            self.i2c_bus.write(self.i2c_address, motor.last_command + bytes([speed]))

    def stop(self, key: str):
        motor = self.motors[key]
        self.i2c_bus.write(self.i2c_address, motor.last_command + bytes([0]))


cowley = MotorController(i2c)

cowley.add(Motor(key="Bodie", position="left"))
cowley.add(Motor(key="Doyle", position="right"))

for m in cowley.motors.values():
    print(m)

cowley.forwards("Bodie")
cowley.forwards("Doyle")

sleep(5000)

cowley.stop("Bodie")
cowley.stop("Doyle")
