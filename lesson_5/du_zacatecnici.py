if __name__ == "__main__":
    for i in range(5):
        print("*")

    print()

    # prvni mozne reseni pres vnorene cykly
    for i in range(1, 6):  # poradi radku [1, 2, 3, 4, 5] a zaroven pocet hvezdicek!
        for j in range(i):  # [0], [0,1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]
            # prikazem end nastavuji, co se ma stat nakonci vypsaneho retezce
            # v tom to pripade nic - chceme dalsi hvezdicky vypsat za
            print("*", end='')
        print() # nova radka

    print()
    # druhe mozne reseni trojuhelnika
    for i in range(1, 6):
        print(i*"*")

    print()
    # treti mozne reseni trojuhelnika
    retezec = "*"
    for i in range(5):
        print(retezec)
        retezec += "*"
