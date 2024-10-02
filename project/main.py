# from time import sleep

from Robot import Robot
from microbit import button_a, sleep

if __name__ == "__main__":

    robot = Robot(0.147, 0.067)
    sleep(1000)
    robot.go(120, 0)
    # sleep(1000)
    # robot.go(0, 1350)
    # sleep(1000)
    # robot.go(0, -1350)
    # sleep(1000)
    # robot.go(0, 0)
    # sleep(1000)
    # robot.inicializuj()
    #
    # dopredna = 0.1
    # uhlovaRad = 0.5
    # perioda_regulace = 100
    # cas_minule = ticks_ms()
    #
    # robot.jed(dopredna, 0)

    while not button_a.was_pressed():
        robot.tick()
        # sleep(1)
    # data = senzory.precti_senzory()
    #
    # # jak casto vycitat hodnoty??
    # # cara_width = 0.018 # sirka cary 18 milimetru
    # # uhlovaRad 0.5 je 28,647889 stupnu → 28° … za 1 sec se bude otacet robot
    # # 0.058 m jsou senzory od stredu robota
    # # obvod (o=2πr) → 2*0.058*3.1415 = 0.3644 m ← obcod po kterém se pohybují senzory
    # # 0.3644 m .... 360°
    # # šířka čáry je 0.018 m → (0.018*360)/0.3644 → 17.78°
    # # ╰→ tzn. čára zabírá 17.78°.
    # # Musím tedy alespoň 2x do sekunty vyčítat hodnotum protože úhlová rychlost (jak rychle zatočí) je 0.5 rad → ±28°
    #
    # if ticks_diff(ticks_ms(), cas_minule) > perioda_regulace:
    #
    #     doprednaTmp = dopredna
    #     uhlovaTmp = 0
    #
    #     if data[Konstanty.LV_S_CARY]:
    #         uhlovaTmp = uhlovaRad
    #     elif data[Konstanty.PR_S_CARY]:
    #         uhlovaTmp = uhlovaRad * -1
    #     elif (data[Konstanty.LV_S_CARY] + data[Konstanty.PR_S_CARY] + data[Konstanty.PROS_S_CARY]) == 0:
    #         doprednaTmp = 0
    #         uhlovaTmp = 0
    #     robot.jed(doprednaTmp, uhlovaTmp)
    #     print("S", int(data[Konstanty.LV_S_CARY]), int(data[Konstanty.PROS_S_CARY]), int(data[Konstanty.PR_S_CARY]),
    #           " ", doprednaTmp, ",", uhlovaTmp)
    #
    # robot.aktualizuj_se()
    # sleep(5)
    robot.go(0, 0)
    # robot.jed(0, 0)
