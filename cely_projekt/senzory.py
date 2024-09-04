from microbit import i2c

class Senzory:

    # konstruktor
    # nova_verze = True znamena, ze enkodery jsou pripojene na piny 14, 15 (vas pripad)
    # nova_verze = False znamena, ze enkodery jsou pripojene pres i2c (Lenky pripad)

    def __init__(self, nova_verze=True, debug=False):
        self.nova_verze = nova_verze
        self.DEBUG = debug

    def precti_senzory(self):
        # na nasi stavebnici jsou nektere senzory pripojeny
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
        # mame celkove 5 senzoru pripojenych do IO expanderu, tzn chceme vycist 5 bitu
        # minimalni mnozstvi, ktere muzeme vycist je ale v bytech
        # tzn je to 1byte, coz je 8 bitu

        surova_data_byte = i2c.read(0x38, 1)
        if self.DEBUG:
            print("surova data", surova_data_byte)

        # chceme prevest vycteny byte na bity, abychom se dostali k informaci ze senzoru
        bitove_pole = self.__byte_na_bity(surova_data_byte)

        # uz bychom mohli vratit to cele bitove_pole, ale muzeme to jeste vyhezkat
        # tzn dat jednotlivym polozkam spravne jmeno, pro ktery senzor to je
        # zde pouzijeme datavou strukturu "dictionary", tzn slovnik
        # https://naucse.python.cz/lessons/beginners/dict/
        senzoricka_data = {}  # vytvorim si prazdny slovnik

        # kazdemu prvku z bitoveho_pole chceme priradit spravne jmeno
        # ze stranky 48 manualu jsem vykoukala
        # v jakem poradi jsou senzory zapojene do IO expanderu
        # experimentalne jsem overila, ze v bitove_poli je to v opacnem poradi,
        # bitove_pole neni jen 8 bitu, ale je to ve tvaru 0b<nasich_bitu>,
        # tzn to musim jeste o 2 pozice posunout

        if not self.nova_verze:
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

    # v micropythonu existuje knihovna, kterou bychom si mohli doinstalovat, napr:
    # https://bitstring.readthedocs.io/en/stable/
    # nicmene to lze vyresit i "rucne", viz tato metoda
    # zakladni trik pracuje s tim, ze si muzeme vytvorit int z bytu
    # a ten int pak prevedu na bity
    def __byte_na_bity(self, data_bytes):
        # https://docs.micropython.org/en/latest/library/builtins.html
        # https://docs.python.org/3/library/stdtypes.html#int.from_bytes
        # druhy parameter znamena "Endianitu": https://cs.wikipedia.org/wiki/Endianita
        data_int = int.from_bytes(data_bytes, "big")
        # https://docs.python.org/3/library/functions.html#bin
        bit_pole_string = bin(data_int)

        if self.DEBUG:
            print("data_int", data_int)
            print("bit pole", bit_pole_string)

        return bit_pole_string



