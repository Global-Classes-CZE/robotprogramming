from microbit import sleep
from microbit import button_a
from microbit import display


def display_text(text="Ahoj"):
    while not button_a.is_pressed():
        display.scroll(text)
        sleep(3000)

display_text()
