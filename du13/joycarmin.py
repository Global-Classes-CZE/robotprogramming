_E='CENTER'
_D=False
_C=None
_B='RIGHT'
_A='LEFT'
from utime import ticks_ms,ticks_us,ticks_diff
from machine import time_pulse_us
import math
class Controller:
	def __init__(A):0
class LIGHT_STATUS:STATUS_ON=1;STATUS_OFF=0
class LIGHT_POSITION:FRONT_LEFT_INNER='FLI';FRONT_LEFT_OUTER='FLO';FRONT_RIGHT_INNER='FRI';FRONT_RIGHT_OUTER='FRO';REAR_LEFT_INNER='RLI';REAR_LEFT_OUTER='RLO';REAR_RIGHT_INNER='RRI';REAR_RIGHT_OUTER='RRO'
class LineSensor:
	def __init__(A,key):A.key=key;A.__status=_D
	@property
	def status(self):return self.__status
	@status.setter
	def status(self,status):self.__status=status
class DIRECTION:FORWARD=0;BACKWARD=1;NONE=-1
class ObstacleSensor:0
class Robot:
	def __init__(A,wheelDiameterInMeters,axleTrackInMetres,i2cBus,neopixel,pin0,pin8,pin12,pin14,pin15):A.__wheelDiameterInMeters=wheelDiameterInMeters;A.__axleTrackInMetres=axleTrackInMetres/2;A.__i2cBus=i2cBus;A.motorController=MotorController(A.__wheelDiameterInMeters,A.__axleTrackInMetres,A.__i2cBus);A.lightController=LightController(neopixel,pin0);A.obstacleController=ObstacleController(A.__i2cBus);A.ultrasonicController=UltrasonicController(pin8,pin12);A.speedController=SpeedController(pin14,pin15);A.lineController=LineController(A.__i2cBus)
	def powerOn(A):
		print('Powering on...')
		if A.__i2cBus is not _C:A.__i2cBus.init()
		A.lightController.offAll()
	def powerOff(A):print('Powering off...');A.lightController.offAll()
class SpeedSensor:
	def __init__(A,key,pin):A.key=key;A.__pin=pin;A.__ticks=0;A.__ticksPerRotation=42;A.__data=-1;A.__clock=ticks_us();A.__period=1000000;A.__radiansPerSecond=0
	def __output(A):return A.__pin.read_digital()
	def init(A):A.__data=A.__output()
	def angleSpeed(A):
		B=ticks_us();C=ticks_diff(B,A.__clock)
		if C>A.__period:D=A.__ticks/A.__ticksPerRotation;E=D*2*math.pi;A.__radiansPerSecond=E/(C/1000000);A.__clock=B;A.__ticks=0
		return A.__radiansPerSecond
	def readData(A):
		B=A.__output()
		if B>=0:
			if B!=A.__data:A.__data=B;A.__ticks+=1
class UltrasonicSensor:
	def __init__(A):A.currentDistance=0
class Light:
	def __init__(A,key,index,color=(0,0,0)):A.key=key;A.index=index;A.color=color;A.status=LIGHT_STATUS
class LineController(Controller):
	def __init__(A,i2cBus,i2cAddress=56):super().__init__();A.i2cBus=i2cBus;A.i2cAddress=i2cAddress;A.__clock=ticks_us();A.__period=75000;A.sensors={_A:LineSensor(_A),_E:LineSensor(_E),_B:LineSensor(_B)}
	def __output(A):return A.i2cBus.read(56,1)
	def __readData(B):A=B.__output();A=int.from_bytes(A,'big');A=bin(A);B.sensors[_A].status=bool(int(A[7]));B.sensors[_E].status=bool(int(A[6]));B.sensors[_B].status=bool(int(A[5]))
	def checkStatus(A):
		B=_D,_D,_D;C=ticks_us();D=ticks_diff(C,A.__clock)
		if D>A.__period:A.__readData();A.__clock=C;B=A.sensors[_A].status,A.sensors[_E].status,A.sensors[_B].status
		return B
