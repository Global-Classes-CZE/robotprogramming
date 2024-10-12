from kalibrace import Kalibrace
from cely_projekt import Konstanty

if __name__ == "__main__":

    kalibrace = Kalibrace(0.067, Konstanty.DOPREDU, "zpomaluj", False, False)
    kalibrace.kalibruj()
