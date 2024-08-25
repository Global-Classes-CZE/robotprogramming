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
    v_l = int(dopredna_rychlost - d * rotace)  # TODO vypocitejte dle prednasky 6
    v_r = int(dopredna_rychlost + d * rotace)  # TODO vypocitejte dle prednasky 6

    # !!!! POZOR !!!!
    # nez zadate v_l a v_r motorum, ujistete se,
    # ze hodnota je mezi 0-255
    if not (-255 <= v_l <= 255) or not (-255 <= v_r <= 255):
        raise ValueError("Rychlost musí být v rozmezí -255/255")
     # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r
    if v_l >= 0:
        i2c.write(0x70, b"\x05" + bytes([v_l])) # Levý dopředu
    if v_l <= 0:
        i2c.write(0x70, b"\x04" + bytes([abs(v_l)])) # Levý dozadu
    if v_r >= 0:
        i2c.write(0x70, b"\x03" + bytes([v_r])) # Pravý dopředu
    if v_r <= 0:
        i2c.write(0x70, b"\x02" + bytes([abs(v_r)])) # Pravý dozadu
if __name__ == "__main__":

    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul

    jed(135, 0)
    sleep (1000)

    jed(0,0)
    sleep (1000)

    jed(0, 1350)
    sleep (1000)

    jed(0,0)