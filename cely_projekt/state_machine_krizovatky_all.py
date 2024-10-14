from microbit import button_a, sleep, button_b
from cely_projekt import Robot, K, Obrazovka

from utime import ticks_diff, ticks_us

if __name__ == "__main__":

    st_start = "START"
    st_kalibruj = "KALIBRUJ"
    st_jed_po_care = "JED_PO_CARE"
    st_reaguj_na_krizovatku = "REAGUJ_NA_KRIZOVATKU"
    st_stop = "EXIT"
    st_cekam_na_tlacitko = "CEKAM"
    st_zatoc = "ZATOC"
    st_narovnej = "NAROVNEJ"
    st_mimo = "MIMO"

    stav = st_start
    Obrazovka.pis(stav)
    index_prikazu = 0

    robot = Robot(0.15, 0.067, False)

    # zmente na vase prikazy
    prikazy = [K.VPRAVO] * 10
    #napr prikazy = [K.ROVNE, K.ROVNE, K.VPRAVO]

    # zmente na vami odladene parametry jizdy po care
    dopredna = 0.1
    uhlova = 0.5
    zastav_za_krizovatkou = True # nastavte na False pokud nechcete, aby vam robot za kazdou krizovatkou cekal na tlacitko

    smer_narovnani = ""
    zatoceno = False

    while not button_a.was_pressed():
        if stav == st_start:
            if robot.inicializuj():
                stav = st_kalibruj
                Obrazovka.pis(stav)

        if stav == st_kalibruj:
            if robot.kalibruj(100,200,10) == 0:
                stav = st_cekam_na_tlacitko
                Obrazovka.pis(stav)
            else:
                break

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

        elif stav == st_narovnej:
            senzoricka_data = robot.senzory.precti_senzory()
            if smer_narovnani == "":
                if senzoricka_data[K.LV_S_CARY]:
                    smer_narovnani = K.LEVY
                elif senzoricka_data[K.PR_S_CARY]:
                    smer_narovnani = K.PRAVY
                elif senzoricka_data[K.PROS_S_CARY]:
                    zatocil = True
                else: # ztracen
                    zatocil = False
                    #stav = st_mimo TODO
                    Obrazovka.pis(stav)

            if smer_narovnani == K.LEVY:
                zatocil = robot.zatoc(0,2, K.PROS_S_CARY)
            elif smer_narovnani == K.PRAVY:
                zatocil = robot.zatoc(0,-2, K.PROS_S_CARY)

            if zatocil:
                if zatoceno:
                    zatoceno = False
                    stav = st_jed_po_care
                else:
                    stav = st_zatoc
                Obrazovka.pis(stav)
                smer_narovnani = ""

        elif stav == st_zatoc:
            zatocil = False

            if prikazy[index_prikazu] == K.VPRAVO:
                zatocil = robot.zatoc(0,-2, K.PR_S_CARY)
            else:
                zatocil = robot.zatoc(0,2, K.LV_S_CARY,)

            if zatocil:
                index_prikazu += 1
                if index_prikazu == len(prikazy):
                    stav = st_stop
                else:
                    stav = st_narovnej
                    zatoceno = True

                Obrazovka.pis(stav)

        elif stav == st_stop:
            robot.jed(0, 0)
            break

        robot.aktualizuj_se(False)
        sleep(5)

    robot.jed(0, 0)
