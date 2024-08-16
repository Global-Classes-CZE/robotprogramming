
# Prvni obrazec
delka = 5
for x in range(delka):
    print("*")
print("")
print("")

# Druhy obrazec
for x in range(delka):
    line = "*"
    for y in range(x):
        line+="*"

    print(line)
