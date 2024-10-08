from neopixel import NeoPixel
from microbit import i2c, pin0, pin8, pin12, pin14, pin15, button_a, button_b, sleep
from utime import ticks_ms, ticks_us, ticks_diff
from machine import time_pulse_us

_U = 0x70
_AL = 40

class _F:
	_X = 0
	_L = 1
	_AD = 2
	_H = 11
	_A = 12

class _J:
	_Z = 0
	_AC = 1
	_E = 2

class _AO:
	_AM = 1
	_D = 2
	_AE = 3
	_V = 4

class _AP:
	def __init__(_IB):
		_IB._EP = 0.0
		_IB._CV = 0.0

class _C:
	def __init__(_IB, _GH, _GG, _GF, a, b):
		_IB._GE = _GH
		_IB._GD = _GG
		_IB._GC = _GF
		_IB.a = a
		_IB.b = b

class _AF:
	def __init__(_IB, p, _JE):
		_IB._BI = p
		_IB._CJ = _JE
		_IB._BK = ticks_ms()

	def _FR(_IB, _IY):
		_EA = ticks_diff(_IY, _IB._BK)
		return  _EA >= _IB._CJ

	def _EV(_IB, _IY, _FL, _FK):
		_IB._BK = _IY
		_EM = _FL - _FK
		_DM = _IB._BI * _EM
		return _DM

class _AI:
	_AB = 0x40
	_AA = 0x20
	_S = 0x10
	_R = 0x08
	_Q = 0x04

	def __init__(_IB):
		_IB._CJ = 50
		_IB._HO()

	def _HO(_IB, _IY=0):
		_IB._AY = i2c.read(0x38, 1)[0]
		if _IY == 0:
			_IB._BN = ticks_ms()
		else:
			_IB._BN = _IY

	def _EX(_IB, _IC):
		return (_IB._AY & _IC) == 0

	def _FR(_IB, _IY):
		_EA = ticks_diff(_IY, _IB._BN)
		return  _EA >= _IB._CJ

	def _JI(_IB):
		_IY = ticks_ms()
		if _IB._FR(_IY):
			_IB._HO(_IY)

class _K:
	_X = 0
	_AH = 1
	_M = 2
	def __init__(_IB):
		_IB._HV()

	def _HV(_IB):
		_IB._ID(_IB._X)

	def _ID(_IB, _JL):
		_IB._JL = _JL
		_IB._IQ = ticks_ms()

	def _FP(_IB, _HB):
		return _IB._JL != _HB

	def _JC(_IB):
		return ticks_diff(ticks_ms(), _IB._IQ) > 400

	def _DL(_IB):
		_IB._ID(_IB._AH if _IB._JL == _IB._M else _IB._M)

	def _JI(_IB):
		if _IB._JL != _IB._X:
			if _IB._JC():
				_IB._DL()
		else:
			_IB._ID(_IB._M)

class _O:
	_DQ = (0, 0, 0)
	_DR = (100, 35, 0)
	_DU = (60, 60, 60)
	_DV = (255, 255, 255)
	_DS = (60, 0, 0)
	_DT = (255, 0, 0)

	def __init__(_IB):
		_IB._BV = NeoPixel(pin0, 8)
		_IB._CP = 0

	def _IF(_IB, _FV, _DP):
		_IB._BV[_FV] = _DP

	def _IG(_IB, _FU, _DP):
		for _FV in _FU:
			_IB._IF(_FV, _DP)

	def _FR(_IB):
		return ticks_diff(ticks_ms(), _IB._CP) > 100

	def write(_IB):
		_IB._BV.write()
		_IB._CP = ticks_ms()

