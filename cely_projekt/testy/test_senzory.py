from senzory import Senzory

def zakladni_test_spusteni():
    try:
        senzory = Senzory()
        senzory.precti_senzory()
        return 1
    except:
        return 0


if __name__ == "__main__":
    print(zakladni_test_spusteni(), "zakladni_test_spusteni")
