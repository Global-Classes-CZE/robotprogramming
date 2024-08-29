from microbit import i2c
from microbit import sleep
from microbit import pin19
from microbit import pin20

i2c.init(freq=400000, sda=pin20, scl=pin19)
i2c.write(0x70, b'\x00\x01')
i2c.write(0x70, b'\xE8\xAA')

def jed(dopredna_rychlost, rotace):
    d = 0.074  # tuto hodnotu si musite zmerit na robotovi, zadejte to v m
    v_l = dopredna_rychlost - d * rotace   # TODO vypocitejte dle prednasky 6
    v_r = dopredna_rychlost + d * rotace  # TODO vypocitejte dle prednasky 6

    zastav()

    if v_l < -255 or v_l > 255:
        return -1

    if v_r < -255 or v_r > 255:
        return -1

    if(v_l <= 0):
        i2c.write(0x70, b'\x02' + bytes([abs(int(v_l))]))
    else:
        i2c.write(0x70, b'\x03' + bytes([abs(int(v_l))]))

    if(v_r <= 0):
        i2c.write(0x70, b'\x04' + bytes([abs(int(v_r))]))
    else:
        i2c.write(0x70, b'\x05' + bytes([abs(int(v_r))]))

def zastav():
    i2c.write(0x70, b'\x02' + bytes([0]))
    i2c.write(0x70, b'\x03' + bytes([0]))
    i2c.write(0x70, b'\x04' + bytes([0]))
    i2c.write(0x70, b'\x05' + bytes([0]))

if __name__ == "__main__":
    zastav()
    jed(135, 0)
    sleep(1000)
    zastav()
    sleep(1000)
    jed(0, 1350)
    sleep(1000)
    zastav()

