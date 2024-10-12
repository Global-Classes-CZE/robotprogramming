from microbit import button_a, sleep, button_b
from cely_projekt import Robot, K, Obrazovka, KalibracniFaktory

from utime import ticks_diff, ticks_us

if __name__ == "__main__":

    st_start = "START"
    st_jed_po_care = "JED_PO_CARE"
    st_reaguj_na_krizovatku = "REAGUJ_NA_KRIZOVATKU"
    st_stop = "EXIT"
    st_cekam_na_tlacitko = "CEKAM"

    stav = st_start
    Obrazovka.pis(stav)
    index_prikazu = 0

    # zmente na vase kalibracni faktory
    kalib_l = KalibracniFaktory(0.93, 51, 37, 17.08, 28.64)
    kalib_p = KalibracniFaktory(1.39, 55, 47, 20.98, 60.16)
    robot = Robot(0.15, 0.067, kalib_l, kalib_p, False)

    # zmente na vase prikazy
    prikazy = [K.ROVNE] * 10
    #napr prikazy = [K.ROVNE, K.ROVNE, K.VPRAVO]

    # zmente na vami odladene parametry jizdy po care
    dopredna = 0.1
    uhlova = 0.5
    zastav_za_krizovatkou = True # nastavte na False pokud nechcete, aby vam robot za kazdou krizovatkou cekal na tlacitko

    while not button_a.was_pressed():
        if stav == st_start:
            if robot.inicializuj():
                stav = st_jed_po_care
                Obrazovka.pis(stav)

        elif stav == st_jed_po_care:
            situace = robot.vycti_senzory_cary()
            if situace == K.CARA:
                robot.jed_po_care(dopredna, uhlova)
            elif situace == K.KRIZOVATKA:
                stav = st_reaguj_na_krizovatku
                Obrazovka.pis(stav)
            # elif situace == K.ZTRACEN:
            # TODO

        elif stav == st_reaguj_na_krizovatku:
            if index_prikazu == len(prikazy):
                stav = st_stop
                Obrazovka.pis(stav)
            else:
                dopredna_popojeti = 0.1
                # if prikazy[index_prikazu] == K.VZAD:
                #    dopredna = -0.1

                popojel = robot.popojed(dopredna_popojeti, 500000)

                if popojel:
                    if zastav_za_krizovatkou:
                        robot.jed(0, 0)
                        stav = st_cekam_na_tlacitko
                    else:
                        if (prikazy[index_prikazu] == K.ROVNE):  # or prikazy[index_prikazu] == K.VZAD:
                            index_prikazu += 1
                            stav = st_jed_po_care
                        else:
                            stav = st_narovnej
                    Obrazovka.pis(stav)

        elif stav == st_cekam_na_tlacitko:
            if button_b.was_pressed():
                if (prikazy[index_prikazu] == K.ROVNE):  # or prikazy[index_prikazu] == K.VZAD:
                    index_prikazu += 1
                    stav = st_jed_po_care
                else:
                    stav = st_narovnej
                Obrazovka.pis(stav)

        elif stav == st_stop:
            robot.jed(0, 0)
            break

        robot.aktualizuj_se()
        sleep(5)

    robot.jed(0, 0)