class Motor:
	def __init__(A,key,position):
		B=position;A.key=key;A.position=B;A.__channelForward=bytes([0]);A.__channelBackward=bytes([0]);A.__velocity=0;A.__pwm=0;A.__direction=DIRECTION.NONE;A.__paramA=0;A.__paramB=0
		if B=='left':A.__channelForward=bytes([5]);A.__channelBackward=bytes([4]);A.__paramA=15.15431538;A.__paramB=29.85786607
		if B=='right':A.__channelForward=bytes([3]);A.__channelBackward=bytes([2]);A.__paramA=15.75436641;A.__paramB=35.30530063
	@property
	def channelForward(self):return self.__channelForward
	@property
	def channelBackward(self):return self.__channelBackward
	@property
	def velocity(self):return self.__velocity
	@velocity.setter
	def velocity(self,value):self.__velocity=value
	@property
	def pwm(self):return self.__pwm
	@pwm.setter
	def pwm(self,value):self.__pwm=value
	@property
	def direction(self):return self.__direction
	@direction.setter
	def direction(self,value):self.__direction=value
	@property
	def paramA(self):return self.__paramA
	@property
	def paramB(self):return self.__paramB
class ObstacleController(Controller):
	def __init__(A,i2cBus,i2cAddress=56):super().__init__();A.i2cBus=i2cBus;A.i2cAddress=i2cAddress;A.sensors={_A:ObstacleSensor(),_B:ObstacleSensor()}
	def checkObstacle(A):0
class SpeedController(Controller):
	def __init__(A,pin14,pin15):C=pin15;B=pin14;super().__init__();A.__pin14=B;A.__pin15=C;A.sensors={_A:SpeedSensor(_A,B),_B:SpeedSensor(_B,C)};A.sensors[_A].init();A.sensors[_B].init()
	def checkSpeed(A):A.sensors[_A].readData();A.sensors[_B].readData();return A.sensors[_A].angleSpeed(),A.sensors[_B].angleSpeed()
class UltrasonicController(Controller):
	def __init__(A,pin8,pin12):super().__init__();A.__trigger=pin8;A.__echo=pin12;A.__clock=ticks_us();A.__period=1000000;A.sensor=UltrasonicSensor();A.soundSpeed=340;A.__trigger.write_digital(0);A.__echo.read_digital()
	def checkDistanceInMetres(A):
		D=ticks_us();E=ticks_diff(D,A.__clock)
		if E>A.__period:
			A.__trigger.write_digital(1);A.__trigger.write_digital(0);A.__echo.read_digital();B=time_pulse_us(A.__echo,1)
			if B<0:return B
			F=B/1000000;C=F*A.soundSpeed;C=C/2;A.sensor.currentDistance=C;A.__clock=D
		return A.sensor.currentDistance
