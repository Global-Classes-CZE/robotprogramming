from microbit import i2c, sleep
from microbit import pin2, pin14, pin15, pin0
from microbit import display, button_a

from utime import ticks_us, ticks_diff

class K:
    NEDEFINOVANO = "nedefinovano"

    LEVY = "levy"
    PRAVY = "pravy"

    DOPREDU = "dopredu"
    DOZADU = "dozadu"

    ENKODER = "enkoder"
    PR_ENKODER = PRAVY + "_" + ENKODER
    LV_ENKODER = LEVY + "_" + ENKODER

    IR = "IR"
    PR_IR = PRAVY + "_" + IR
    LV_IR = LEVY + "_" + IR

    SENZOR_CARY = "senzor_cary"
    PR_S_CARY = PRAVY + "_" + SENZOR_CARY
    LV_S_CARY = LEVY + "_" + SENZOR_CARY
    PROS_S_CARY = "prostredni_" + SENZOR_CARY

    PI = 3.14159265359

    CARA = "cara"
    KRIZOVATKA = "krizovatka"
    ZTRACEN = "ztracen"
    ZATOC = "zatoc"

    ROVNE = "rovne"
    VPRAVO = "vpravo"
    VLEVO = "vlevo"
    VZAD = "vzad"

    VSE = "vse"


class Senzory:

    def __init__(self, nova_verze=True):
        self.nova_verze = nova_verze
        i2c.init(400000)

    def precti_senzory(self):
        surova_data_byte = i2c.read(0x38, 1)
        bitove_pole = self.byte_na_bity(surova_data_byte)

        senzoricka_data = {}

        if not self.nova_verze:
            senzoricka_data[K.LV_ENKODER] = bitove_pole[9]
            senzoricka_data[K.PR_ENKODER] = bitove_pole[8]

        senzoricka_data[K.LV_S_CARY] = bool(int(bitove_pole[7]))
        senzoricka_data[K.PROS_S_CARY] = bool(int(bitove_pole[6]))
        senzoricka_data[K.PR_S_CARY] = bool(int(bitove_pole[5]))
        senzoricka_data[K.LV_IR] = bool(int(bitove_pole[4]))
        senzoricka_data[K.PR_IR] = bool(int(bitove_pole[3]))

        return senzoricka_data

    def byte_na_bity(self, data_bytes):

        data_int = int.from_bytes(data_bytes, "big")
        bit_pole_string = bin(data_int)

        return bit_pole_string

class Enkoder:

    def __init__(self, jmeno, perioda_rychlosti=1, nova_verze=True):
        self.jmeno = jmeno
        self.perioda_rychlosti = perioda_rychlosti*1000000  # na us

        self.nova_verze = nova_verze
        self.tiky = 0
        self.posledni_hodnota = -1
        self.tiky_na_otocku = 40
        self.nova_verze = nova_verze
        self.inicializovano = False
        self.cas_posledni_rychlosti = ticks_us()
        self.radiany_za_sekundu = 0

        if not self.nova_verze:
            self.senzory = Senzory(False)

    def inicializuj(self):
        self.posledni_hodnota = self.aktualni_hodnota()
        self.inicializovano = True

    def aktualni_hodnota(self):
        if self.nova_verze:
            if self.jmeno == K.PR_ENKODER:
                return pin15.read_digital()
            elif self.jmeno == K.LV_ENKODER:
                return pin14.read_digital()
            else:
                return -2
        else:
            senzoricka_data = self.senzory.precti_senzory()

            if self.jmeno == K.LV_ENKODER or self.jmeno == K.PR_ENKODER:
                return int(senzoricka_data[self.jmeno])
            else:
                return -2

    def aktualizuj_se(self):
        if self.posledni_hodnota == -1:
            return -1

        aktualni_enkoder = self.aktualni_hodnota()
        if aktualni_enkoder >= 0:
            if self.posledni_hodnota != aktualni_enkoder:
                self.posledni_hodnota = aktualni_enkoder
                self.tiky += 1
        else:
            return aktualni_enkoder
        return 0

    def us_na_s(self, cas):
        return cas/1000000

    def vypocti_rychlost(self):
        cas_ted = ticks_us()
        interval_us = ticks_diff(cas_ted, self.cas_posledni_rychlosti)
        if interval_us >= self.perioda_rychlosti:
            interval_s = self.us_na_s(interval_us)
            otacky = self.tiky/self.tiky_na_otocku
            radiany = otacky * 2 * K.PI
            self.radiany_za_sekundu = radiany / interval_s
            self.tiky = 0
            self.cas_posledni_rychlosti = cas_ted

        return self.radiany_za_sekundu

