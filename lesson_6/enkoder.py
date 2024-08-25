from microbit import sleep
from microbit import pin14
from microbit import pin15
from microbit import button_a

def enkoder_signal(jmeno_enkoderu):
    if jmeno_enkoderu == "pravy_enkoder":
        return int(pin15.read_digital())
    elif jmeno_enkoderu == "levy_enkoder":
        return int(pin14.read_digital())
    else:
        print("Zadali jste nepodporovane jmeno")
        return -1

if __name__ == "__main__":

    while not button_a.was_pressed():
        data_enkoderu = enkoder_signal("levy_enkoder")
        if data_enkoderu == 1:
            print("levy enkoder vidi")
        elif data_enkoderu == 0:
            print("levy enkoder nevidi")
        else:
            print("jsem tululum a upsala jsem se nekde v nazvu enkoderu :)")
        sleep(100)
