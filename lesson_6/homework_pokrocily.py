from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu

def jed(dopredna_rychlost, rotace):
    # TODO
    d = 0.075  # tuto hodnotu si musite zmerit na robotovi, zadejte to v m
    v_l = dopredna_rychlost - d*rotace
    v_r = dopredna_rychlost + d*rotace
    #print(v_l, v_r)

    # !!!! POZOR !!!!
    # nez zadate v_l a v_r motorum, ujistete se,
    # ze hodnota je mezi 0-255

     # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r
    if 0 <= v_l <= 255:
        i2c.write(0x70, b"\x05" + bytes([int(v_l)]))
    elif -255 <= v_l < 0:
        v_l = v_l*-1
        i2c.write(0x70, b"\x04" + bytes([int(v_l)]))
    if 0 <= v_r <= 255:
        i2c.write(0x70, b"\x03" + bytes([int(v_r)]))
    elif -255 <= v_r < 0:
        v_r = v_r*-1
        i2c.write(0x70, b"\x02" + bytes([int(v_r)]))
    else:
        raise ValueError("PWM mimo rozsah - v_l=",v_l,", v_r=",v_r)

# musel jsem udelat tuto funkci pro zastaveni, protoze na konci programu mi jed(0,0) nevypinalo leve kolo
def zastav():
    i2c.write(0x70, b"\x05\x00")
    i2c.write(0x70, b"\x04\x00")
    i2c.write(0x70, b"\x03\x00")
    i2c.write(0x70, b"\x02\x00")

if __name__ == "__main__":

    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul
    i2c.init(freq=100000)
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")
    sleep(100)
    i2c.write(0x70, b"\x05\x00")
    i2c.write(0x70, b"\x04\x00")
    i2c.write(0x70, b"\x03\x00")
    i2c.write(0x70, b"\x02\x00")

    jed(135, 0)
    sleep(1000)
    zastav()
    sleep(1000)
    jed(0, 1350)
    sleep(1000)
    zastav()

