from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu

# !!!! POZOR !!!!
# nez zadate v_l a v_r motorum, ujistete se,
# ze hodnota je mezi 0-255
def getV(n):
    return max(min(255, int(abs(n))), 0)

def jed(dopredna_rychlost, rotace):
    # TODO
    d = 7.5 / 100
    v_l = dopredna_rychlost - d*rotace
    v_r = dopredna_rychlost + d*rotace

    # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r
    if v_r == 0:
        i2c.write(0x70, b"\x03" + bytes([0]))
        i2c.write(0x70, b"\x02" + bytes([0]))
    elif v_r >= 0:
        i2c.write(0x70, b"\x03" + bytes([getV(v_r)]))
    else:
        i2c.write(0x70, b"\x02" + bytes([getV(v_r)]))

    if v_l == 0:
        i2c.write(0x70, b"\x05" + bytes([0]))
        i2c.write(0x70, b"\x04" + bytes([0]))
    elif v_l > 0:
        i2c.write(0x70, b"\x05" + bytes([getV(v_l)]))
    else:
        i2c.write(0x70, b"\x04" + bytes([getV(v_l)]))

if __name__ == "__main__":

    i2c.init(freq=100000)

    # probud cip motoru
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")

    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    jed(135, 0)
    sleep(1000)
    # pak zastavil na 1s
    jed(0, 0)
    sleep(1000)
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    jed(0, 1350)
    sleep(1000)
    # a pak zastavil a kod se vypnul
    jed(0, 0)

