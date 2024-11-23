from microbit import i2c
from microbit import sleep

# na nasem konkretnim robotu se motory ovladaji pres
# komunikacni protokol i2c
# vice o i2c: https://cs.wikipedia.org/wiki/I%C2%B2C

# musime nastavit, s jakou rychlosti budeme na i2c komunikovat
# toto zalezi na HW - musime se podivat do manualu, kolik jak microbit,
# tak deska motoru umoznuji
# v nasem pripade umoznuji jak 100kHz tak 400kHz
# dobra praxe: zacnete s nizci rychlosti, pokud vse funguje
# prejdete na vyssi

i2c.init(freq=100000)

# nasledujici info bychom normalne nasli v manualu
# v tomto pripade jsem to vykoukala ze vzoroveho kodu joy-car
# v prvni rade musime "probudit" cip, ktery ovlada motory
# tyto prikazy jsou specificke pro naseho robota

#probud cip motoru
i2c.write(0x70, b"\x00\x01")
i2c.write(0x70, b"\xE8\xAA")

# nasledujici povely jsouu ziskane z dokumentace
# muzete to najit v manualu stavby robota na strane 44

# 0x02, 0x03 - kanaly pro PWM pro jeden motor
# 0-255 rozsah hodnot, kterym se ridi PWM
sleep(100)  # pro jistotu, aby mel cip se moznost probudit

i2c.write(0x70, b"\x05" + bytes([135]))  # rozjet motor
sleep(2000)
# zastav vsechny motory a vsechny smery
i2c.write(0x70, b"\x02" + bytes([0]))
i2c.write(0x70, b"\x03" + bytes([0]))
i2c.write(0x70, b"\x04" + bytes([0]))
i2c.write(0x70, b"\x05" + bytes([0]))
