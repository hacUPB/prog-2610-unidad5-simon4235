promedio_edad = 0
suma_edad = 0
contador = 0
import csv

with open(".\\SRC\\personas.csv", "r", encoding = "utf-8") as csvfile:
    lector = csv.reader(csvfile, delimiter = ",")
    encabezados = next(lector)
    for fila in lector:
        nombre = fila[0]
        apellido = fila[1]
        edad = int(fila[2])
        suma_edad += edad
        contador += 1

        print(f"La persona {contador}, se llama {nombre} {apellido} y tiene {edad} años.")

promedio_edad = suma_edad / contador

print(f"la edad promedio entre todas las personas es {promedio_edad} años.")
    