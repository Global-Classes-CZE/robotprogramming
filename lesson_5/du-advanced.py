from microbit import i2c
from microbit import sleep

def init():
    #inicializace i2c
    i2c.init(freq=400000)
    #probud cip motoru
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')

def jed(motor, smer, rychlost):
    pwm_no=0
    if motor == "pravy":
        if smer == "dozadu":
            pwm_no=2
        if smer == "dopredu":
            pwm_no=3
    if motor == "levy":
        if smer == "dozadu":
            pwm_no=4
        if smer == "dopredu":
            pwm_no=5

    if pwm_no>0:
        i2c.write(0x70, bytes([pwm_no, rychlost]))


if __name__ == "__main__":
    init()
    rychlost = 135

    # oba dopredu
    jed("pravy","dopredu",rychlost)
    jed("levy", "dopredu",rychlost)
    sleep(1000)
    # zastavit
    jed("pravy","dopredu",0)
    jed("levy", "dopredu",0)
    sleep(200)

    # oba dozadu
    jed("pravy","dozadu",rychlost)
    jed("levy", "dozadu",rychlost)
    sleep(1000)
    # zastavit
    jed("pravy","dozadu" ,0)
    jed("levy", "dozadu" ,0)
