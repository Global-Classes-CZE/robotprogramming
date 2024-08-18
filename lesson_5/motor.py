from microbit import i2c
from microbit import sleep

i2c.init(freq=400000)

#probud cip motoru
i2c.write(0x70, b"\x00\x01")
i2c.write(0x70, b"\xE8\xAA")

#i2c.write(0x70, b"\x02" + bytes([0]))
#i2c.write(0x70, b"\x03" + bytes([0]))
#i2c.write(0x70, b"\x04" + bytes([0]))
#i2c.write(0x70, b"\x05" + bytes([0]))

levy = "levy"
pravy = "pravy"
dopredu = "dopredu"
dozadu = "dozadu"

def jed(motor, smer, rychlost):

    if not (0 <= rychlost <= 255):
        raise ValueError("Rychlost musí být v rozmezí 0-255")

    if motor == str(pravy) and smer == str(dozadu):
        i2c.write(0x70, b"\x02" + bytes([rychlost]))
    if motor == str(pravy) and smer == str(dopredu):
        i2c.write(0x70, b"\x03" + bytes([rychlost]))
    if motor == str(levy) and smer == str(dozadu):
        i2c.write(0x70, b"\x04" + bytes([rychlost]))
    if motor == str(levy) and smer == str(dopredu):
        i2c.write(0x70, b"\x05" + bytes([rychlost]))

def main():
#vpřed
    jed(pravy, dopredu, 100)
    jed(levy, dopredu, 100)
    sleep(1000)
#zastav
    jed(pravy, dopredu, 0)
    jed(levy, dopredu, 0)
    sleep(1000)
#vzad
    jed(pravy, dozadu, 100)
    jed(levy, dozadu, 100)
    sleep(1000)
#zastav
    jed(pravy, dozadu, 0)
    jed(levy, dozadu, 0)

main()
