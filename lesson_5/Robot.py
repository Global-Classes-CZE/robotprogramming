import time
from LightDriver import LightDriver, LightPlacement

class Robot:
    blink_freq_ms = 500

    def __init__(self):
        self.light_driver = LightDriver()

    def indikuj(self, smer_zataceni):
        '''Indikuje smer zataceni, pro ted string "doprava" nebo "doleva"'''
        if smer_zataceni == "doprava":
            self.light_driver.blink(LightPlacement.RIGHT_DIRECTION, self.blink_freq_ms)
        elif smer_zataceni == "doleva":
            self.light_driver.blink(LightPlacement.LEFT_DIRECTION, self.blink_freq_ms)
        else:
            print.error("Neznamy smer zataceni %s" % smer_zataceni)

    def neindikuj(self):
        '''Prestane indikovat jakekoli zataceni.'''
        self.light_driver.blink_off()

    def zapni_svetla(self):
        '''Zapne predni potkavaci a zadni svetla.'''
        self.light_driver.front_on()
        self.light_driver.back_on()

    def zapni_predni_dalkova_svetla(self):
        '''Zapne predni dalkova svetla.'''
        self.light_driver.front_beam_on()

    def vypni_predni_dalkova_svetla(self):
        '''Zapne predni dalkova svetla. Pokud svitila potkavaci, zustanou svitit.'''
        self.light_driver.front_beam_off()

    def brzdi(self):
        '''Indikuje brzdeni zadnimi svetly.'''
        self.light_driver.brake_on()

    def nebrzdi(self):
        '''Vypne brzdeni (pokud svitila zadni svetla, zustanou svitit).'''
        self.light_driver.brake_off()

    def vypni_svetla(self):
        '''Vypne vsechna svetla.'''
        self.light_driver.off()

    def update(self):
        '''Aktualizuje stav robota, subsystemy casuji svuj provoz, nezdrzuji.'''
        self.light_driver.update()

if __name__ == "__main__":
    robot = Robot()
    etapy = [
        "svetla", "zapinam dalkova",
        "odbocuji vlevo", "uz nechci dalkova, je tam auto", "konec odbocovani",
        "odbocuji vpravo", "brzdeni, protoze mi tam vlitla srnka", "konec odbocovani",
        "konec brzdeni", "konec svetel", "konec"
    ]
    phase_length = 5000
    phase_start = time.ticks_ms()
    etapa = "startovni klid"
    while len(etapy) > 0:
        if time.ticks_diff(time.ticks_ms(), phase_start) > phase_length:
            phase_start = time.ticks_ms()
            etapa = etapy[0]
            etapy = etapy[1:]
            print("Etapa %s" % etapa)
            if etapa == "svetla":
                robot.zapni_svetla()
            elif etapa == "zapinam dalkova":
                robot.zapni_predni_dalkova_svetla()
            elif etapa == "odbocuji vlevo":
                robot.indikuj("doleva")
            elif etapa == "uz nechci dalkova, je tam auto":
                robot.vypni_predni_dalkova_svetla()
            elif etapa == "konec odbocovani":
                robot.neindikuj()
            elif etapa == "odbocuji vpravo":
                robot.indikuj("doprava")
            elif etapa == "brzdeni, protoze mi tam vlitla srnka":
                robot.brzdi()
            elif etapa == "konec brzdeni":
                robot.nebrzdi()
            elif etapa == "konec svetel":
                robot.vypni_svetla()
        robot.update()
        time.sleep(0.1)
    print("Tak zase nekdy na videnou!")
