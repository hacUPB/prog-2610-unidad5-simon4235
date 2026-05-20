archivo = open(".\\SRC\\texto_aleatorio.txt", "r", encoding="utf-8")

lectura = archivo.readlines()
print("Primera lectura:", lectura)

for linea in lectura:
    print(linea[0])
