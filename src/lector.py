import pandas as pd
import sqlite3


def leer_archivo(ruta):
    try:
        if ruta.endswith(".csv"):
            datos = pd.read_csv(ruta)
        elif ruta.endswith((".xlsx", ".xls")):
            datos = pd.read_excel(ruta)
        elif ruta.endswith(".db"):
            conexion = sqlite3.connect(ruta)
            cursor = conexion.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = [t[0] for t in cursor.fetchall()]
            tabla = tablas[0]
            datos = pd.read_sql_query(f"SELECT * FROM {tabla}", conexion)   
            conexion.close()        
        else:
            print("Formato no soportado. El archivo debe ser .csv, .xlsx/.xls. o .db")
            return datos

        print("Datos cargados exitosamente:")
        print(datos.head(10))  # Muestra las primeras 10 filas del dataset
        return datos # En caso de querer devolver todos los datos

    except Exception as e:
        print(f"Error al leer el archivo: {e}")




if __name__ == "__main__":

    
    archivo = input("Introduce la ruta completa del archivo que quieres analizar: ")
    resultado = leer_archivo(archivo)


        


