import pandas as pd
from sklearn.model_selection import train_test_split


def separacion_entrenamiento_test (datos: pd.DataFrame, columnas_entrada, columna_salida, porcentaje_test, random_state):
    """
        Divide los datos en conjuntos de entrenamiento y prueba de forma aleatoria pero reproducible.

        Parámetros:
            datos: DataFrame de pandas con los datos completos.
            columnas_entrada: lista con los nombres de las columnas de entrada.
            columna_salida: string con el nombre de la columna de salida.
            porcentaje_test: proporción de datos para el conjunto de prueba (por defecto 0.2 → 20%).
            random_state: semilla aleatoria fija para asegurar reproducibilidad (por defecto 42).

        Devuelve:
            X_train, X_test, y_train, y_test
    """
    X = datos[columnas_entrada]
    y = datos[columna_salida]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = porcentaje_test, random_state = random_state
    )

    return X_train, X_test, y_train, y_test