from microbit import i2c
from microbit import sleep

# Motor je typu string a muze mit hodnoty “pravy” a “levy”
# Smer je typu string a muze mit hodnoty “dopredu”, “dozadu”
# Rychlost je celociselne cislo od 0-255
# Napoveda: budete potrebovat podminky if/else v kodu
def jed(motor, smer, rychlost):
    rychlost = min(rychlost, 255)
    rychlost = max(rychlost, 0)
    if motor == "pravy":
        if smer == "dopredu":
            i2c.write(0x70, b"\x03" + bytes([rychlost]))
        else:
            i2c.write(0x70, b"\x02" + bytes([rychlost]))
    else:
        if smer == "dopredu":
            i2c.write(0x70, b"\x05" + bytes([rychlost]))
        else:
            i2c.write(0x70, b"\x04" + bytes([rychlost]))


# Motor je typu string a muze mit hodnoty “pravy” a “levy”
def zastav(motor):
    jed(motor, 'dopredu', 0)
    jed(motor, 'dozadu', 0)

if __name__ == "__main__":
    i2c.init(freq=100000)

    # probud cip motoru
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")

    # TODO predelelejte tento kod, aby robot jel 1s vpred
    jed("pravy", "dopredu", 128)
    jed("levy", "dopredu", 128)
    sleep(1000)
    
    # pak zastavil na 1s
    zastav("pravy")
    zastav("levy")
    sleep(1000)
    
    # pak se rozjel vzad po dobu 1s
    jed("pravy", "dozadu", 128)
    jed("levy", "dozadu", 128)
    sleep(1000)
    # a pak zastavil a kod se vypnul
    zastav("pravy")
    zastav("levy")
