from microbit import i2c
from microbit import sleep

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu

#funkce pro limit nastaveni rychlosti 0-255
def clamp(n):
    return max(min(255, n), 0)

def jed(dopredna_rychlost:float, rotace:float):
    param_motor_prava_dozadu = b'\x02'
    param_motor_prava_dopredu = b'\x03'
    param_motor_leva_dozadu = b'\x04'
    param_motor_leva_dopredu = b'\x05'
    
    d = 0.15 
    v_l = int(dopredna_rychlost - d * rotace)
    v_r = int(dopredna_rychlost + d * rotace)
    print(v_l, " ", v_r)

     # TODO nastavte rychlost a smer motoru podle hodnot v_l a v_r
    i2c.init(freq=400000)
    #kontrola rychlosti a smeru praveho kola
    if v_r > 0:
        i2c.write(0x70, param_motor_prava_dopredu + bytes([clamp(v_r)]))
    elif v_r < 0:
        i2c.write(0x70, param_motor_prava_dozadu + bytes([clamp(abs(v_r))]))
    elif v_r == 0:
        i2c.write(0x70, param_motor_prava_dozadu + bytes([0]))
        i2c.write(0x70, param_motor_prava_dopredu + bytes([0]))
  
    #kontrola rychlosti a smeru leveho kola      
    if v_l > 0:
        i2c.write(0x70, param_motor_leva_dopredu + bytes([clamp(v_l)]))
    elif v_l < 0:
        i2c.write(0x70, param_motor_leva_dozadu + bytes([clamp(abs(v_l))]))
    elif v_l == 0:
        i2c.write(0x70, param_motor_leva_dozadu + bytes([0]))
        i2c.write(0x70, param_motor_leva_dopredu + bytes([0])) 
        
#hlavni fce
def main():
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")
    jed(135, 0)
    sleep(1000) 
    jed(0, 0)
    sleep(1000) 
    jed(0, 1350)
    sleep(1000) 
    jed(0, 0)
    
#main
if __name__ == "__main__":
    main()
