from Encoder import Encoder
from Motor import Motor
from I2cAdapter import I2cAdapter
from Period import Period


class MoveController:
    __ADDRESS = 0x70

    def __init__(self, wheelSpan, wheelDiameter, encoder: Encoder):
        self.__period = Period(1000)
        self.__encoder = encoder
        self.__d = wheelSpan / 2
        self.__motorL = Motor(MoveController.__ADDRESS, b'\x05', b'\x04', self.__d, 28.404601, 31.92611167)
        self.__motorR = Motor(MoveController.__ADDRESS, b'\x03', b'\x02', self.__d, 27.74501239, 32.95067256)
        self.__init()

        self.__PWM = 0

    def __init(self):
        I2cAdapter.write(self.__ADDRESS, b'\x00\x01')
        I2cAdapter.write(self.__ADDRESS, b'\xE8\xAA')
        self.__motorL.stop()
        self.__motorR.stop()

    # def zmen_o(self, pwm):
    #     pwm_nove = int(self.__PWM + pwm)
    #     pwm_nove = min(pwm_nove, 255)
    #     pwm_nove = max(pwm_nove, 0)
    #     self.goPWM(pwm_nove, 0)

    def goPWM(self, pwm, rotation=0):
        pwm_l = pwm - self.__d * rotation
        pwm_r = pwm + self.__d * rotation

        self.__motorL.goPWM(int(pwm_l))
        self.__motorR.goPWM(int(pwm_r))

    def goV(self, v, rotation=0):
        # jed rychlosti meter / second

        v_l = v - self.__d * rotation
        v_r = v + self.__d * rotation

        self.__motorL.goV(v_l)
        self.__motorR.goV(v_r)

        # if v == 0:
        #     self.goPWM(v, rotation)
        #     return
        #
        # # dopredna rychlost na uhlovou rychlost
        # omega = v / self.__d  # omega = uhlova rychlost (rad / sec)
        #
        # print('speed=' + str(v), 'omega=' + str(omega))
        # # uhlova rychlost na PWM
        # a = 25.45852411
        # b = 41.13058938
        # pwm = max(int(a * omega + b), 200)
        # print('speed=' + str(v), 'omega=' + str(omega), 'pwm=' + str(pwm))
        # self.__PWM = pwm
        # self.goPWM(pwm, rotation)

    # def goPWM(self, pwm, rotation=0):
    #     v_l = pwm - self.__d * rotation
    #     v_r = pwm + self.__d * rotation
    #     if not -255 <= v_l <= 255:
    #         return -1
    #     if not -255 <= v_r <= 255:
    #         return -1
    #     self.__motorL.go(int(v_l))
    #     self.__motorR.go(int(v_r))

    __calibrate = False
    __cPeriod = None
    __cSpeed = None
    __cSpeeds = None
    __cPWM = None

    def calibrate(self):
        self.__calibrate = True
        self.__cPeriod = Period(1600)
        self.__cSpeed = 70
        self.__cPWM = [0, 0]
        self.__cSpeeds = [0, 0]

    def tick(self):
        if self.__calibrate and self.__cPeriod.isTime():
            speed = self.__encoder.wheel().getSpeed()
            for i in [0, 1]:
                if speed[i] > 0:
                    self.__cSpeeds[i] = speed[i]
                    self.__cPWM[i] = self.__cSpeed
            self.__cSpeed += 2
            self.__motorL.goPWM(self.__cSpeed if self.__cPWM[0] == 0 else 0)
            self.__motorR.goPWM(self.__cSpeed if self.__cPWM[1] == 0 else 0)
            print(self.__cSpeed, self.__cSpeeds, self.__cPWM)

        # pass
        # P regulace
        # if self.__period.isTime():
        #     speed = self.__encoder.wheel().getSpeed()
        #     self.__motorL.regulate(speed[0])
        #     self.__motorR.regulate(speed[1])
