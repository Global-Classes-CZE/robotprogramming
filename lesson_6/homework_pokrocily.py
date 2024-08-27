from WheelDriver import WheelDriver
import time

# dopredna_rychlost v je float
# rotace je uhlova rychlost omega a take float
# Poznámka: samotná velikost čísel ještě nebude dávat smysl,
# tzn dopredna_rychlost NENÍ v m/s, ale v nějakých nedefinovaných jednotkách…
# tento problém odstraníme příští hodinu

def jed(wheel_driver, dopredna_rychlost, rotace, doba_ms):
    d = 0.09  # polovina roztece kol, tj. polovina z 18cm
    v_l = dopredna_rychlost - d*rotace  # prednaska 7, slide 50: v_l = v - d*ω
    v_r = dopredna_rychlost + d*rotace  # prednaska 7, slide 50: v_r = v + d*ω
    print ("jedeme v_l: %f, v_r: %f" % (v_l, v_r))
    wheel_driver.move_by_time(v_l, v_r, doba_ms)

if __name__ == "__main__":
    # napiste kod, aby robot jel rychlosti "135" 1s vpred
    # pak zastavil na 1s
    # pak rotoval okolo sve osy 1s s rychlosti "1350"  po dobu 1s
    # a pak zastavil a kod se vypnul
    wheel_driver = WheelDriver()
    etapy = [
        "dopredu", "rotace", "konec"
    ]
    phase_length = 2000  # 1 sekunda pro cinnost, 1 sekunda pro stop stav
    phase_start = time.ticks_ms()
    etapa = "startovni klid"
    while len(etapy) > 0:
        if time.ticks_diff(time.ticks_ms(), phase_start) > phase_length:
            phase_start = time.ticks_ms()
            etapa = etapy[0]
            etapy = etapy[1:]
            print("Etapa %s" % etapa)
            if etapa == "dopredu":
                jed(wheel_driver, dopredna_rychlost=135, rotace=0, doba_ms=1000)
            elif etapa == "rotace":
                jed(wheel_driver, dopredna_rychlost=135, rotace=1350, doba_ms=1000)
        wheel_driver.update()
        time.sleep(0.01)
    print("Finished")
