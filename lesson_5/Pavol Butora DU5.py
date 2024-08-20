# Zacatecnici ukol
maxIndex = 6
asterixChar = '*'

for i in range(1, maxIndex):
  print(asterixChar)

print()

maxAsterixCounts = 6
for asterixCount in range(1, maxAsterixCounts):
  print(asterixChar * asterixCount)



# Pokrocili ukol
from microbit import sleep
from microbit import i2c
from microbit import Image
from microbit import display

i2cControllerAddress = 0x70
i2cControllerFrequency = 100000
motorLavy = "lavy"
motorPravy = "pravy"
smerDopredu = "dopredu"
smerDozadu = "dozadu"
minRychlost = 0
maxRychlost = 255
zelanaRychlost = 100
charF = Image("99900:90000:99000:90000:90000")
charR = Image("99900:90900:99900:99000:90900")
charS = Image("99900:90000:99900:00900:99900")
charE = Image("99900:90000:99900:90000:99900")

def jed(motor : str, smer : str, rychlost : int):
    isError = False
    
    if motor != motorLavy and motor != motorPravy:
        print("Zla hodnota pre motor '" + motor + "'. Povolene hodnoty su '" + motorLavy + "', '" + motorPravy + "'")
        isError = True
    
    if smer != smerDopredu and smer != smerDozadu:
        print("Zla hodnota pre smer '" + smer + "'. Povolene hodnoty su '" + smerDopredu + "', '" + smerDozadu + "'")
        isError = True
    
    if rychlost < minRychlost or rychlost > maxRychlost :
        print("Zla hodnota pre rychlost '" + str(rychlost) + "' musi byt v intervale <" + str(minRychlost) + ", " + str(maxRychlost) + ">")
        isError = True
    
    if isError:
        return "Nastala chyba"
    
    if motor == motorLavy:
        if smer == smerDopredu:
            i2c.write(i2cControllerAddress, bytes([0x03]) + bytes([rychlost]))
        if smer == smerDozadu: 
            i2c.write(i2cControllerAddress, bytes([0x04]) + bytes([rychlost]))
    
    if motor == motorPravy:
        if smer == smerDopredu:
            i2c.write(i2cControllerAddress, bytes([0x05]) + bytes([rychlost]))
        if smer == smerDozadu:
            i2c.write(i2cControllerAddress, bytes([0x02]) + bytes([rychlost]))
    
    return "Running Motor='" + motor + "', Smer='" + smer + "', Rychlost='" + str(rychlost) + "'"

# stop all motors
def stop():
    i2c.write(i2cControllerAddress, bytes([0x03]) + bytes([0]))
    i2c.write(i2cControllerAddress, bytes([0x04]) + bytes([0]))
    i2c.write(i2cControllerAddress, bytes([0x05]) + bytes([0]))
    i2c.write(i2cControllerAddress, bytes([0x02]) + bytes([0]))
    ShowImageOnDisplay(charS)

def JedDopredu(rychlost : int):
    print(jed(motorLavy, smerDopredu, rychlost))
    print(jed(motorPravy, smerDopredu, rychlost))
    ShowImageOnDisplay(charF)

def JedDozadu(rychlost : int):
    print(jed(motorLavy, smerDozadu, rychlost))
    print(jed(motorPravy, smerDozadu, rychlost))
    ShowImageOnDisplay(charR)

def ShowImageOnDisplay(image : Image):
    display.show(image)
 
if __name__ == "__main__":
    # Initialization of the I2C interface
    i2c.init(i2cControllerFrequency)

    # Print addresses
    adresy = i2c.scan()
    print(adresy)

    # Initialization of the PWM controller
    i2c.write(i2cControllerAddress, b"\x00\x01")
    i2c.write(i2cControllerAddress, b"\xE8\xAA")

    # Move forward
    JedDopredu(zelanaRychlost)
    sleep(1000)
    stop()

    # Move backward
    JedDozadu(zelanaRychlost)
    sleep(1000)
    stop()

    ShowImageOnDisplay(charE)
    print("Application exit")
    print()
