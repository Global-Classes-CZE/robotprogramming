from time import ticks_ms, ticks_diff, sleep

from microbit import button_a
from microbit import button_b

from WheelDriver import WheelDriver

if __name__ == "__main__":
    # Pocitejte nove tiky pro leve a prave kolo

    # Reseni pouziva aktivni rychle tikajici smycku, ktera se zastavi tlacitkem B
    # a vypise vysledky tlacitkem A. Smycka pouziva non-blocking cteni senzoru
    # pri update stavu kazdeho kola.
    print("Starting")
    wheel_driver = WheelDriver()
    wheel_driver.move(100, 150)  # nerovnomerny pohyb (at je co sbirat)
    phase_length = 1000  # kazdou sekundu vypiseme po testu tlacitkem
    phase_start = ticks_ms()
    while not button_b.was_pressed():
        if ticks_diff(ticks_ms(), phase_start) > phase_length:
            phase_start = ticks_ms()
            while button_a.was_pressed():
                print("levy tachometr: %s" % wheel_driver.wheel_left.tachometer)
                print("pravy tachometr: %s" % wheel_driver.wheel_right.tachometer)
        wheel_driver.update()
        sleep(0.01)
    wheel_driver.stop()
    print("Finished")
