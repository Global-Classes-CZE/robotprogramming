from microbit import i2c
from microbit import sleep

i2c.init(freq=100000)

#probud cip motoru
i2c.write(0x70, b"\x00\x01")
i2c.write(0x70, b"\xE8\xAA")

#0x02, 0x03
#0-255
sleep(100)
i2c.write(0x70, b"\x05" + bytes([135]))
sleep(2000)
i2c.write(0x70, b"\x02" + bytes([0]))
i2c.write(0x70, b"\x03" + bytes([0]))
i2c.write(0x70, b"\x04" + bytes([0]))
i2c.write(0x70, b"\x05" + bytes([0]))
