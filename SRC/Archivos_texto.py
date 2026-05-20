# Abre (o crea) un archivo en modo escritura
fp = open(".\\SRC\\Ejercicio-1.txt", "r", encoding="utf-8")
datos_1 = fp.readlines()
print("Primera lectura:", datos_1)

datos_2 = fp.read()
print("Segunda lectura:", datos_2)
fp.close()