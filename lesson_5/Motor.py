from microbit import i2c
from microbit import sleep

class Motor:

    def __init__(self):
        #inicializace i2c
        i2c.init(freq=400000)
        #probud cip motoru
        i2c.write(112, bytes([0x00,0x01]))
        i2c.write(112, bytes([0xE8,0xAA]))

    def jed(self, motor, smer, rychlost):
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
#        print([pwm_no,rychlost, motor,smer])

        if pwm_no>0:
            i2c.write(0x70, bytes([pwm_no, rychlost]))

def main():
    motor = Motor()
    rychlost = 135

    # oba dopredu
    motor.jed("pravy", "dopredu", rychlost)
    motor.jed("levy", "dopredu", rychlost)
    sleep(1000)
    # zastavit
    motor.jed("pravy", "dopredu", 0)
    motor.jed("levy", "dopredu", 0)
    sleep(200)

    # oba dozadu
    for rychlost in range(255):
        motor.jed("pravy", "dozadu", rychlost)
        motor.jed("levy", "dozadu", rychlost)
        sleep(100)
    # zastavit
    motor.jed("pravy", "dozadu", 0)
    motor.jed("levy", "dozadu", 0)

if __name__ == "__main__":
    main()

