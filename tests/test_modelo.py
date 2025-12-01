import pytest
import pandas as pd
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modelo import separacion_entrenamiento_test, crear_modelo_lineal, guardar_modelo

@pytest.fixture
def datos_test():
    """Crea un DataFrame pequeño para usar en las pruebas."""
    np.random.seed(42)
    df = pd.DataFrame({
        'entrada1': np.random.rand(20) * 10,  
        'entrada2': np.random.rand(20) * 100,    
        'salida': np.random.rand(20) * 10      
    })
    return df

def test_separacion_datos(datos_test):
    """
    Verifica que la función divide los datos en el porcentaje correcto (20% test).
    """
    X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
        datos_test, 
        columnas_entrada=['entrada1'], 
        columna_salida='salida', 
        porcentaje_test=0.2
    )
    
    assert len(X_test) == 4
    assert len(X_train) == 16
    assert len(y_test) == 4
    assert len(X_train) + len(X_test) == 20

def test_crear_modelo_lineal(datos_test):
    """
    Verifica que el modelo se entrena, genera la fórmula y calcula R2.
    """
    entradas = ['entrada1']
    X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
        datos_test, entradas, 'salida'
    )
    
    resultados = crear_modelo_lineal(X_train, X_test, y_train, y_test, entradas)
    
    assert 'modelo' in resultados
    assert 'r2_train' in resultados
    assert 'formula' in resultados
    
    assert isinstance(resultados['formula'], str)
    assert "entrada1" in resultados['formula'] 
    
    assert isinstance(resultados['r2_test'], float)
    assert resultados['r2_test'] <= 1.0

@patch('src.modelo.messagebox.showinfo')
@patch('src.modelo.filedialog.asksaveasfilename')
def test_guardar_modelo(mock_filedialog, mock_msgbox, datos_test, tmp_path):
    """
    Prueba que 'guardar_modelo' funciona y crea el archivo.
    """
    archivo_destino = tmp_path / "modelo_test.joblib"
    mock_filedialog.return_value = str(archivo_destino)
    
    X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
        datos_test, ['entrada1'], 'salida'
    )
    res = crear_modelo_lineal(X_train, X_test, y_train, y_test, ['entrada1'])
    
    metricas = {'r2': res['r2_test']}
    
    guardar_modelo(res['modelo'], ['entrada1'], 'salida', metricas, "Descripción de prueba")
    
    assert archivo_destino.exists(), "El archivo .joblib no se creó"
    mock_msgbox.assert_called_once()
    
    datos_cargados = joblib.load(archivo_destino)
    assert datos_cargados['descripcion'] == "Descripción de prueba"
    assert datos_cargados['columna_salida'] == 'salida'

def test_carga_y_prediccion(datos_test, tmp_path):
    """
    Verifica el ciclo completo: Entrenar -> Guardar -> Cargar -> Predecir.
    """
    X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
        datos_test, ['entrada1'], 'salida'
    )
    res = crear_modelo_lineal(X_train, X_test, y_train, y_test, ['entrada1'])
    modelo_original = res['modelo']
    
    archivo_modelo = tmp_path / "modelo_final_test.joblib"
    joblib.dump(modelo_original, archivo_modelo)

    modelo_cargado = joblib.load(archivo_modelo)


    dato_nuevo = pd.DataFrame({'entrada1': [5.0]})
    prediccion = modelo_cargado.predict(dato_nuevo)

    assert modelo_cargado is not None
    assert isinstance(prediccion[0], float)