class LightController(Controller):
	def __init__(A,neopixel,pin0):
		B=neopixel;super().__init__();A.__neopixel=_C;A.lights={LIGHT_POSITION.FRONT_LEFT_INNER:Light(LIGHT_POSITION.FRONT_LEFT_INNER,0),LIGHT_POSITION.FRONT_LEFT_OUTER:Light(LIGHT_POSITION.FRONT_LEFT_OUTER,1),LIGHT_POSITION.FRONT_RIGHT_OUTER:Light(LIGHT_POSITION.FRONT_RIGHT_OUTER,2),LIGHT_POSITION.FRONT_RIGHT_INNER:Light(LIGHT_POSITION.FRONT_RIGHT_INNER,3),LIGHT_POSITION.REAR_LEFT_OUTER:Light(LIGHT_POSITION.REAR_LEFT_OUTER,4),LIGHT_POSITION.REAR_LEFT_INNER:Light(LIGHT_POSITION.REAR_LEFT_INNER,5),LIGHT_POSITION.REAR_RIGHT_INNER:Light(LIGHT_POSITION.REAR_RIGHT_INNER,6),LIGHT_POSITION.REAR_RIGHT_OUTER:Light(LIGHT_POSITION.REAR_RIGHT_OUTER,7)};A.__indicatorPeriod=500;A.__indicatorTime=ticks_ms();A.__cycle=0
		if B is not _C:A.neopixel=B(pin0,8)
	def on(A,key,color):
		C=color;B=A.lights[key];B.status=LIGHT_STATUS.STATUS_ON;B.color=C
		if A.neopixel is not _C:A.neopixel[B.index]=C;A.neopixel.show()
	def off(A,key):
		B=A.lights[key];B.status=LIGHT_STATUS.STATUS_OFF;B.color=0,0,0
		if A.neopixel is not _C:A.neopixel[B.index]=B.color;A.neopixel.show()
	def offAll(A):
		for B in A.lights.values():A.off(B.key)
		if A.neopixel is not _C:A.neopixel.show()
	def toggleHeadlightsOn(A):B=A.lights[LIGHT_POSITION.FRONT_LEFT_INNER];C=A.lights[LIGHT_POSITION.FRONT_RIGHT_INNER];A.on(B.key,(255,255,255));A.on(C.key,(255,255,255))
	def toggleHeadlightsOff(A):B=A.lights[LIGHT_POSITION.FRONT_LEFT_INNER];C=A.lights[LIGHT_POSITION.FRONT_RIGHT_INNER];A.off(B.key);A.off(C.key)
	def toggleBrakelightsOn(A):B=A.lights[LIGHT_POSITION.REAR_LEFT_INNER];C=A.lights[LIGHT_POSITION.REAR_RIGHT_INNER];A.on(B.key,(255,0,0));A.on(C.key,(255,0,0))
	def toggleBrakelightsOff(A):B=A.lights[LIGHT_POSITION.REAR_LEFT_INNER];C=A.lights[LIGHT_POSITION.REAR_RIGHT_INNER];A.off(B.key);A.off(C.key)
	def __turnIndicatorOn(A,light1,light2,cycle=3):
		C=light2;B=light1;D=ticks_ms();E=ticks_diff(D,A.__indicatorTime)
		if E>A.__indicatorPeriod:
			if A.__cycle<cycle+3:
				if B.status==LIGHT_STATUS.STATUS_ON:A.off(B.key)
				else:A.on(B.key,(255,165,0))
				A.__indicatorTime=D
				if C.status==LIGHT_STATUS.STATUS_ON:A.off(C.key)
				else:A.on(C.key,(255,165,0))
				A.__indicatorTime=D;A.__cycle+=1
	def turnIndicatorLeftOn(A,cycle=3):A.turnIndicatorRightOff();B=A.lights[LIGHT_POSITION.FRONT_LEFT_OUTER];C=A.lights[LIGHT_POSITION.REAR_LEFT_OUTER];A.__turnIndicatorOn(B,C,cycle)
	def turnIndicatorLeftOff(A):A.off(A.lights[LIGHT_POSITION.FRONT_LEFT_OUTER].key);A.off(A.lights[LIGHT_POSITION.REAR_LEFT_OUTER].key)
	def turnIndicatorRightOn(A,cycle=3):A.turnIndicatorLeftOff();B=A.lights[LIGHT_POSITION.FRONT_RIGHT_OUTER];C=A.lights[LIGHT_POSITION.REAR_RIGHT_OUTER];A.__turnIndicatorOn(B,C,cycle)
	def turnIndicatorRightOff(A):A.off(A.lights[LIGHT_POSITION.FRONT_RIGHT_OUTER].key);A.off(A.lights[LIGHT_POSITION.REAR_RIGHT_OUTER].key)
