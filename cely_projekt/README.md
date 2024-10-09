# Changelog/ Seznam změn

## 9.10.

### Změna interface (důležité pro vás)
- návrat třídy KalibracniFaktory
- změna konstruktoru třídy Robot, aby se do něj vkládáli KalibracniFaktory pro leve a prave kolo. 

Příklad použití:
```
kalib_l = KalibracniFaktory(0.93, 51, 37, 17.08, 28.64)
kalib_p = KalibracniFaktory(1.39, 55, 47, 20.98, 60.16)
robot = Robot(0.15, 0.067, kalib_l,  kalib_p)
``` 

kde KalibracniFaktory jsou v pořadí:

`def __init__(self, min_rychlost, min_pwm_rozjezd, min_pwm_dojezd, a, b)`

### Interní změny
- ošetřené přetečení PWM při první velké hodnotě
- oprava chyby v třídě Senzory, kde se hodnoty pro IR nárázníky špatně přetypovávali


