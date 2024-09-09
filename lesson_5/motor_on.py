# Import of the micro:bit module
from microbit import i2c
from microbit import sleep

if __name__ == "__main__":
    # Initialization of the I2C interface
    i2c.init(freq=400000)

    adresy = i2c.scan()

    for adresa in adresy:
        print(hex(adresa))

    # Initialization of the PWM controller
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')

    i2c.write(0x70, b'\x03' + bytes([135]))
    sleep(1000)
    i2c.write(0x70, b'\x03' + bytes([0]))

