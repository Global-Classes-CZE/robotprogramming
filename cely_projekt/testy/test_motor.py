from microbit import i2c, button_a, sleep
from cely_projekt import Motor, KalibracniFaktory, Konstanty

def test_konstruktor_string_levy():
    hodnota_testu = -1
    try:
        motor = Motor("levy", 0.067)
        hodnota_testu = 1
    except AttributeError as e:
        print(e)
        hodnota_testu = 0
    return hodnota_testu

def test_konstruktor_string_pravy():
    hodnota_testu = -1
    try:
        motor = Motor("pravy", 0.067)
        hodnota_testu = 1
    except AttributeError as e:
        print(e)
        hodnota_testu = 0
    return hodnota_testu

def test_konstruktor_konstakty_levy():
    hodnota_testu = -1
    try:
        motor = Motor(Konstanty.LEVY, 0.067)
        hodnota_testu = 1
    except AttributeError as e:
        print(e)
        hodnota_testu = 0
    return hodnota_testu

def test_konstruktor_konstanty_pravy():
    hodnota_testu = -1
    try:
        motor = Motor(Konstanty.PRAVY, 0.067)
        hodnota_testu = 1
    except AttributeError as e:
        print(e)
        hodnota_testu = 0
    return hodnota_testu

def test_konstruktor_prazdny():
    hodnota_testu = -1
    try:
        motor = Motor()
        hodnota_testu = 0
    except:
        hodnota_testu = 1
    return hodnota_testu

def test_konstruktor_nahodny_retezec():
    hodnota_testu = -1
    try:
        motor = Motor("fsdfsd", 0.067)
        hodnota_testu = 0
    except AttributeError as e:
        print(e)
        hodnota_testu = 1
    return hodnota_testu

def test_konstruktor_velke_pismeno():
    hodnota_testu = -1
    try:
        motor = Motor("Levy", 0.067)
        hodnota_testu = 0
    except AttributeError as e:
        print(e)
        hodnota_testu = 1
    return hodnota_testu

def test_inicializace():
    motor = Motor("levy", 0.067)
    motor.inicializuj()
    return int(motor.__inicializovano)

def test_kalibrace_po_inicializaci():
    motor = Motor("levy", 0.067)
    motor.inicializuj()
    hodnota = motor.kalibrace()
    if hodnota == 0:
        return 1
    else:
        return 0

def test_kalibrace_bez_inicializaci():
    motor = Motor("levy", 0.067)
    hodnota = motor.kalibrace()
    if hodnota == -1:
        return 1
    else:
        return 0

def porovnej_floaty(a,b, rel_tol=1e-04, abs_tol=0.0):

    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def test_uhlova_01():
    motor = Motor("levy", 0.067)
    skutecna = motor.__dopredna_na_uhlovou(0.1052)
    print("skutecna", skutecna)
    ocekavana = Konstanty.PI
    return int(porovnej_floaty(ocekavana, skutecna))

def zakladni_test_spusteni(nova_verze):
    min_rychlost = 2.165826 # ziskej z excelu
    min_pwm_rozjezd = 79 # kalibrace vytiskne na konci pri "zrychluj"
    min_pwm_dojezd = 41 # kalibrace vytiskne na konci pri "zpomaluj"
    a = 24.3732783404646 # ziskej z excelu
    b = 8.21172006498485 # ziskej z excelu

    levy_faktor = KalibracniFaktory(min_rychlost, min_pwm_rozjezd, min_pwm_dojezd, a, b)

    motor = Motor(Konstanty.LEVY, 0.067, levy_faktor, nova_verze)
    motor.inicializuj()
    motor.jed_doprednou_rychlosti(0.067*Konstanty.PI)
    while not button_a.was_pressed():
        if motor.aktualizuj_se() < 0:
            break
        sleep(5)

    motor.jed_doprednou_rychlosti(0)

if __name__ == "__main__":
    i2c.init(4000000)

    #False - Lenka stara verze robota
    #True - vase verze
    zakladni_test_spusteni(True)