class Motor:
    def __init__(self, jmeno, prumer_kola, nova_verze=True):
        if jmeno == K.LEVY:
            self.kanal_dopredu = b"\x05"
            self.kanal_dozadu = b"\x04"
        elif jmeno == K.PRAVY:
            self.kanal_dopredu = b"\x03"
            self.kanal_dozadu = b"\x02"
        else:
            raise AttributeError("spatne jmeno motoru, musi byt \"levy\" a nebo \"pravy\", zadane jmeno je" + str(jmeno))

        self.jmeno = jmeno
        self.prumer_kola = prumer_kola
        self.enkoder = Enkoder(jmeno + "_enkoder", 1, nova_verze)
        self.smer = K.NEDEFINOVANO
        self.inicializovano = False
        self.rychlost_byla_zadana = False
        self.min_pwm = 0
        self.perioda_regulace = 1000000 #v microsekundach
        self.cas_posledni_regulace = 0
        self.aktualni_rychlost = 0

        self.rych_rozjezd = -1
        self.pwm_rozjezd = -1
        self.a = 0
        self.b = 0

    def inicializuj(self):
        i2c.write(0x70, b"\x00\x01")
        i2c.write(0x70, b"\xE8\xAA")

        self.enkoder.inicializuj()
        self.inicializovano = True
        self.cas_posledni_regulace = ticks_us()

    def jed_doprednou_rychlosti(self, v: float):
        if not self.inicializovano:
            return -1

        self.pozadovana_uhlova_r_kola = self.dopredna_na_uhlovou(v)
        self.rychlost_byla_zadana = True

        prvni_PWM = self.uhlova_na_PWM(abs(self.pozadovana_uhlova_r_kola))
        if self.pozadovana_uhlova_r_kola > 0:
            self.smer = K.DOPREDU
        elif self.pozadovana_uhlova_r_kola < 0:
            self.smer = K.DOZADU
        else:
            self.smer == K.NEDEFINOVANO

        return self.jed_PWM(prvni_PWM)

    def dopredna_na_uhlovou(self, v: float):
        return v/(self.prumer_kola/2)

    def uhlova_na_PWM(self, uhlova):

        if uhlova == 0: #TODO uvazuj, zda tohle by nemelo byt pod min rozjezd rychlost
            return 0
        else:
            if self.zkalibrovano:
                return int(self.a*uhlova + self.b)
            else:
                return -1

    def jed_PWM(self, PWM):
        je_vse_ok = -2
        omezeni = False

        if PWM > 255:
            PWM = 255
            omezeni = True

        if PWM < 0:
            PWM = 0
            omezeni = True

        if self.smer == K.DOPREDU:
            je_vse_ok  = self.nastav_PWM_kanaly(self.kanal_dopredu, self.kanal_dozadu, PWM)
        elif self.smer == K.DOZADU:
            je_vse_ok  = self.nastav_PWM_kanaly(self.kanal_dozadu, self.kanal_dopredu, PWM)
        elif self.smer == K.NEDEFINOVANO:
            if PWM == 0:
                je_vse_ok = self.nastav_PWM_kanaly(self.kanal_dozadu, self.kanal_dopredu, PWM)
            else:
                je_vse_ok = -1
        else:
            je_vse_ok = -3

        if je_vse_ok == 0 and omezeni:
            return -4
        else:
            return je_vse_ok

    def nastav_PWM_kanaly(self, kanal_on, kanal_off, PWM):
        # TODO zkontroluj, ze motor byl inicializovan
        i2c.write(0x70, kanal_off + bytes([0]))
        i2c.write(0x70, kanal_on + bytes([PWM]))
        self.PWM = PWM
        return 0

    def aktualizuj_se(self, s_regulaci):
        self.enkoder.aktualizuj_se()
        if s_regulaci:
            cas_ted = ticks_us()
            cas_rozdil = ticks_diff(cas_ted, self.cas_posledni_regulace)
            navratova_hodnota = 0
            if cas_rozdil > self.perioda_regulace:
                navratova_hodnota = self.reguluj_otacky()
                self.cas_posledni_regulace = cas_ted

            return navratova_hodnota
        else:
            return 0

    def reguluj_otacky(self):

        if not self.inicializovano:
            return -1

        if not self.rychlost_byla_zadana:
            return -2

        P = 6

        self.aktualni_rychlost = self.enkoder.vypocti_rychlost()

        if self.pozadovana_uhlova_r_kola < 0:
            self.aktualni_rychlost *= -1

        error = self.pozadovana_uhlova_r_kola - self.aktualni_rychlost
        akcni_zasah = P*error
        return self.zmen_PWM_o(akcni_zasah)

    def zmen_PWM_o(self, akcni_zasah):

        akcni_zasah = int(akcni_zasah)

        if self.smer == K.DOZADU:
            akcni_zasah *= -1

        nove_PWM = self.PWM + akcni_zasah

        return self.jed_PWM(nove_PWM)

    def kalibruj(self, rych, pwm):

        if self.pwm_rozjezd == -1:
            return -1

        roz_rych = rych- self.rych_rozjezd
        roz_pwm = pwm - self.pwm_rozjezd

        if roz_rych == 0 or roz_pwm ==0:
            return -2

        self.a = roz_pwm/roz_rych
        self.b = pwm - self.a*rych
        self.zkalibrovano = True
        return 0

    def min_rychlost(self, pwm):

        rych = self.enkoder.vypocti_rychlost()

        if rych > 0:
            if self.pwm_rozjezd == -1:
                self.pwm_rozjezd= pwm
                self.rych_rozjezd = rych
        elif rych == 0:
            if self.pwm_rozjezd != -1:
                self.pwm_rozjezd = -1
                self.rych_rozjezd = 0

        return rych