class _P:
	_FF = (1, 2, 4, 7)
	_FG = (1, 4)
	_FH = (2, 7)
	_FA = (0, 3)
	_CZ = (5, 6)
	_FM = (0, 3, 5, 6)
	_HX = (5,)
	def __init__(_IB, _JM):
		_IB._BO = _O()
		_IB._BD = _K()
		_IB._CM = _JM
		_IB._II(_J._AC)
		_IB._IH()
		_IB._IJ()
		_IB._BG = False
		_IB._AS = 0
		_IB._JN = False

	def _II(_IB, _JL):
		_IB._BQ = _JL

	def _IH(_IB):
		if _IB._CM._CV > 0.0:
			_IB._BC = _F._L
		elif _IB._CM._CV < 0.0:
			_IB._BC = _F._AD
		else:
			_IB._BC = _F._X

	def _IJ(_IB):
		_IB._BH = _IB._CM._EP < 0.0

	def _IE(_IB):
		if False:
			_IB._BG = True
			_IB._AS = ticks_ms()

	def _FO(_IB):
		if _IB._BG:
			_EA = ticks_diff(ticks_ms(), _IB._AS)
			if _EA < 1_000:
				return True
			_IB._BG = False
		return False

	def _JI(_IB):
		_IB._IH()
		_IB._IJ()
		_IB._IE()
		_DA = _IB._BD._JL
		if _IB._BC != _F._X or _IB._JN:
			_IB._BD._JI()
		else:
			_IB._BD._HV()
		if _IB._BD._FP(_DA) or _IB._BO._FR():
			if _IB._BD._JL == _K._M:
				if _IB._AZ == _F._L or _IB._JN:
					_IB._BO._IG(_IB._FG, _O._DR)
				if _IB._AZ == _F._AD or _IB._JN:
					_IB._BO._IG(_IB._FH, _O._DR)
			else:
				_IB._BO._IG(_IB._FF, _O._DQ)
			_EZ = _O._DQ
			_CY = _O._DQ
			if _IB._BQ == _J._AC:
				_EZ = _O._DU
				_CY = _O._DS
			if _IB._BQ == _J._E:
				_EZ = _O._DV
				_CY = _O._DS
			if _IB._FO():
				_CY = _O._DT
			_IB._BO._IG(_IB._FA, _EZ)
			_IB._BO._IG(_IB._CZ, _CY)
			if _IB._BH:
				_IB._BO._IG(_IB._HX, _O._DU)
			_IB._BO.write()

class _AK:
	_N = 50
	def __init__(_IB):
		_IB._BE = -1
		_IB._CK = [0] * _IB._N
		_IB._CI = [0] * _IB._N
		_IB._AW = -1
		_IB._BM = -1
		_IB._FQ = True

	
	def _ET(_IB, _IY: int):
		_GQ = int(_IY / 100_000)
		if _GQ == _IB._BM:
			return -1
		else:
			_IB._BM = _GQ
			return (_IB._BE + 1) % _IB._N

	def _GU(_IB, _GN, _IY, _IU):
		if _IB._AW < _IB._N:
			_IB._AW += 1
			if _IB._AW > 2:
				_IB._FQ = (_IB._CI[_IB._BE]-_IU) == 0
		_IB._CK[_GN] = _IY
		_IB._CI[_GN] = _IU
		_IB._BE = _GN

	def _JI(_IB, _IU):
		_IY = ticks_us()
		_GN = _IB._ET(_IY)
		if _GN >= 0:
			_IB._GU(_GN, _IY, _IU)

	def _DF(_IB, _DW=5, _GX=0):
		if _DW < 2:
			_DW = 10
		if _DW+_GX >= _IB._AW:
			_DW = _IB._AW - _GX - 1
		if _DW < 2:
			return 0
		_IN = _IB._AT(_DW, _GX)
		_IO = _IB._AT(_DW, _GX+1)
		return  (_IN + _IO) / 2

	def _AT(_IB, _DW, _GX):
		_EL = (_IB._BE - _GX) % _IB._N
		_IR = (_EL - _DW + 1) % _IB._N
		_EC = _IB._CK[_EL] - _IB._CK[_IR]
		_EB = _IB._CI[_EL] - _IB._CI[_IR]
		return 1_000_000 * _EB / _EC

