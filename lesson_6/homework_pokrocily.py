# Write your code here :-)
from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu

def jed(dopredna_rychlost, rotace):
                                                # TODO
    d = 0.075                                   # tuto hodnotu si musite zmerit na robotovi, zadejte to v m - 7,5 cm = 0,075 m
    v_l = abs(int(dopredna_rychlost-d*rotace))  # TODO vypocitejte dle prednasky 6
    v_r = abs(int(dopredna_rychlost+d*rotace))  # TODO vypocitejte dle prednasky 6
    
    # !!!! POZOR !!!!
    # nez zadate v_l a v_r motorum, ujistete se,
    # ze hodnota je mezi 0-255

    if (0 <= abs(v_l) <= 255) and (0 <= abs(v_r) <= 255):
        if dopredna_rychlost > 0:
            i2c.write(0x70, b"\x03" + bytes([v_r]))
            i2c.write(0x70, b"\x05" + bytes([v_l]))
        elif dopredna_rychlost < 0:
            i2c.write(0x70, b"\x02" + bytes([v_r]))
            i2c.write(0x70, b"\x04" + bytes([v_l]))
        elif dopredna_rychlost == 0 and rotace >= 0:
            i2c.write(0x70, b"\x03" + bytes([rotace]))
            i2c.write(0x70, b"\x04" + bytes([rotace]))
        elif dopredna_rychlost == 0 and rotace < 0:
            i2c.write(0x70, b"\x02" + bytes([abs(rotace)]))
            i2c.write(0x70, b"\x05" + bytes([abs(rotace)]))
            
    else:
        print("hodnoty mimo rozsah")
        
    print()

    # 02 - pravý vzad
    # 03 - pravý vpřed
    # 04 - levý vzad
    # 05 - levý vpřed

     # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r

def zastav():
    i2c.write(0x70, b"\x02" + bytes([0]))
    i2c.write(0x70, b"\x03" + bytes([0]))
    i2c.write(0x70, b"\x04" + bytes([0]))
    i2c.write(0x70, b"\x05" + bytes([0]))

if __name__ == "__main__":

    # TODO napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul

    #zapni komunikaci
    i2c.init(freq=100000)

    # probuď motory
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")
    
    
    #jedeme

    jed(135, 0)    
    sleep(1000)
    
    zastav()
    sleep(1000)

    jed(0,135)
    sleep(1000)

    zastav()

