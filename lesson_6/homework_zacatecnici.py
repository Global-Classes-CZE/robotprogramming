from microbit import i2c, sleep

def jed(motor, smer, rychlost):
    if motor == "pravy":
        if smer == "dopredu":
            i2c.write(0x70, b"\x03" + bytes([rychlost]))
        elif smer == "dozadu":
            i2c.write(0x70, b"\x02" + bytes([rychlost]))
        else:
            raise ValueError("Neplatny vstup")
    elif motor == "levy":
        if smer == "dopredu":
            i2c.write(0x70, b"\x05" + bytes([rychlost]))
        elif smer == "dozadu":
            i2c.write(0x70, b"\x04" + bytes([rychlost]))
        else:
            raise ValueError("Neplatny vstup")
    else:
        raise ValueError("Neplatny vstup")

def zastav(motor):
    if motor == "pravy":
        jed("pravy", "dopredu", 0)
        jed("pravy", "dozadu", 0)
    elif motor == "levy":
        jed("levy", "dopredu", 0)
        jed("levy", "dozadu", 0)
    else:
        raise ValueError("Neplatny vstup")

if __name__ == "__main__":
    i2c.init(100000)
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")

    jed("pravy", "dopredu", 135)
    jed("levy", "dopredu", 135)
    sleep(1000)

    zastav("pravy")
    zastav("levy")
    sleep(1000)

    jed("pravy", "dozadu", 135)
    jed("levy", "dozadu", 135)
    sleep(1000)

    zastav("pravy")
    zastav("levy")
    sleep(1000)
