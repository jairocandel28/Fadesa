import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def separacion_entrenamiento_test(datos: pd.DataFrame, columnas_entrada, columna_salida, porcentaje_test=0.2, random_state=42):
    """Divide los datos en conjuntos de entrenamiento y prueba de forma aleatoria pero reproducible. 
    Parámetros: 
    datos: DataFrame de pandas con los datos completos. 
    columnas_entrada: lista con los nombres de las columnas de entrada. 
    columna_salida: string con el nombre de la columna de salida. porcentaje_test: proporción de datos para el conjunto de prueba (por defecto 0.2 → 20%). 
    random_state: semilla aleatoria fija para asegurar reproducibilidad (por defecto 42). Devuelve: X_train, X_test, y_train, y_test """

    X = datos[columnas_entrada]
    y = datos[columna_salida]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=porcentaje_test, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def crear_modelo_lineal(X_train, X_test, y_train, y_test, columnas_entrada):
    """Crea, ajusta y evalúa un modelo de regresión lineal."""
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Predicciones
    y_train_pred = modelo.predict(X_train)
    y_test_pred = modelo.predict(X_test)

    # Métricas
    r2_train = r2_score(y_train, y_train_pred)
    r2_test = r2_score(y_test, y_test_pred)
    ecm_train = mean_squared_error(y_train, y_train_pred)
    ecm_test = mean_squared_error(y_test, y_test_pred)

    # Fórmula del modelo
    formula = " + ".join([f"{coef:.3f}·{col}" for coef, col in zip(modelo.coef_, columnas_entrada)])
    formula = f"{formula} + {modelo.intercept_:.3f}"

    resultados = {
        "modelo": modelo,
        "formula": formula,
        "r2_train": r2_train,
        "r2_test": r2_test,
        "ecm_train": ecm_train,
        "ecm_test": ecm_test,
        "y_train_pred": y_train_pred,
        "y_test_pred": y_test_pred,
    }

    return resultados 