class _G:
	def __init__(_IB, _HJ):
		if _HJ == _F._L:
			_IB._BX = pin14
		else:
			_IB._BX = pin15
		_IB._CH = _AK()
		_IB._BW = _IB._HP()
		_IB._IU = 0
		_IB._ED = _F._H

	def _FQ(_IB):
		return _IB._CH._FQ

	def _HP(_IB):
		return _IB._BX.read_digital()

	def _GT(_IB):
		if _IB._ED == _F._H:
			_IB._IU += 1
			return 0
		if _IB._ED == _F._A:
			_IB._IU -= 1
			return 0
		return -1

	def _JI(_IB, _ED):
		_IB._ED = _ED
		_GR = _IB._HP()
		if (_GR != _IB._BW):
			_IB._GT()
			_IB._BW = _GR
		_IB._CH._JI(_IB._IU)

	def _EY(_IB, _JH, _DW=5, _GX=0):
		_IM = _IB._CH._DF(_DW, _GX)
		if _JH == _AO._AM:
			return _IM
		_IM /= _AL
		if _JH == _AO._D:
			return _IM
		_IM *= (2 * 3.1416)
		if _JH == _AO._AE:
			return _IM
		return 0

class _AQ:
	def __init__(_IB, _HJ, _HL, _DH):
		_IB._BY = _HJ
		_IB._BB = _G(_HJ)
		_IB._CD = _AF(6, 500)
		_IB._AU = _DH
		_IB._HL = _HL
		_IB._IM = 0.0
		_IB._ED = _F._H
		if _HJ == _F._AD:
			_IB._CA = 2
			_IB._CB = 3
		elif _HJ == _F._L:
			_IB._CA = 4
			_IB._CB = 5
		else:
			_IB._CA = 0
			_IB._CB = 0
		i2c.write(_U, bytes([0x00, 0x01]))
		i2c.write(_U, bytes([0xE8, 0xAA]))

	def _EK(_IB):
		_IB._IM = 0.0
		_IB._JT(_IB._CA, _IB._CB, 0)

	def _FQ(_IB):
		return _IB._BB._FQ()

	def _ES(_IB):
		return _IB._AU._GE

	def _JT(_IB, _GW, _GY, _HK):
		i2c.write(_U, bytes([_GW, 0]))
		i2c.write(_U, bytes([_GY, _HK]))
		_IB._BZ = _HK

	def _EW(_IB, _IM):
		if _IM==0.0:
			return 0
		return _IB._AU.a * _IM + _IB._AU.b

	def _HY(_IB, _IM):
		_IB._IM = _IM
		if _IB._IM >= 0:
			_IB._ED = _F._H
		else:
			_IB._ED = _F._A
		_HK = _IB._EW(abs(_IM))
		_IB._CE(_HK)

	def _DN(_IB, _HK):
		if _IB._IM != 0.0:
			if (_IB._FQ()):
				_GB = _IB._AU._GD
			else:
				_GB = _IB._AU._GC
			if _HK < _GB:
				_HK = _GB
		return _HK

	def _CE(_IB, _HK):
		_HA = _HK
		_HK = int(_HK)
		_HK = _IB._DN(_HK)
		if _HK < 0:
			return
		if _HK > 255:
			return
		if _IB._CB>0 and _IB._CA>0:
			if _IB._ED == _F._H:
				return _IB._JT(_IB._CA, _IB._CB, _HK)
			if _IB._ED == _F._A:
				return _IB._JT(_IB._CB, _IB._CA, _HK)
			return
		return

	def _AV(_IB, _DM):
		_GO = 0
		if _IB._ED == _F._H:
			_GO = _IB._BZ + _DM
		if _IB._ED == _F._A:
			_GO = _IB._BZ - _DM
		if _GO > 255:
			_GO = 255
		if _GO < 0:
			_GO  = 0
		return _IB._CE(_GO)

	def _EY(_IB, _JH, _DW=5, _GX=0):
		if _JH == _AO._V:
			return _IB._HL * _IB._BB._EY(_AO._AE, _DW, _GX)
		return _IB._BB._EY(_JH, _DW, _GX)

	def _HS(_IB):
		_IY = ticks_ms()
		if _IB._CD._FR(_IY):
			_FZ = _IB._BB._EY(_AO._AE)
			_DM = _IB._CD._EV(_IY, _IB._IM, _FZ)
			_IB._AV(_DM)

	def _JI(_IB):
		_IB._BB._JI(_IB._ED)
		_IB._HS()

