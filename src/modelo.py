import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm


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


ruta_archivo = r"C:\Users\jairo\Desktop\Fadesa\Fadesa-3\docs\housing.csv"
datos = pd.read_csv(ruta_archivo)

columnas_entrada = ["longitude", "latitude", "housing_median_age", "total_rooms",
    "total_bedrooms", "population", "households", "median_income"]

columna_salida = "median_house_value"

datos[columnas_entrada] = datos[columnas_entrada].fillna(datos[columnas_entrada].median())

X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
    datos, columnas_entrada, columna_salida, porcentaje_test=0.2, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

ECM = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Error Cuadrático Medio:", ECM)
print("R²:", r2)
print("Coeficientes:", dict(zip(columnas_entrada, modelo.coef_)))

#Probamos librería statsmodels
X = datos[columnas_entrada]
y = datos[columna_salida]

#rellenar con mediana(para el ejemplo)
X = X.fillna(X.median())
y = y.fillna(y.median())

X = sm.add_constant(X)  
modelo = sm.OLS(y, X)  
resultado = modelo.fit()
print(resultado.summary())



