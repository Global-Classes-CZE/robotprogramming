from micropython import const
from utime import ticks_ms
from microbit import pin14, pin15, sleep

ROBOT_TicksPerCircle = const(40)                            # Pocet tiku na jednu otáčku kola (2 * 20)

class SpeedTicks:
    LIMIT = const(101)                                      # pocet desetin pro ktere si pamatujeme hodnoty

    def __init__(self):
        self.times = [0] * self.LIMIT
        self.ticks = [0] * self.LIMIT
        self.index = 0

    def getNewIndex(self, time):                            # Zjisti z casu jestli uz muzeme ulozit data do dalsiho indexu
        newIndex = (time // 100) % self.LIMIT               # cas na desetiny sekundy, a ukladame jich maximalne LIMIT
        if newIndex != self.index:                          # pokud je spocteny index jiny nez ulozeny
            return newIndex                                 #     tak ho vratime (mame novy index)
        else:
            return -1                                       # jinak vratime -1 (nemame novy index = musime jeste pockat)

    def nextValues(self, newIndex, time, ticks):            # Ulozime nove hodnoty do pole
        self.index = newIndex                               # zapamatujeme si novy index
        self.times[self.index] = time                       #  ulozime cas do tohoto indexu
        self.ticks[self.index] = ticks                      #  ulozime tiky do tohoto indexu

    def run(self, ticks):                                   # Nech nas pracovat
        time = ticks_ms()                                   # precteme cas v ms
        newIndex = self.getNewIndex(time)                   # spocti novy index z casu
        if newIndex >= 0:                                   # mame novy index?
            self.nextValues(newIndex, time, ticks)          # ano -> ulozime nove hodnoty pro tento index

    def calculate(self, pocetDesetin=10):                   # Spocti rychlost tiku (tick/s), pouzij k tomu data stara "pocet desetin"
        if pocetDesetin<1 or pocetDesetin>=self.LIMIT:      # je hodnota pocetDesetin vyhovujici (budeme ji umet spocitat)?
            pocetDesetin = 10                               # ne -> nahrad ji implicitni hodnotou
        newIndex = self.index                               # pro jistotu si vezmeme aktuali index do lokalni promenne (aby se nam pod rukama nezmenil)
        oldIndex = (newIndex - pocetDesetin) % self.LIMIT   # spocteme index pro data pred "poctem desetin"
        diffTimes = self.times[newIndex] - self.times[oldIndex] # spocti rozdil tiku za cca pocetDesetin
        diffTicks = self.ticks[newIndex] - self.ticks[oldIndex] # spocti rozdil casu za cca pocetDesetin
        return 1000 * diffTicks / diffTimes                 # rychlost = pocet tiku za 1s (tj. za 1000ms)

class Ticks:
    UP = const(1)                       # smer nahoru = pricitame(kolo se toci dopredu)
    DOWN = const(2)                     # smer dolu = odecitame (kole se toci dozadu)

    def __init__(self, pin):
        self.pin = pin                                  # pin na kterem budeme sledovat tiky
        self.actualPinValue = self.readPin()            # precteme aktualni hodnotu na pinu
        self.lastPinValue = self.actualPinValue         #   a ulozime si ji i jako lastValue
        self.count = 0                                  # pocet tiku (od zacateku)
        self.setDirection(self.UP)                      # smer pocitani (pricitat/odecitat)
        self.speed = SpeedTicks()                       # objekt ktery umi spociat rychlost

    def readPin(self):                                  # Precti hodnotu na pinu
        return self.pin.read_digital()

    def setDirection(self, value):                      # Nastav smer
        self.direction = value

    def getCount(self):                                 # Dej mi celkovy pocet
        return self.count

    def nextTick(self):                                 # Dalsi tik
        if self.direction == self.UP:                   # Mame pocitat nahoru (pricitat)?
            self.count += 1                             # ano -> pricti 1
        else:
            self.count -= 1                             # ne -> odecti 1

    def getSpeed_InTick(self, pocetDesetin=10):         # Dej mi rychlost spocitanou z dat starych "pocetDesetin"
        return self.speed.calculate(pocetDesetin)

    def getSpeed_InRad(self, pocetDesetin=10):          # Dej mi rychlost spocitanou z dat starych "pocetDesetin"
        return self.getSpeed_InTick(pocetDesetin) / ROBOT_TicksPerCircle * 6.28

    def run(self):                                      # Merici funkce, musi se volat dostatecne casto (minimalne jednou za desetinu sekundy)
        self.actualPinValue = self.readPin()            # Precti pin, ktery kontrolujeme
        if self.actualPinValue != self.lastPinValue:    # Nastala zmena hodnoty pinu?
            self.nextTick()                             # ano -> zapocitec dalsi ticks
            self.lastPinValue = self.actualPinValue     #        a zapamatujeme se zmenenou hodnotu
        self.speed.run(self.getCount())                 # nech i objektu rychlost moznost pracovat

def main():
    levy = Ticks(pin14)
    pravy = Ticks(pin15)
    while True:
        for i in range(100):
            levy.run()                  # musime volat dostatecne casto
            pravy.run()
            sleep(10)
        # Zobrazime rychlost
        print(
            "Rychlost:",
            "leve kolo=", levy.getSpeed_InRad(10), "rad/s",
            "prave kolo=", pravy.getSpeed_InRad(10), "rad/s",
        )

if __name__ == "__main__" :
    main()
