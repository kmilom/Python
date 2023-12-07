#Ejercicios sencillos con python
"""
print("Hello World")
"""

"""
celsius = float(input("Ingrese la cantidad de grados celsius: "))
farenheit = ((9/5)*celsius) + 32
print(celsius, " grados en Farenheit: ", farenheit)
"""

"""
n = int(input(("Ingrese un nú8mero entero: ")))
if n % 2 == 0:
    print(n, "es un número par.")
else:
    print(n, "es un número impar.")
"""

"""
i = 0
while i < 5:
    j = 0
    while j <= i:
        print("*", end="")
        j += 1
    print("")
    i += 1

for i in range(5):
    j = 0
    while j <= i:
        print("*", end="")
        j += 1
    print()
"""
"""
top = 10
for i in range(top):
    for j in range(top * 2):
        if j == top or (j >= top - i and j <= top + i):
            print("*", end="")
        else:
            print(" ", end="")
    print()
for i in range(top, -1, -1):
    for j in range(top * 2 + 1):
        if j == top or (j >= top - i and j <= top + i):
            print("*", end="")
        else:
            print(" ", end="")
    print()
"""