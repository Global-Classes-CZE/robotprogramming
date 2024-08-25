from microbit import sleep
from microbit import pin14
from microbit import pin15
from microbit import button_a

tiky = 0  # globalni promena

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

    return tiky

if __name__ == "__main__":

   # misto vypisu vidi/nevidi vypisujte tiky
    while not button_a.was_pressed():
        data_enkoderu = enkoder_signal("levy_enkoder")
        if data_enkoderu == 1:
            print("levy enkoder vidi")
        elif data_enkoderu == 0:
            print("levy enkoder nevidi")
        else:
            print("jsem tululum a upsala jsem se nekde v nazvu enkoderu :)")
        sleep(100)