class _W:
	def __init__(_IB, _JQ, _JP, _JM, _DI, _DJ):
		_IB._AX = _JQ / 2
		_IB._CC = _JP / 2
		_IB._JM = _JM
		_IB._CN = _AQ(_F._L, _IB._CC, _DI)
		_IB._CO = _AQ(_F._AD, _IB._CC, _DJ)

	def _EK(_IB):
		try:
			_IB._GS(0, 0)
		except _B as e:
			_IB._CN._EK()
			_IB._CO._EK()
			raise e

	def _ES(_IB):
		_GI = _IB._CN._ES()
		_GJ = _IB._CO._ES()
		return max(_GI, _GJ)

	def _GS(_IB, _EP, _CV):
		_IB._JM._EP = _EP
		_IB._JM._CV = _CV
		_IB._CN._HY(_IB._JM._EP - _IB._AX * _IB._JM._CV)
		_IB._CO._HY(_IB._JM._EP + _IB._AX * _IB._JM._CV)

	def _DE(_IB, _IM):
		return _IM / _IB._CC

	def _JI(_IB):
		_IB._CN._JI()
		_IB._CO._JI()

class _AJ:
	_T = 10

	def __init__(_IB, _JD):
		_IB._CL = pin8
		_IB._CL.write_digital(0)
		_IB._BA = pin12
		_IB._BA.read_digital()
		_IB._BJ = 0
		_IB._BL = -3
		_IB._CJ = _JD
		_IB._FT = -1

	def _DG(_IB, _IY):
		_IB._BJ = _IY
		_IB._CL.write_digital(1)
		_IB._CL.write_digital(0)
		_IM = 340
		_JB = time_pulse_us(_IB._BA, 1, 5_000)
		if _JB < 0:
			return _JB
		_JA = _JB / 1_000_000
		_EE = _JA * _IM / 2
		return _EE

	def _FR(_IB, _IY):
		_EA = ticks_diff(_IY, _IB._BJ)
		return  _EA >= _IB._CJ

	def _JI(_IB):
		_IY = ticks_ms()
		if _IB._FR(_IY):
			_IB._BL = _IB._DG(_IY)
			if _IB._BL > 0:
				_IB._FT = _IB._BL
			if _IB._BL == -1:
				_IB._FT = _IB._T

class _AG:
	def __init__(_IB, _FW, _HZ):
		_JM = _AP()
		i2c.init(freq=400_000)
		_IB._CF = _AI()
		_IB._CG = _AJ(300)
		_IB._CD = _AF(15, 1_000)
		_IB._BP = _P(_JM)
		_IB._GK = _W(0.15, 0.067, _JM, _FW, _HZ)
		_IB._GK._GS(0, 0)
		_IB._BS = _IB._GK._DE(0.3)
		_IB._BT = _IB._GK._ES()

	def _EK(_IB):
		_IB._GK._EK()

	def _IS(_IB):
		return 0.00898 * _HH.read_analog()

	def _EU(_IB):
		return _IB._CG._FT

	def _IT(_IB):
		if _IB._CF._EX(_AI._AA) or _IB._CF._EX(_AI._AB):
			_IB._GK._GS(0, 0)

	def _IP(_IB, _IM):
		if _IM >= 0:
			_IK = 1
		else:
			_IK = -1
		_CS = abs(_IM)
		if _CS > _IB._BS:
			_CS = _IB._BS
		elif _CS < _IB._BT:
			_CS = _IB._BT
		return _IK * _CS

	def _CT(_IB, _HU, _EE):
		_EF = abs(_EE-_HU)
		return _EF <= 0.03

	def _HT(_IB):
		_IY = ticks_ms()
		if _IB._CD._FR(_IY):
			_HU = 0.2
			_EE = _IB._EU()
			if _IB._CT(_HU, _EE):
				_GP = 0
			else:
				_GP = _IB._CD._EV(_IY, -_HU, -_EE)
				_GP = _IB._IP(_GP)
			_IB._GK._GS(_GP, 0)

	def _JI(_IB):
		_IB._GK._JI()
		_IB._CF._JI()
		_IB._CG._JI()
		_IB._BP._JI()
		_IB._IT()
		_IB._HT()

if __name__ == "__main__":
	_FW  = _C(2.8, 110, 75, 11.692, 28.643)
	_HZ = _C(2.8, 110, 75, 12.259, 30.332)
	_IA = _AG(_FW, _HZ)
	try:
		while not button_a.was_pressed():
			_IA._JI()
			sleep(1)
		_IA._GK._GS(0, 0)
	except _B as e:
		_IA._EK()
		raise e
