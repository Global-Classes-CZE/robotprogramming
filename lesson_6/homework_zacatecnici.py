from microbit import i2c
from microbit import sleep

# Motor je typu string a muze mit hodnoty “pravy” a “levy”
# Smer je typu string a muze mit hodnoty “dopredu”, “dozadu”
# Rychlost je celociselne cislo od 0-255
# Napoveda: budete potrebovat podminky if/else v kodu
def jed(motor, smer, rychlost):
    # TODO

# Motor je typu string a muze mit hodnoty “pravy” a “levy”
def zastav(motor):
    # TODO

if __name__ == "__main__":
    i2c.init(freq=100000)

    # probud cip motoru
    i2c.write(0x70, b"\x00\x01")
    i2c.write(0x70, b"\xE8\xAA")

    # TODO predelelejte tento kod, aby robot jel 1s vpred
    # pak zastavil na 1s
    # pak se rozjel vzad po dobu 1s
    # a pak zastavil a kod se vypnul
    # 0x02, 0x03
    # 0-255
    sleep(100)
    i2c.write(0x70, b"\x05" + bytes([135]))
    sleep(2000)
    i2c.write(0x70, b"\x02" + bytes([0]))
    i2c.write(0x70, b"\x03" + bytes([0]))
    i2c.write(0x70, b"\x04" + bytes([0]))
    i2c.write(0x70, b"\x05" + bytes([0]))
