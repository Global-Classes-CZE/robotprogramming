from microbit import button_a
from microbit import button_b
from WheelDriver import WheelDriver
import time

if __name__ == "__main__":
    # Pocitejte nove tiky pro leve a prave kolo

    # Reseni pouziva aktivni rychle tikajici smycku, ktera se zastavi tlacitkem B
    # a vypise vysledky tlacitkem A. Smycka pouziva non-blocking cteni senzoru
    # pri update stavu kazdeho kola.
    wheel_driver = WheelDriver()
    wheel_driver.move(100, 150)  # nerovnomerny pohyb (at je co sbirat)
    phase_length = 1000  # kazdou sekundu vypiseme po testu tlacitkem
    phase_start = time.ticks_ms()
    while not button_b.was_pressed():
        if time.ticks_diff(time.ticks_ms(), phase_start) > phase_length:
            phase_start = time.ticks_ms()
            while button_a.was_pressed():
                (levy_encoder, pravy_encoder) = wheel_driver.get_ticks()
                print("levy enc: %d, pravy enc: %d" % (levy_encoder, pravy_encoder))
        wheel_driver.update()
        time.sleep(0.01)
    print("Finished")
