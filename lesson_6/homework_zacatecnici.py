# Homework no.7

from microbit import i2c
from microbit import sleep

motorLavy = "lavy"
motorPravy = "pravy"
smerDopredu = "dopredu"
smerDozadu = "dozadu"
minRychlost = 0
maxRychlost = 130
zelanaRychlost = 100
i2cControllerAddress = 0x70
pravyMotorDopredu = 0x03
pravyMotorDozadu = 0x02
lavyMotorDopredu = 0x05
lavyMotorDozadu = 0x04

class Motor:
    # ctor
    def __init__(self, jmeno):
        self.motor = jmeno
        if self.motor != motorLavy and self.motor != motorPravy:
            print("Zla hodnota pre motor '" + self.motor + ". Povolene hodnoty su '" + motorLavy + "', '" + motorPravy + "'")
            return
    
    def jed(self, smer : str, rychlost : int):
        if rychlost < minRychlost or rychlost > maxRychlost :
            print("Zla hodnota pre rychlost '" + str(rychlost) + "' musi byt v intervale <" + str(minRychlost) + ", " + str(maxRychlost) + ">")
            return

        if self.motor == motorLavy:
            if smer == smerDopredu:
                i2c.write(i2cControllerAddress, bytes([lavyMotorDozadu]) + bytes([0]))
                i2c.write(i2cControllerAddress, bytes([lavyMotorDopredu]) + bytes([rychlost]))
            if smer == smerDozadu:
                i2c.write(i2cControllerAddress, bytes([lavyMotorDopredu]) + bytes([0]))
                i2c.write(i2cControllerAddress, bytes([lavyMotorDozadu]) + bytes([rychlost]))

        if self.motor == motorPravy:
            if smer == smerDopredu:
                i2c.write(i2cControllerAddress, bytes([pravyMotorDozadu]) + bytes([0]))
                i2c.write(i2cControllerAddress, bytes([pravyMotorDopredu]) + bytes([rychlost]))
            if smer == smerDozadu:
                i2c.write(i2cControllerAddress, bytes([pravyMotorDopredu]) + bytes([0]))
                i2c.write(i2cControllerAddress, bytes([pravyMotorDozadu]) + bytes([rychlost]))

        return "Running Motor='" + self.motor + "', Smer='" + smer + "', Rychlost='" + str(rychlost) + "'"

    def zastav(self):
        if self.motor == motorLavy:
            i2c.write(i2cControllerAddress, bytes([lavyMotorDopredu]) + bytes([0]))
            i2c.write(i2cControllerAddress, bytes([lavyMotorDozadu]) + bytes([0]))
        
        if self.motor == motorPravy:
            i2c.write(i2cControllerAddress, bytes([pravyMotorDopredu]) + bytes([0]))
            i2c.write(i2cControllerAddress, bytes([pravyMotorDozadu]) + bytes([0]))

if __name__ == "__main__":
    i2c.init(freq=100000)

    # probud cip motoru
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")

    # Inicializuj premenne typu Motor
    levy_motor = Motor(motorLavy)
    pravy_motor = Motor(motorPravy)
    
    # Move forward
    levy_motor.jed(smerDopredu, 130)
    pravy_motor.jed(smerDopredu, 130)
    
    sleep(1000)
    
    levy_motor.jed(smerDozadu, 130)
    pravy_motor.jed(smerDozadu, 130)

    sleep(1000)

    levy_motor.zastav()
    pravy_motor.zastav()
