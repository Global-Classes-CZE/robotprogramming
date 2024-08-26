from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu

def jed(dopredna_rychlost, rotace):
    # TODO
    d = 0  # tuto hodnotu si musite zmerit na robotovi, zadejte to v m
    v_l = 0  # TODO vypocitejte dle prednasky 6
    v_r = 0  # TODO vypocitejte dle prednasky 6

    # !!!! POZOR !!!!
    # nez zadate v_l a v_r motorum, ujistete se,
    # ze hodnota je mezi 0-255

     # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r

if __name__ == "__main__":

    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul

