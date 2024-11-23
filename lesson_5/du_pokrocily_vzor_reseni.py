from microbit import i2c, sleep

def nastav_PWM_kanaly(kanal_on, kanal_off, rychlost):
    # je nesmirne dulezite vzdy mit zapnuty jen jeden kanal,
    # tedy tato funkce zarucuje, ze se druhy kanal vypne
    i2c.write(0x70, kanal_off + bytes([0]))
    i2c.write(0x70, kanal_on + bytes([rychlost]))
    return 0

def jed(motor, smer, rychlost):
    '''
       Tato funkce uvede dany motor do pohybu,
       zadanou rychlosti a v pozadovanem smeru.
       Vraci chybove hodnoty:
        0: vse je v poradku
       -1: program neprobehl spravne
       -2: zadane nepodporovane jmeno motoru
       -3: pozadovana rychlost je mimo mozny rozsah
       -4: zadany nepodporovany smer
    '''
    je_vse_ok = -1

    rychlost = int(rychlost)
    if rychlost < 0 or rychlost > 255:
        je_vse_ok = -3
        return

    if motor == "levy":
        if smer == "dopredu":
            je_vse_ok = nastav_PWM_kanaly(b"\x05", b"\x04", rychlost)
        elif smer == "dozadu":
            je_vse_ok = nastav_PWM_kanaly(b"\x04", b"\x05", rychlost)
        else:
            je_vse_ok = -4
    elif motor == "pravy":
        if smer == "dopredu":
            je_vse_ok = nastav_PWM_kanaly(b"\x03", b"\x02", rychlost)
        elif smer == "dozadu":
            je_vse_ok = nastav_PWM_kanaly(b"\x02", b"\x03", rychlost)
        else:
            je_vse_ok = -4
    else:
        je_vse_ok = -2

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
