from time import sleep

from I2cAdapter import I2cAdapter


class Motor:
    def __init__(self, address, addressForward, addressBack, d, a, b):
        self.__address = address
        self.__addressForward = addressForward
        self.__addressBack = addressBack
        self.__d = d
        self.__a = a
        self.__b = b
        self.__pwm = 0  # referencni PWM
        self.__v = 0  # referencni dopredna rychlost

    def goV(self, v):
        if v == 0:
            self.__goPWM(0)
            return
        # print('goV v', v)
        self.__v = v
        omega = v / self.__d  # dopredna na uhlovou rychlost
        # print('goV omega', omega)
        coef = 1 if omega > 0 else -1

        pwm = int(self.__a * omega + self.__b * coef)  # uhlova rychlost na PWM

        pwm_original = pwm
        pwm_max = 75
        pwm_min = 40

        pwm = pwm_max if pwm_min < pwm <= pwm_max else pwm
        pwm = 0 if -pwm_min < pwm <= pwm_min else pwm
        pwm = -pwm_max if -pwm_max < pwm <= -pwm_min else pwm

        self.__pwm = max(min(pwm, 200), -200)
        # print('v', v, 'omega', omega, 'a', self.__a, 'b', self.__b, 'pwm', self.__pwm, 'pwmOrig', pwm_original)
        # print('goV pwm', self.__pwm)
        self.__goPWM(self.__pwm)

    def stop(self):
        self.__goPWM(0)

    def regulate(self, v):
        # v: Aktualni rychlost podle ktere chceme regulovat
        if self.__v == 0:
            self.__goPWM(0)
            return
        error = self.__v - v
        P = 40
        pwm = int(self.__pwm + (P * error))
        pwm = max(min(pwm, 230), -230)
        # print('error=' + str(error), 'AZ=' + str(P * error), 'pwm=' + str(pwm), '__v=' + str(self.__v), 'v=' + str(v))
        self.__goPWM(pwm)

    def goPWM(self, pwm):
        self.__pwm = pwm
        self.__goPWM(pwm)

    def __goPWM(self, pwm):
        print('__goPWM', pwm)
        I2cAdapter.write(self.__address, self.__addressForward + bytes([pwm if pwm > 0 else 0]))
        I2cAdapter.write(self.__address, self.__addressBack + bytes([pwm * -1 if pwm < 0 else 0]))
