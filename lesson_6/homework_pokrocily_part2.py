from microbit import sleep
from microbit import pin14
from microbit import pin15
from microbit import button_a

tiky = 0  # globalni promena
data = 0


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
    global data
    data_enkoderu = enkoder_signal(jmeno_enkoderu)
    if data != data_enkoderu:
        tiky += 1
        data = data_enkoderu
    return tiky


if __name__ == "__main__":

    # misto vypisu vidi/nevidi vypisujte tiky
    while not button_a.was_pressed():
        pocet_tiku("levy_enkoder")
        print(tiky)
        sleep(100)
