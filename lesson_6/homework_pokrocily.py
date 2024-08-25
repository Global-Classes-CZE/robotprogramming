from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu


def jed(dopredna_rychlost, rotace):
    # TODO
    d = 0.15  # tuto hodnotu si musite zmerit na robotovi, zadejte to v m
    v_l = dopredna_rychlost - (rotace * d / 2)  # TODO vypocitejte dle prednasky 6
    v_r = dopredna_rychlost + (rotace * d / 2)  # TODO vypocitejte dle prednasky 6

    # !!!! POZOR !!!!
    # nez zadate v_l a v_r motorum, ujistete se,
    # ze hodnota je mezi 0-255
    v_l = max(min(int(v_l), 255), 0)
    v_r = max(min(int(v_r), 255), 0)

    if v_l >= 0:
        i2c.write(0x70, b"\x05" + bytes([v_l]))
    else:
        i2c.write(0x70, b"\x04" + bytes([abs(v_l)]))

    if v_r >= 0:
        i2c.write(0x70, b"\x03" + bytes([v_r]))
    else:
        i2c.write(0x70, b"\x02" + bytes([abs(v_r)]))

    # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r


if __name__ == "__main__":

    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul

    i2c.init(100000)
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")

    jed(135, 0)
    sleep(1000)

    jed(0, 0)
    sleep(1000)

    jed(0, 1350)
    sleep(1000)

    jed(0, 0)
    sleep(1000)
