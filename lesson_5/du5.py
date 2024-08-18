from microbit import i2c
from microbit import sleep

#zacatecnici
print("prvni cast")
for i in range(1, 6):
    print("*")
print("druha cast")
for i in range(0, 5):
    i+=1
    print(i * "*")
    
#pokrocili
def jed(motor:str, smer:str, rychlost:int):
    motor_values = {"pravy", "levy"}
    smer_values = {"dopredu", "dozadu"}
    rychlost_values = range(256)
    param_motor_prava_dozadu = b'\x02'
    param_motor_prava_dopredu = b'\x03'
    param_motor_leva_dozadu = b'\x04'
    param_motor_leva_dopredu = b'\x05'
    
    if motor not in motor_values:
        raise ValueError("results: motor_values must be 'pravy' or 'levy'")
    elif smer not in smer_values:
        raise ValueError("results: smer_values must be 'dopredu' or 'dozadu'")
    elif rychlost not in rychlost_values:
        raise ValueError("results: rychlost_values must be in range 0 - 255")
    else:
        i2c.init(freq=400000)
        if motor == 'pravy' and smer == 'dopredu':
            param_motor = param_motor_prava_dopredu
        elif motor == 'levy' and smer == 'dopredu':
            param_motor = param_motor_leva_dopredu
        elif motor == 'pravy' and smer == 'dozadu':
            param_motor = param_motor_prava_dozadu
        elif motor == 'levy' and smer == 'dozadu':
            param_motor = param_motor_leva_dozadu
        print("test")
        i2c.write(0x70, b"\x00\x01")
        i2c.write(0x70, b"\xE8\xAA")
        i2c.write(0x70, param_motor + bytes([rychlost]))


if __name__ == "__main__":
    jed('pravy', 'dopredu', 100)
    jed('levy', 'dopredu', 100)
    sleep(1000)
    jed('pravy', 'dopredu', 0)
    jed('levy', 'dopredu', 0)
    sleep(1000)
    jed('pravy', 'dozadu', 100)
    jed('levy', 'dozadu', 100)
    sleep(1000)
    jed('pravy', 'dozadu', 0)
    jed('levy', 'dozadu', 0)
    sleep(1000)
    
