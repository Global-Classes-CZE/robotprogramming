"""
Soubor: gostopgo.py

Autor: Alexandr Ulybin

Popis:
Domácí úkol Lekce 5, zadání č.2 pokročilý
"""
from microbit import i2c
from microbit import sleep


def jed(motor: str, smer: str, rychlost: int):
    if motor == "pravy":
        if smer == "dopredu":
            i2c.write(0x70, bytes([0x05]) + bytes([rychlost]))
        if smer == "dozadu":
            i2c.write(0x70, bytes([0x02]) + bytes([rychlost]))
    if motor == "levy":
        if smer == "dopredu":
            i2c.write(0x70, bytes([0x03]) + bytes([rychlost]))
        if smer == "dozadu":
            i2c.write(0x70, bytes([0x04]) + bytes([rychlost]))


if __name__ == "__main__":
    i2c.init(400000)

    i2c.write(0x70, bytes([0x00, 0x01]))
    i2c.write(0x70, bytes([0xE8, 0xAA]))

    jed(motor="pravy", smer="dopredu", rychlost=100)
    jed(motor="levy", smer="dopredu", rychlost=100)

    sleep(1000)

    jed(motor="pravy", smer="dopredu", rychlost=0)
    jed(motor="levy", smer="dopredu", rychlost=0)

    jed(motor="pravy", smer="dozadu", rychlost=100)
    jed(motor="levy", smer="dozadu", rychlost=100)

    sleep(1000)

    jed(motor="pravy", smer="dozadu", rychlost=0)
    jed(motor="levy", smer="dozadu", rychlost=0)
