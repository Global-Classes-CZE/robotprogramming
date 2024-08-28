from micropython import const
from utime import ticks_ms
from microbit import pin14, pin15, sleep, i2c

ROBOT_TicksPerCircle = const(40)                            # Pocet tiku na jednu otáčku kola (2 * 20)

class SpeedTicks:
    LIMIT = const(101)                                      # pocet desetin pro ktere si pamatujeme hodnoty

    def __init__(self):
        self.countValues = 0
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
        if self.countValues < self.LIMIT:                   # jeste nemame vsechny hodnoty pole zaplnene?
            self.countValues += 1                           # ano -> pricteme ze mame dalsi hodnotu
        self.index = newIndex                               # zapamatujeme si novy index
        self.times[self.index] = time                       #  ulozime cas do tohoto indexu
        self.ticks[self.index] = ticks                      #  ulozime tiky do tohoto indexu

    def run(self, ticks):                                   # Nech nas pracovat. Musime volat dostatecne casto (minimalne jednou za desetinu sekundy)
        time = ticks_ms()                                   # precteme cas v ms
        newIndex = self.getNewIndex(time)                   # spocti novy index z casu
        if newIndex >= 0:                                   # mame novy index?
            self.nextValues(newIndex, time, ticks)          # ano -> ulozime nove hodnoty pro tento index

    def calculate(self, countTenths=10):                    # Spocti rychlost tiku (tick/s), pouzij k tomu data dlouha countTenths (desetin sekundy)
        if countTenths<1 or countTenths>=self.countValues:  # je hodnota pocetDesetin vyhovujici (budeme ji umet spocitat)?
            if self.countValues < 2:                        # ne    mame alespon 2 hodnoty pro spocteni rychlosti?
                return 0                                    #       ne -> vratime rychlost 0 (jsme na zacatku a snad nikam nejedeme)
            else:
                if self.countValues >= 10:                  #       mame alespon 10 hodnot?
                    countTenths = 10                        #           ano -> nahradime nevhodnou delku implicitni hodnotou 10
                else:
                    countTenths = self.countValues          # ne  -> nahradime delku maximalni moznou (kolik mame dat)
        endIndex = self.index                               # koncovy index pro data (kde konci casove okno)
        startIndex = (endIndex - countTenths) % self.LIMIT  # spocteme pocatecni index (pro data pred lengt "desetinami")
        diffTimes = self.times[endIndex] - self.times[startIndex] # spocti rozdil tiku za cca pocetDesetin
        diffTicks = self.ticks[endIndex] - self.ticks[startIndex] # spocti rozdil casu za cca pocetDesetin
        return 1000 * diffTicks / diffTimes                 # rychlost = pocet tiku za 1s (tj. za 1000ms)

class Ticks:
    UP = const(1)                                           # smer nahoru = pricitame(kolo se toci dopredu)
    DOWN = const(2)                                         # smer dolu = odecitame (kole se toci dozadu)

    def __init__(self, pin):
        self.pin = pin                                      # pin na kterem budeme sledovat tiky
        self.actualPinValue = self.readPin()                # precteme aktualni hodnotu na pinu
        self.lastPinValue = self.actualPinValue             #   a ulozime si ji i jako lastValue
        self.count = 0                                      # pocet tiku (od zacateku)
        self.setDirection(self.UP)                          # smer pocitani (pricitat/odecitat)
        self.speed = SpeedTicks()                           # objekt ktery umi spociat rychlost

    def readPin(self):                                      # Precti hodnotu na pinu
        return self.pin.read_digital()

    def setDirection(self, value):                          # Nastav smer
        self.direction = value

    def getCount(self):                                     # Dej mi celkovy pocet
        return self.count

    def nextTick(self):                                     # Dalsi tik
        if self.direction == self.UP:                       # Mame pocitat nahoru (pricitat)?
            self.count += 1                                 # ano -> pricti 1
        else:
            self.count -= 1                                 # ne -> odecti 1

    def getSpeed_InTick(self, countTenths=10):              # Dej mi rychlost spocitanou z dat starych "pocet desetin sekundy"
        return self.speed.calculate(countTenths)

    def getSpeed_InRad(self, countTenths=10):               # Dej mi rychlost spocitanou z dat starych "pocet desetin sekundy"
        return self.getSpeed_InTick(countTenths) / ROBOT_TicksPerCircle * 6.28

    def rychlost_otaceni(self):                             # Jmeno funkce pozadovane zadanim
        return self.getSpeed_InRad()

    def run(self):                                          # Merici funkce, musi se volat dostatecne casto (rychleji nez nastavaji zmeny na pin-u)
        self.actualPinValue = self.readPin()                # Precti pin, ktery kontrolujeme
        if self.actualPinValue != self.lastPinValue:        # Nastala zmena hodnoty pinu?
            self.nextTick()                                 # ano -> zapocitec dalsi ticks
            self.lastPinValue = self.actualPinValue         #        a zapamatujeme se zmenenou hodnotu
        self.speed.run(self.getCount())                     # nech i objektu rychlost moznost pracovat

class Engine:
    def __init__(self, jmeno, pin):
        self.jmeno = jmeno
        self.encoder = Ticks(pin)

        i2c.init(freq=400000)
        sleep(100)
        #probud cip motoru
        i2c.write(112, bytes([0x00, 0x01])
        i2c.write(112, bytes([0xE8, 0xAA])

    def jed_PWM(self, smer, PWM):
        if(self.jmeno == "levy"):
            if(smer=="dopredu"):
                i2c.write(0x70, b"\x05" + bytes([PWM]))
                return 0
        return -1

    def run(self):
        self.encoder.run()

def main():
    leftEngine = Engine("levy", pin14)
    speedUp = [0] * self.256
    speedDown = [0] * self.256
#    rightEngine = Engine("pravy", pin15)
    for pwm in range(256):
        leftEngine.jed_PWM("dopredu", pwm)              # nastavime hodnotu PWM
        for i in range(150):                            # pockame 1s pred zmenou rychlost ale budeme porad merit rychlost
            leftEngine.run()                            # merici funkci musime volat dostatecne casto
            sleep(10)
        speedUp[pwm] = leftEngine.encoder.getSpeed_InRad()

    for pwm in range(256):
        leftEngine.jed_PWM("dopredu", 255-pwm)          # nastavime hodnotu PWM sestupne
        for i in range(150):                            # pockame 1s pred zmenou rychlost ale budeme porad merit rychlost
            leftEngine.run()                            # merici funkci musime volat dostatecne casto
            sleep(10)
        speedDwon[255-pwm] = leftEngine.encoder.getSpeed_InRad()

    for pwm in range(256):
        print((pwm, speedUp[pwm]))



if __name__ == "__main__" :
    main()
