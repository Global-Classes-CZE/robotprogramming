from microbit import i2c
from microbit import i2c
from microbit import sleep
from microbit import button_a

DEBUG = True

# v micropythonu existuje knihovna, kterou bychom si mohli doinstalovat, napr:
# https://bitstring.readthedocs.io/en/stable/
# nicmene to lze vyresit i "rucne", viz tato metoda
# zakladni trik pracuje s tim, ze si muzeme vytvorit int z bytu
# a ten int pak prevedu na bity
def byte_na_bity(data_bytes):
    # https://docs.micropython.org/en/latest/library/builtins.html
    # https://docs.python.org/3/library/stdtypes.html#int.from_bytes
    # druhy parameter znamena "Endianitu": https://cs.wikipedia.org/wiki/Endianita
    data_int = int.from_bytes(data_bytes, "big")
    # https://docs.python.org/3/library/functions.html#bin
    bit_pole_string = bin(data_int)

    if DEBUG:
        print("data_int", data_int)
        print("bit pole", bit_pole_string)

    return bit_pole_string

# IO Expander Read data and store in sen_data
def precti_senzory():
    # na nasi stavebnici jsou vsechny senzory (az na ultrazvukovy) pripojeny
    # pres tzv. IO expander
    # IO expander znamena Input Output rozsirovac
    # podivejte na stranku 48 manualu (toho, podle ktereho jste to staveli)
    # IO expander je pripojen take pres i2c a ma adresu 0x38
    # takze prvni krok je vycist data
    # zde se vyctou data ze vsech senzoru pripojenych k expanderu
    # i2c.read ma dva alespon dva povinne parametery:
    # https://microbit-micropython.readthedocs.io/en/latest/i2c.html
    # adresa a pocet bytu, ktere cheme vycist
    # na nasi stavebnici, kazdy ze senzoru vraci jen True/False, tzn 1 bit
    # mame celkove 7 senzoru pripojenych do IO expanderu, tzn chceme vycist 7 bitu
    # minimalni mnozstvi, ktere muzeme vycist je ale v bytech
    # tzn je to 1byte, coz je 8 bitu
    surova_data_byte = i2c.read(0x38, 1)
    if DEBUG:
        print("surova data", surova_data_byte)

    # chceme prevest vycteny byte na bity, abychom se dostali k informaci ze senzoru
    bitove_pole = byte_na_bity(surova_data_byte)

    # uz bychom mohli vratit to cele bitove_pole, ale muzeme to jeste vyhezkat
    # tzn dat jednotlivym polozkam spravne jmeno, pro ktery senzor to je
    # zde pouzijeme datavou strukturu "dictionary", tzn slovnik
    # https://naucse.python.cz/lessons/beginners/dict/

    senzoricka_data = {}  # vytvorim si prazdny slovnik

    # kazdemu prvku z bitoveho_pole chceme priradit spravne jmeno
    # ze stranky 48 manualu jsem vykoukala
    # v jakem poradi jsou senzory zapojene do IO expanderu
    # napr levy_enkoder je pripojen na pin0
    # experimentalne jsem overila, ze v bitove_poli to ale neodpovida polozce [0],
    # ale naopak te nejvice v pravo
    # bitove_pole neni jen 8 bitu, ale je to ve tvaru 0b<nasich_bitu>,
    # tzn to musim jeste o 2 pozice posunout

    senzoricka_data["levy_enkoder"] = bitove_pole[9]
    senzoricka_data["pravy_enkoder"] = bitove_pole[8]
    senzoricka_data["levy_sledovac_cary"] = bitove_pole[7]
    senzoricka_data["prostredni_sledovac_cary"] = bitove_pole[6]
    senzoricka_data["pravy_sledovac_cary"] = bitove_pole[5]
    senzoricka_data["levy_IR"] = bitove_pole[4]
    senzoricka_data["pravy_IR"] = bitove_pole[3]
    # pripominka - my mame jen 7 senzoru, ale vycetli jsme 1 byte,
    # tzn 8. bit na pozici [2] je nejaky "duch", o ktery nam tu nejde
    # pozice [1] je pismeno "b", o tom nam taky nejde
    # pozice [0] je vzdy 0, taky nam o to nejde

    return senzoricka_data

def enkoder_signal(jmeno_enkoderu):
    senzoricka_data = precti_senzory()
    if DEBUG:
        print(senzoricka_data)

    if jmeno_enkoderu == "pravy_enkoder":
        return int(senzoricka_data["pravy_enkoder"])
    elif jmeno_enkoderu == "levy_enkoder":
        return int(senzoricka_data["levy_enkoder"])
    else:
        print("Zadali jste nepodporovane jmeno")
        return -1


if __name__ == "__main__":

    # puste si kod a jemne si levy kolem pohybujte,
    # meli byste videt, ze se meni kdy levy enkoder vidi a nevidi
    DEBUG = False  # nastavte na True pokud chcete videt pomocne vypisy

    i2c.init(freq=400000)

    while not button_a.was_pressed():
        data = enkoder_signal("levy_enkoder")
        if data == 1:
            print("levy enkoder vidi")
        elif data == 0:
            print("levy enkoder nevidi")
        else:
            print("jsem tululum a upsala jsem se nekde v nazvu enkoderu :)")
        sleep(1000)
