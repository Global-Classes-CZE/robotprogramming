# vyuziti knihoven
# softwarova knihovna - kolekce predpripravenych programu nekym jinym,
# ktery muzeme s vyhodou pouzit
# vice na: https://cs.wikipedia.org/wiki/Knihovna_(programov%C3%A1n%C3%AD)

# nekdy muzeme videt zapis "import microbit"
# nebo "from microbit import *"
# tyto zapisy nedoporucuji - do programu se vlozi uplne vse,
# co je v knihovne s nazvem "microbit"
# je to jako kdybychom si na vylet do Krkonos vzali mapu sveta
# budeme zbytecne tahat s sebou zatez, ktera je k nam k nicemu
# tady to zbytecne zvetsuje kod

# prehled funkci knihovny microbit:
# https://microbit-micropython.readthedocs.io/en/v2-docs/microbit_micropython_api.html

from microbit import sleep
from microbit import button_a
from microbit import display

# funkce ma tzv. defaultni parametr - tento string se pouzije,
# pokud funkci nic nezadame

def display_text(text="Ahoj"):
    '''Funkce, ktera vypise zadany text na obrazovku tak dlouho,
    dokud nezmackneme tlacitko A'''

    while not button_a.was_pressed():
        display.scroll(text)
        sleep(1000)

display_text()  # nic zadano, pouzije se defaultni parameter
display_text("robote!")  # pouzije se tento zadany string
