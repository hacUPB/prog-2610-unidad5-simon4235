from pathlib import Path
import matplotlib.pyplot as plt
import csv

def explorar_directorio(ruta):

    try:
       archivos = list(ruta.iterdir())

    except FileNotFoundError:
        print("Ruta no encontrada")
        ruta = Path(input("Ingrese una ruta válida: "))

    else:
        print("Archivos encontrados:")
        for archivo in archivos:
            print(f"- {archivo.name}")

    return ruta

def procesar_bitacoras(nombre_archivo, ruta, lista_errores, conectores):

    total_lineas = 0
    total_palabras = 0
    caracteres_con_espacios = 0
    caracteres_sin_espacios = 0
    errores = 0
    palabras_repetidas = {}
    longitudes_lineas = []
    
    ruta_txt = ruta / f"{nombre_archivo}.txt"

    try:
        with open(ruta_txt, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

    except FileNotFoundError:
        print("Archivo no encontrado en la carpeta\n1. Ingresar un nuevo nombre de archivo\n2. Ingresar una nueva ruta")
        opcion = input("Ingrese la opción que desea seleccionar: ")
        if opcion == "1":
            nombre_archivo = input("Ingrese un nombre válido del archivo de bitácora a procesar: ")
        elif opcion == "2":
            ruta = Path(input("Ingrese una nueva ruta válida: "))

    else:
        for linea in lineas:
            
            total_lineas += 1
            linea = linea.replace("\n", "")
            total_palabras += len(linea.split())
            caracteres_con_espacios += len(linea)
            caracteres_sin_espacios += len(linea.replace(" ", ""))
            if 0 < len(linea) <= 100:
                longitudes_lineas.append(len(linea))

            for error in lista_errores:
                if error in linea:
                    errores += 1

            palabras = linea.lower().split()
            for palabra in palabras:
                palabra = palabra.strip(".,;:!?()[]{}\"'")
                if palabra not in conectores and palabra:
                    if palabra in palabras_repetidas:
                        palabras_repetidas[palabra] += 1
                    else:
                        palabras_repetidas[palabra] = 1

        lista_palabras = list(palabras_repetidas.items())

        for i in range(len(lista_palabras)):
            for j in range(len(lista_palabras) - 1):
                if lista_palabras[j][1] < lista_palabras[j + 1][1]:
                    temp = lista_palabras[j]
                    lista_palabras[j] = lista_palabras[j + 1]
                    lista_palabras[j + 1] = temp

        print("Total líneas:", total_lineas)
        print("Total palabras:", total_palabras)
        print("Caracteres con espacios:", caracteres_con_espacios)
        print("Caracteres sin espacios:", caracteres_sin_espacios)
        print("Errores encontrados:", errores)
        print("Top 5 palabras más repetidas:")
        
        for i in range(5):
            print(lista_palabras[i][0], ":", lista_palabras[i][1])

        palabras = []
        frecuencias = []
        for i in range(10):
            palabras.append(lista_palabras[i][0])
            frecuencias.append(lista_palabras[i][1])

        plt.barh(palabras, frecuencias)
        plt.title("Top 10 palabras más frecuentes")
        plt.xlabel("Frecuencia")
        plt.ylabel("Palabras")
        plt.savefig("./SRC/reto/graficas/grafica_palabras.png")
        plt.show()

        plt.hist(longitudes_lineas, bins=10)
        plt.title("Distribución de longitud de líneas")
        plt.xlabel("Cantidad de caracteres por línea")
        plt.ylabel("Número de líneas")
        plt.savefig("./SRC/reto/graficas/grafica_lineas.png")
        plt.show()
    
    return nombre_archivo, ruta

def analizar_dataset(nombre_archivo, ruta):
    
    ruta_csv = ruta / f"{nombre_archivo}.csv"

    try:
        with open(ruta_csv, "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector)
            datos = list(lector)

        with open(ruta_csv, "r", encoding="utf-8") as archivo:
            lector_dict = csv.DictReader(archivo)
            datos_dict = list(lector_dict)

    except FileNotFoundError:
        print("Archivo no encontrado en la carpeta\n1. Ingresar un nuevo nombre de archivo\n2. Ingresar una nueva ruta")
        opcion = input("Ingrese la opción que desea seleccionar: ")
        if opcion == "1":
            nombre_archivo = input("Ingrese un nombre válido del archivo de bitácora a procesar: ")
        elif opcion == "2":
            ruta = Path(input("Ingrese una nueva ruta válida: "))

    else:
        while True:
            print("1. Vista previa de datos")
            print("2. Cálculo de Estadísticas Descriptivas")
            print("3. Gráfico evolución temporal")
            print("4. Gráfico comparación categórica")
            print("5. Gráfico correlación de variables")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                print("Encabezados: ")
                print(encabezados)

                print(f"Primeras 10 filas: ")
                for i in range(10):
                    print(datos[i])
                
                print("Últimas 5 filas:")
                for i in range(len(datos) - 5, len(datos)):
                    print(datos[i])

            elif opcion == "2":
                print("Columnas disponibles:")
                for encabezado in encabezados:
                    print("-", encabezado)
                columna = input("Ingrese el nombre de la columna numérica que desea analizar: ")
                valores = []
                for fila in datos_dict:
                    if fila[columna] != "":
                        try:
                            valores.append(float(fila[columna]))
                        except ValueError:
                            pass

                promedio = sum(valores) / len(valores)

                valores.sort()
                if len(valores) % 2 == 0:
                    mediana = (valores[len(valores)//2 - 1] + valores[len(valores)//2]) / 2
                else:
                    mediana = valores[len(valores)//2]

                print("Total registros válidos:", len(valores))
                print("Promedio:", promedio)
                print("Mediana:", mediana)
                print("Máximo:", max(valores))
                print("Mínimo:", min(valores))
        
            elif opcion == "3":
                print("Columnas disponibles:")
                for encabezado in encabezados:
                    print("-", encabezado)
                columna_x = input("Ingrese columna para eje X: ")
                
                print("Columnas disponibles:")
                for encabezado in encabezados:
                    print("-", encabezado)
                columna_y = input("Ingrese columna numérica para eje Y: ")

                x = []
                y = []

                for fila in datos_dict:
                    if fila[columna_x] != "" and fila[columna_y] != "":
                        try:
                            valor_y = float(fila[columna_y])
                            x.append(fila[columna_x])
                            y.append(valor_y)
                        except ValueError:
                            pass

                pares = list(zip(x, y))
                pares.sort()

                x = []
                y = []

                for par in pares:
                    x.append(par[0])
                    y.append(par[1])

                plt.plot(x, y)
                plt.title("Evolución temporal")
                plt.xlabel(columna_x)
                plt.ylabel(columna_y)
                plt.xticks(rotation=90)
                plt.tight_layout()
                plt.savefig("./SRC/reto/graficas/grafica_temporal.png")
                plt.show()

            elif opcion == "4":
                print("Columnas disponibles:")
                for encabezado in encabezados:
                    print("-", encabezado)

                columna = input("Ingrese el nombre de la columna categórica: ")

                categorias = {}

                for fila in datos_dict:
                    valor = fila[columna]

                    if valor != "":
                        if valor in categorias:
                            categorias[valor] += 1
                        else:
                            categorias[valor] = 1

                etiquetas = []
                cantidades = []

                for categoria in categorias:
                    etiquetas.append(categoria)
                    cantidades.append(categorias[categoria])

                plt.pie(cantidades, labels=etiquetas, autopct="%1.1f%%")
                plt.title(f"Distribución de {columna}")
                plt.savefig("./SRC/reto/graficas/grafica_categorica.png")
                plt.show()
            
            elif opcion == "5":
                print("Columnas disponibles:")
                for encabezado in encabezados:
                    print("-", encabezado)

                columna_x = input("Ingrese la primera columna numérica: ")
                columna_y = input("Ingrese la segunda columna numérica: ")

                x = []
                y = []

                for fila in datos_dict:
                    if fila[columna_x] != "" and fila[columna_y] != "":
                        try:
                            valor_x = float(fila[columna_x])
                            valor_y = float(fila[columna_y])

                            x.append(valor_x)
                            y.append(valor_y)
                        except ValueError:
                            pass

                plt.scatter(x, y)
                plt.title("Correlación de variables")
                plt.xlabel(columna_x)
                plt.ylabel(columna_y)
                plt.savefig("./SRC/reto/graficas/grafica_correlacion.png")
                plt.show()

            elif opcion == "6":
                break   

    return nombre_archivo, ruta
        


def main():
    ruta = Path("./SRC/reto/directorio")
    lista_errores = ["ERROR", "404"]
    conectores = [
        "de", "del", "la", "las", "el", "los",
        "y", "e", "o", "u", "ni",
        "en", "a", "al", "por", "para", "con", "sin", "pero",
        "sobre", "entre", "hasta", "desde", "hacia",
        "un", "una", "unos", "unas",
        "que", "como", "cuando", "donde", "porque",
        "es", "son", "fue", "eran", "ser", "estar",
        "se", "su", "sus", "lo", "le", "les",
        "mi", "mis", "tu", "tus", "ya",
        "no", "si", "sí",
        "me", "te", "nos", "os",
        "este", "esta", "estos", "estas",
        "ese", "esa", "esos", "esas",
        "aquel", "aquella", "aquellos", "aquellas",
    ]
    
    while True:
        print("¡Bienvenido al explorador CLI para el análisis y visualización de archivos reales!\n1. explorar directorio\n2. Procesar bitácoras\n3. Analizar dataset de datos abiertos\n4. Salir")
        try:
            opcion = int(input("Ingrese el número de la opción que desea seleccionar: "))
        except ValueError:
            print("Error: debe ingresar un número del 1 al 4")
            continue

        if opcion == 1:
            ruta = explorar_directorio(ruta)
        elif opcion == 2:
            nombre_archivo = input("Ingrese el nombre del archivo de bitácora a procesar (sin .txt): ")
            nombre_archivo, ruta = procesar_bitacoras(nombre_archivo, ruta, lista_errores, conectores)
        elif opcion == 3:
            nombre_archivo = input("Ingrese el nombre del archivo csv (sin .csv): ")
            nombre_archivo, ruta = analizar_dataset(nombre_archivo, ruta)
        elif opcion == 4:
            break
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 4.")

if __name__ == "__main__":
    main()