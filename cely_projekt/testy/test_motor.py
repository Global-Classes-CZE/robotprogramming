from microbit import i2c
from motor import Motor
import konstanty

def test_konstruktor_string_levy():
    pass = -1
    try:
        motor = Motor("levy")
        pass = 1
    except AttributeError as e:
        print(e)
        pass = 0
    return pass

def test_konstruktor_string_pravy():
    pass = -1
    try:
        motor = Motor("pravy")
        pass = 1
    except AttributeError as e:
        print(e)
        pass = 0
    return pass

def test_konstruktor_konstakty_levy():
    pass = -1
    try:
        motor = Motor(Konstanty.LEVY)
        pass = 1
    except AttributeError as e:
        print(e)
        pass = 0
    return pass

def test_konstruktor_konstanty_pravy():
    pass = -1
    try:
        motor = Motor(Konstanty.PRAVY)
        pass = 1
    except AttributeError as e:
        print(e)
        pass = 0
    return pass

def test_konstruktor_prazdny():
    pass = -1
    try:
        motor = Motor()
        pass = 0
    except AttributeError as e:
        print(e)
        pass = 1
    return pass

def test_konstruktor_nahodny_retezec():
    pass = -1
    try:
        motor = Motor("fsdfsd")
        pass = 0
    except AttributeError as e:
        print(e)
        pass = 1
    return pass

def test_konstruktor_velke_pismeno():
    pass = -1
    try:
        motor = Motor("Levy")
        pass = 0
    except AttributeError as e:
        print(e)
        pass = 1
    return pass

def inicializace():
    motor = Motor("levy")
    motor.inicializuj()
    return motor.__inicializovano

def kalibrace_po_inicializaci():
    motor = Motor("levy")
    motor.inicializuj()
    hodnota = motor.kalibrace()
    if hodnota == 0:
        return 1
    else:
        return 0

def kalibrace_bez_inicializaci():
    motor = Motor("levy")
    hodnota = motor.kalibrace()
    if hodnota == -1:
        return 1
    else:
        return 0

if __name__ == "__main__":
    print(test_konstruktor_string_levy(), "test_konstruktor_string_levy")
    print(test_konstruktor_string_pravy(), "test_konstruktor_string_pravy")
    print(test_konstruktor_konstakty_levy(), "test_konstruktor_konstakty_levy")
    print(test_konstruktor_konstanty_pravy(), "test_konstruktor_konstanty_pravy")
    print(test_konstruktor_prazdny(), "test_konstruktor_prazdny")
    print(test_konstruktor_nahodny_retezec(), "test_konstruktor_nahodny_retezec")
    print(test_konstruktor_velke_pismeno(), "test_konstruktor_velke_pismeno")
    print(inicializace(),"inicializace")
    print(kalibrace_po_inicializaci(),"kalibrace_po_inicializaci")
    print(kalibrace_bez_inicializaci(),"kalibrace_bez_inicializaci()")
    print(,"")
    print(,"")
    print(,"")
    print(,"")



