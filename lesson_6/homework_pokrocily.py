from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu


def jed(dopredna_rychlost, rotace):
    # TODO
    d = 0.0875  # tuto hodnotu si musite zmerit na robotovi, zadejte to v m
    v_l = int(dopredna_rychlost - d * rotace)  # TODO vypocitejte dle prednasky 6
    v_r = int(dopredna_rychlost + d * rotace)  # TODO vypocitejte dle prednasky 6
    command_l: bytes = bytes([0])
    command_r: bytes = bytes([0])
    # !!!! POZOR !!!!
    # nez zadate v_l a v_r motorum, ujistete se,
    # ze hodnota je mezi 0-255

    # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r

    v_l_abs = abs(v_l)
    v_r_abs = abs(v_r)
    print(v_l)
    print(v_r)

    if (0 < v_l_abs <= 255) and (0 < v_r_abs <= 255):
        if v_l >= 0:
            command_l = bytes([0x05]) + bytes([v_l_abs])
        else:
            command_l = bytes([0x04]) + bytes([v_l_abs])
        if v_r >= 0:
            command_r = bytes([0x03]) + bytes([v_r_abs])
        else:
            command_r = bytes([0x02]) + bytes([v_r_abs])
        i2c.write(0x70, command_l)
        i2c.write(0x70, command_r)
    else:
        i2c.write(0x70, bytes([0x05]) + bytes([0]))
        i2c.write(0x70, bytes([0x04]) + bytes([0]))
        i2c.write(0x70, bytes([0x03]) + bytes([0]))
        i2c.write(0x70, bytes([0x02]) + bytes([0]))


if __name__ == "__main__":
    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul

    i2c.init(400000)

    i2c.write(0x70, bytes([0x00, 0x01]))
    i2c.write(0x70, bytes([0xE8, 0xAA]))

    sleep(1000)

    jed(135, 0)
    sleep(1000)
    jed(0, 0)
    sleep(1000)
    jed(0, 1350)
    sleep(1000)
    jed(0, 0)
