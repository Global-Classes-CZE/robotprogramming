for i in range(1, 6):
    print("*")

i = 1
while i <= 5:
    print('*')
    i += 1

for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()
    
for i in range(1, 6):
    print('*' * i)