class MotorController(Controller):
	def __init__(A,wheelDiameterInMeters,axleTrackInMeters,i2cBus,i2cAddress=112):super().__init__();A.__wheelDiameterInMeters=wheelDiameterInMeters;A.__axleTrackInMeters=axleTrackInMeters;A.__i2cBus=i2cBus;A.__i2cAddress=i2cAddress;A.__clocks={};A.__pwm0=0;A.__pwm1=0;A.__pwm2=0;A.__pwm3=0;A.__metersPerSecondInitial=0;A.__angleSpeedInitial=0;A.__sonarIsOn=_D;A.motors={_A:Motor(_A,'left'),_B:Motor(_B,'right')}
	def __normalizePWM(A,pwm,minPwm=0,maxPwm=255):return max(minPwm,min(pwm,maxPwm))
	def init(A):A.__i2cBus.write(A.__i2cAddress,bytes([0,1]));A.__i2cBus.write(A.__i2cAddress,bytes([232,170]))
	def onClock(A,callbackPeriods=_C):
		D=callbackPeriods;C=ticks_us()
		if D:
			for(B,(E,F))in enumerate(D):
				if B not in A.__clocks:A.__clocks[B]=C
				G=A.__clocks[B]
				if ticks_diff(C,G)>F:E();A.__clocks[B]=C
	def driveByPWM(A,*B):
		if not B:
			if A.motors[_A].direction==DIRECTION.FORWARD:A.__pwm0=A.motors[_A].pwm;A.__pwm1=0
			else:A.__pwm1=A.motors[_A].pwm;A.__pwm0=0
			if A.motors[_B].direction==DIRECTION.FORWARD:A.__pwm2=A.motors[_B].pwm;A.__pwm3=0
			else:A.__pwm3=A.motors[_B].pwm;A.__pwm2=0
		elif len(B)==4:A.__pwm0,A.__pwm1,A.__pwm2,A.__pwm3=B
		A.__i2cBus.write(A.__i2cAddress,A.motors[_A].channelForward+bytes([A.__normalizePWM(A.__pwm0)]));A.__i2cBus.write(A.__i2cAddress,A.motors[_A].channelBackward+bytes([A.__normalizePWM(A.__pwm1)]));A.__i2cBus.write(A.__i2cAddress,A.motors[_B].channelForward+bytes([A.__normalizePWM(A.__pwm2)]));A.__i2cBus.write(A.__i2cAddress,A.motors[_B].channelBackward+bytes([A.__normalizePWM(A.__pwm3)]))
	def driveByVelocity(A,metersPerSecond,angleSpeed):
		C=angleSpeed;B=metersPerSecond
		if A.__metersPerSecondInitial==0:A.__metersPerSecondInitial=B
		if A.__angleSpeedInitial==0:A.__angleSpeedInitial=C
		A.motors[_A].velocity=B-A.__axleTrackInMeters*C;A.motors[_A].velocity/=A.__wheelDiameterInMeters/2;A.motors[_B].velocity=B+A.__axleTrackInMeters*C;A.motors[_B].velocity/=A.__wheelDiameterInMeters/2;A.motors[_A].pwm=int(A.motors[_A].paramA*abs(A.motors[_A].velocity)+A.motors[_A].paramB);A.motors[_B].pwm=int(A.motors[_B].paramA*abs(A.motors[_B].velocity)+A.motors[_B].paramB)
		if A.motors[_A].velocity==0:A.motors[_A].pwm=0
		if A.motors[_B].velocity==0:A.motors[_B].pwm=0
		if A.motors[_A].velocity>0:A.motors[_A].direction=DIRECTION.FORWARD
		else:A.motors[_A].direction=DIRECTION.BACKWARD
		if A.motors[_B].velocity>0:A.motors[_B].direction=DIRECTION.FORWARD
		else:A.motors[_B].direction=DIRECTION.BACKWARD
		A.driveByPWM()
	def driveWithRegulator(A,speed,P=28):
		B,C=speed
		if round(float(B),1)!=.0 and round(float(C),1)!=.0:
			if A.motors[_A].velocity<0:B*=-1
			if A.motors[_B].velocity<0:C*=-1
			F=A.motors[_A].velocity-B;G=A.motors[_B].velocity-C;D=int(P*F);E=int(P*G)
			if A.motors[_A].direction==DIRECTION.BACKWARD:D*=-1
			if A.motors[_B].direction==DIRECTION.BACKWARD:E*=-1
			A.motors[_A].pwm+=D;A.motors[_B].pwm+=E;A.driveByPWM()
	def driveWithSonar(A,distanceInMetres,metersFromObstacle=.2,P=.5):
		C=distanceInMetres
		if C>0:
			D=-metersFromObstacle;E=-C;F=D-E;B=P*F
			if B>A.__metersPerSecondInitial:B=A.__metersPerSecondInitial
			A.driveByVelocity(B,A.__angleSpeedInitial)
	def driveWithLineDetection(A,status,angleSpeed):
		C=angleSpeed;B=status;print(B);D,F,E=B
		if D:A.driveByVelocity(A.__metersPerSecondInitial,C)
		if E:A.driveByVelocity(A.__metersPerSecondInitial,-C)
		if not E and not D:A.driveByVelocity(A.__metersPerSecondInitial,0)