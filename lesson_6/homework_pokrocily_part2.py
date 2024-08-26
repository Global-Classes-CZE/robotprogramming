from microbit import sleep
from microbit import pin14
from microbit import pin15
from microbit import button_a

tiky = 0  # globalni promena
pe_predchozi_stav = 0
le_predchozi_stav = 0

def enkoder_signal(jmeno_enkoderu):
    if jmeno_enkoderu == "pravy_enkoder":
        return int(pin15.read_digital())
    elif jmeno_enkoderu == "levy_enkoder":
        return int(pin14.read_digital())
    else:
        print("Zadali jste nepodporovane jmeno")
        return -1

def pocet_tiku(jmeno_enkoderu):
    # TODO volejte funkce enkoder_signal a pocitejte nove tiky
    global tiky
    global pe_predchozi_stav
    global le_predchozi_stav

    if jmeno_enkoderu == "pravy_enkoder":
        pe_aktualni_stav = enkoder_signal("pravy_enkoder")

        if pe_aktualni_stav != pe_predchozi_stav:
            tiky += 1
            pe_predchozi_stav = pe_aktualni_stav

    if jmeno_enkoderu == "levy_enkoder":
        le_aktualni_stav = enkoder_signal("levy_enkoder")

        if le_aktualni_stav != le_predchozi_stav:
            tiky += 1
            le_predchozi_stav = le_aktualni_stav

    return tiky

if __name__ == "__main__":

   # misto vypisu vidi/nevidi vypisujte tiky
    while not button_a.was_pressed():
        pocet_tiku("pravy_enkoder")
        pocet_tiku("levy_enkoder")
        print(int(tiky))
        sleep(10)
