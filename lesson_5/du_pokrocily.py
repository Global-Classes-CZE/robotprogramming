from microbit import i2c

def nastav_PWM_kanaly(kanal_on, kanal_off, rychlost):
    i2c.write(0x70, kanal_off + bytes([0]))
    i2c.write(0x70, kanal_on + bytes([rychlost]))
    return 0

def jed(motor, smer, rychlost):
    je_vse_ok = -2

    rychlost = int(rychlost)
    if rychlost < 0 or rychlost > 255:
        je_vse_ok = -1
        return

    if motor == "levy":
        if smer == "dopredu":
            je_vse_ok = nastav_PWM_kanaly(b"\x05", b"\x04", rychlost)
        elif smer == "dozadu":
            je_vse_ok = nastav_PWM_kanaly(b"\x04", b"\x05", rychlost)
        else:
            je_vse_ok = -1
    elif motor == "pravy":
        if smer == "dopredu":
            je_vse_ok = nastav_PWM_kanaly(b"\x03", b"\x02", rychlost)
        elif smer == "dozadu":
            je_vse_ok = nastav_PWM_kanaly(b"\x02", b"\x03", rychlost)
        else:
            je_vse_ok = -1
    else:
        je_vse_ok = -1

    return je_vse_ok

if __name__ == "__main__":

    i2c.init(freq=400000)
    # probud cip motoru
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")
    sleep(100)

    # dopredu
    jed("levy", "dopredu", 135)
    jed("pravy", "dopredu", 135)
    sleep(1000)
    # zastav
    jed("levy", "dopredu", 0)
    jed("pravy", "dozadu", 0)
    sleep(1000)
    # dozadu
    jed("levy", "dozadu", 135)
    jed("pravy", "dozadu", 135)
    sleep(1000)
    # zastav
    jed("levy", "dopredu", 0)
    jed("pravy", "dozadu", 0)
