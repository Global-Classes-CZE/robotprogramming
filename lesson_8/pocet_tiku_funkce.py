# vzorove reseni pocet tiku - mozny pristup, ale ne idealni

from microbit import sleep

from tridy import Senzory

def pocet_tiku(aktualni_hodnota, posledni_hodnota, tiky_celkem):
    # pokud je posledni merena hodnota jina nez aktualni hodnota
    # jedna se o zmenu a tedy tik!
    if posledni_hodnota != aktualni_hodnota:
        # tento radek znamena to same jako tiky_celkem = tiky_celkem + 1
        tiky_celkem += 1
        # musime si zapamatovat aktualni hodnotu, jako tu posledne videnou
        posledni_hodnota = aktualni_hodnota

    return tiky_celkem

if __name__ == "__main__":

    # vytvorim objekt podle tridy Senzory()
    # volam konstruktor
    senzory = Senzory()

    senzoricka_data = senzory.precti_senzory()
    posledni_hodnota = senzoricka_data["levy_enkoder"]
    print("main: posledni_hodnota", posledni_hodnota)

    print("pootocte kolem")
    sleep(2000)

    senzoricka_data = senzory.precti_senzory()
    aktualni_hodnota = senzoricka_data["levy_enkoder"]
    print("main: aktualni_hodnota", aktualni_hodnota)

    tiky = 0
    tiky = pocet_tiku(aktualni_hodnota, posledni_hodnota, tiky)
    print("pocet_tiku", tiky)