class Robot:

    def __init__(self, rozchod_kol: float, prumer_kola: float, nova_verze=True):
        """
        Konstruktor tridy
        """
        self.d = rozchod_kol/2
        self.prumer_kola = prumer_kola

        self.levy_motor = Motor(K.LEVY, prumer_kola, nova_verze)
        self.pravy_motor = Motor(K.PRAVY, prumer_kola, nova_verze)
        self.inicializovano = False
        self.cas_minule_reg = ticks_us()
        self.perioda_regulace = 1000000
        self.senzory = Senzory(nova_verze)

        self.perioda_cary_us = 75000

        self.posledni_cas_popojeti = 0

    def inicializuj(self):
        i2c.init(400000)
        self.levy_motor.inicializuj()
        self.pravy_motor.inicializuj()
        self.inicializovano = True
        self.posledni_cas_reg_cary_us = ticks_us()
        self.jed(0,0)
        return True

    def kalibruj(self, od, do, ink):
        if not self.inicializovano:
            return -1

        if od >=do:
            return -2

        if 0 <= od <=255:
            if 0 <= do <= 255:
                pass
            else:
                return -2
        else:
            return -2

        if ink <= 0:
            return -2

        self.levy_motor.smer = K.DOPREDU
        self.pravy_motor.smer = K.DOZADU

        pwm = od

        l_rych = -1
        p_rych = -1
        button_a.was_pressed() # cteni zpusobi vynulovani stavu

        while pwm <= do:
            if button_a.was_pressed():
                break

            error = self.levy_motor.jed_PWM(pwm)
            if error != 0:
                break
            error = self.pravy_motor.jed_PWM(pwm)
            if error != 0:
                break

            cas_minule = ticks_us()
            cas_ted = cas_minule

            while ticks_diff(cas_ted, cas_minule) < 1000000:
                cas_ted = ticks_us()
                error = self.levy_motor.aktualizuj_se(False)
                if error < 0:
                    break
                error = self.pravy_motor.aktualizuj_se(False)
                if error < 0:
                    break
                sleep(5)

            if error < 0:
                break

            l_rych = self.levy_motor.min_rychlost(pwm)
            p_rych = self.pravy_motor.min_rychlost(pwm)

            if pwm != do:
                if l_rych > 0 and p_rych > 0:
                    pwm = do
                    continue

            pwm += ink

        error = self.levy_motor.jed_PWM(0)
        error = self.pravy_motor.jed_PWM(0)

        error = self.levy_motor.kalibruj(l_rych, pwm-ink)
        if error == -1:
            return -3
        elif error == -2:
            return -4

        error = self.pravy_motor.kalibruj(p_rych, pwm-ink)
        if error == -1:
            return -5
        elif error == -2:
            return -6

        return 0


    # pokrocily ukol 7
    def jed(self, dopredna_rychlost: float, uhlova_rychlost: float):

        if not self.inicializovano:
            return -1

        dopr_rychlost_leve = dopredna_rychlost - self.d * uhlova_rychlost
        dopr_rychlost_prave = dopredna_rychlost + self.d * uhlova_rychlost

        self.levy_motor.jed_doprednou_rychlosti(dopr_rychlost_leve)
        self.pravy_motor.jed_doprednou_rychlosti(dopr_rychlost_prave)

        return 0

    def zmer_a_vrat_napajeci_napeti(self):
        return 0.00898 * pin2.read_analog()

    def aktualni_rychlost(self):
        levy_r = self.levy_motor.aktualni_rychlost * self.prumer_kola/2
        pravy_r = self.pravy_motor.aktualni_rychlost * self.prumer_kola/2


        omega = (pravy_r - levy_r)/ (2 * self.d)
        v = levy_r + self.d * omega
        return v, omega

    def aktualizuj_se(self, s_motor_regulaci):
        self.levy_motor.aktualizuj_se(s_motor_regulaci)
        self.pravy_motor.aktualizuj_se(s_motor_regulaci)

    def vycti_senzory_cary(self):

        senzoricka_data = self.senzory.precti_senzory()

        if senzoricka_data[K.LV_S_CARY] and senzoricka_data[K.PR_S_CARY]:
            return K.KRIZOVATKA
        if senzoricka_data[K.LV_S_CARY] and senzoricka_data[K.PROS_S_CARY]:
            return K.KRIZOVATKA
        if senzoricka_data[K.PROS_S_CARY] and senzoricka_data[K.PR_S_CARY]:
            return K.KRIZOVATKA

        elif not senzoricka_data[K.LV_S_CARY] and not senzoricka_data[K.PR_S_CARY] and not senzoricka_data[K.PROS_S_CARY]:
            return K.ZTRACEN
        else:
            return K.CARA

    def jed_po_care(self, dopredna, uhlova):
        cas_ted = ticks_us()

        if ticks_diff(cas_ted, self.posledni_cas_reg_cary_us) > self.perioda_cary_us:
            self.posledni_cas_reg_cary_us = cas_ted
            data = self.senzory.precti_senzory()

            if data[K.LV_S_CARY]:
                self.jed(dopredna, uhlova)

            if data[K.PR_S_CARY]:
                self.jed(dopredna, -uhlova)

            if not data[K.LV_S_CARY] and not data[K.PR_S_CARY]:
                self.jed(dopredna, 0)

    def popojed(self, dopredna, perioda_us):

        if self.posledni_cas_popojeti == 0:
            self.posledni_cas_popojeti = ticks_us()

        cas_ted = ticks_us()
        if ticks_diff(cas_ted, self.posledni_cas_popojeti) > perioda_us:
            self.posledni_cas_popojeti = 0
            self.jed(0,0)
            return True
        else:
            self.jed(dopredna, 0)
            return False

    def zatoc(self, dopredna, uhlova, senzor):

        senzoricka_data = self.senzory.precti_senzory()
        hodnota_senzoru = senzoricka_data[senzor]

        if hodnota_senzoru:
            self.jed(0,0)
            return True
        else:
            self.jed(dopredna, uhlova)
            return False

class Obrazovka:
    def pis(text):
        display.show(text[0])
        print(text)
