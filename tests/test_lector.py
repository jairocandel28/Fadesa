import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.lector import leer_archivo



def test_leer_csv_valido(tmp_path):
    """
    Crea un archivo CSV temporal y verifica que se carga correctamente.
    Usa 'tmp_path' de pytest para no ensuciar tu disco duro.
    """
    carpeta = tmp_path / "datos"
    carpeta.mkdir()
    archivo_csv = carpeta / "test.csv"
    archivo_csv.write_text("col1,col2\n10,20\n30,40", encoding="utf-8")
    
    df = leer_archivo(str(archivo_csv))
    
    assert df is not None, "El dataframe no debería ser None"
    assert not df.empty, "El dataframe no debería estar vacío"
    assert list(df.columns) == ["col1", "col2"], "Las columnas no coinciden"
    assert len(df) == 2, "Debería haber 2 filas de datos"

def test_extension_invalida():
    """
    Verifica que la función maneje archivos con extensiones incorrectas (.txt).
    """
    resultado = leer_archivo("archivo_falso.txt")
    
  
    assert resultado is None or resultado.empty if hasattr(resultado, 'empty') else True

def test_archivo_no_existe():
    """
    Verifica que no explote el programa si el archivo no existe.
    """
    resultado = leer_archivo("ruta/que/no/existe.csv")
    assert resultado is None