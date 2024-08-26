from microbit import i2c
from microbit import sleep

# initializace komunikace a cipu motoru
def init():

    i2c.init(freq=100000)
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")


# spusti prislusny motor v urcenem smeru a rychlosti
def jed(motor, smer, rychlost):
    if motor == "pravy":
        if smer == "vpred":
            i2c.write(0x70, b"\x02" + bytes([0]))
            i2c.write(0x70, b"\x03" + bytes([rychlost]))
        elif smer == "vzad":
            i2c.write(0x70, b"\x03" + bytes([0]))
            i2c.write(0x70, b"\x02" + bytes([rychlost]))
    if motor == "levy":
        if smer == "vpred":
            i2c.write(0x70, b"\x04" + bytes([0]))
            i2c.write(0x70, b"\x05" + bytes([rychlost]))
        elif smer == "vzad":
            i2c.write(0x70, b"\x05" + bytes([0]))
            i2c.write(0x70, b"\x04" + bytes([rychlost]))


# zastavi motory
def zastav():
    jed("pravy", "vpred", 0)
    jed("levy", "vpred", 0)


if __name__ == "__main__":
    init()

    # skoro plnou parou vpred
    jed("pravy", "vpred", 200)
    jed("levy", "vpred", 200)
    sleep(1000)

    # zastavit a stat na pul sekundy
    zastav()
    sleep(500)

    # skoro plnou parou vzad
    jed("pravy", "vzad", 200)
    jed("levy", "vzad", 200)
    sleep(1000)

    # na konci slusne zastavime
    zastav()
