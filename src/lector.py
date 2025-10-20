import pandas as pd


def leer_archivo(ruta):
    try:
        if ruta.endswith(".csv"):
            datos = pd.read_csv(ruta)
        elif ruta.endswith((".xlsx", ".xls")):
            datos = pd.read_excel(ruta)
        else:
            print("Formato no soportado. El archivo debe ser .csv o .xlsx/.xls.")
            return

        print("Datos cargados exitosamente:")
        print(datos.head(10))  # Muestra las primeras 10 filas del dataset
        return datos # En caso de querer devolver todos los datos

    except Exception as e:
        print(f"Error al leer el archivo: {e}")


if __name__ == "__main__":

    
    archivo = input("Introduce la ruta completa del archivo que quieres analizar: ")
    resultado = leer_archivo(archivo)


