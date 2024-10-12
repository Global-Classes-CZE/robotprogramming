# Changelog/ Seznam změn

## 12.10.

### Přidán stavový automat pro test detekce křižovatek

- Kód vám umožní splnit podúkol 1 projektu pro začátečníky - tedy vyzkoušet robustnost detekce křižovatek.
- V kódu je nastaveno 10 příkazů rovně
- za každou zdetekovanou křižovatkou (na displeji se objeví R), robot popojede za ni a bude čekat na zmáčknutí tlačítka B (na obrazovce uvidíte "C" pro čekám)
- jak robot bude ve stavu C, tak ho přesuňte zpět na čáru před křivotkou a spusťe znova
- pokud vám robot dokáže detekovat křižovatku 10 krát za sebou, super, máte vyhráno
- na discord jsem dávala video, jak to provádím já
- zkuste robota dát na čáru pod různými úhly, ale vždy tak, aby jeden senzor byl na čáře

### Co musíte změnit

- V kódu musíte nastavit vaše kalibrační parametry získané úkolem 11
```
kalib_l = KalibracniFaktory(0.93, 51, 37, 17.08, 28.64)
kalib_p = KalibracniFaktory(1.39, 55, 47, 20.98, 60.16)
```

a v úkolu 13 jste si měli pohrát (pokdu jste dělali úkol pro začátečníky) s hodnotami dopředné a úhlové rychlosti pro bang-bang regulátor, tzn. nastavte v kódu také
```
dopredna = 0.1
uhlova = 0.5
```

### Třídy světel byly přesunuty do samostatného souboru

- kvůli velikosti jsem také odstranila světla z cely_projekt a přesunula je do souboru svetla.py
- robot se tedy aktuálně nerozsvící

### Interní změny

- zamergovala se kód Honzy Chaloupka pro měření stavu baterie, ale zatím se to nikde nepoužívá


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


