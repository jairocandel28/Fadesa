# Plan de Pruebas

**Proyecto:** Sistema de Predicción (FADESA)  
**Fecha:** [09/12/2025]    


**Funcionalidades Clave a Probar:**
1.  Carga y visualización de datos (CSV/Excel).
2.  Selección de variables (Entrada/Salida).
3.  Preprocesado y limpieza de datos (Manejo de nulos).
4.  Parametrización y creación del modelo (Train/Test split).
5.  Guardado y Carga de modelos persistentes (.joblib).
6.  Realización de predicciones (Interfaz de inferencia).


## 1. Casos de Prueba

### A. Carga y Visualización de Datos

| ID | Escenario | Pasos / Acción | Resultado Esperado | Estado |
|:---|:---|:---|:---|:---:|
| **CP-01** | Carga de archivo válido | 1. Clic en "ABRIR ARCHIVO".<br>2. Seleccionar CSV/Excel correcto. | La ruta se actualiza, el mensaje de bienvenida desaparece y se muestra la tabla con datos. | [ CORRECTO ] |
| **CP-02** | Cancelar carga | 1. Clic en "ABRIR ARCHIVO".<br>2. Cerrar ventana o cancelar. | La aplicación no se cierra. Mantiene el estado anterior ("Ningún archivo..."). | [ CORRECTO ] |
| **CP-03** | Archivo vacío | 1. Intentar cargar un CSV vacío (0kb). | Muestra alerta: *"El archivo no contiene datos o no fue posible cargarlos"*. | [ CORRECTO ] |

### B. Selección y Preprocesado

| ID | Escenario | Pasos / Acción | Resultado Esperado | Estado |
|:---|:---|:---|:---|:---:|
| **CP-04** | Confirmación vacía | 1. Cargar datos.<br>2. No seleccionar nada.<br>3. Clic "CONFIRMAR SELECCIÓN". | Muestra advertencia: *"Selecciona al menos una columna de ENTRADA y una de SALIDA"*. | [ CORRECTO ] |
| **CP-05** | Detección de Nulos | 1. Seleccionar columnas con huecos.<br>2. Clic "CONFIRMAR SELECCIÓN". | Muestra alerta con conteo de nulos y despliega el panel "Manejo de valores inexistentes". | [ CORRECTO ] |
| **CP-06** | Imputación Constante (Error) | 1. Elegir "Rellenar con constante".<br>2. Dejar campo vacío o poner texto.<br>3. Clic "Aplicar". | Muestra advertencia: *"Debes ingresar un valor constante"* o *"Debes ingresar un número"*. | [ CORRECTO ] |
| **CP-07** | Imputación Correcta | 1. Elegir "Media" o "Eliminar".<br>2. Clic "Aplicar". | Mensaje *"Preprocesado aplicado correctamente"* y despliega panel de Separación. | [ CORRECTO ] |

### C. Creación del Modelo

| ID | Escenario | Pasos / Acción | Resultado Esperado | Estado |
|:---|:---|:---|:---|:---:|
| **CP-08** | Parámetros Inválidos | 1. Poner `1.5` o `-0.1` en "% Entrenamiento".<br>2. Clic "Crear modelo". | Muestra advertencia: *"El porcentaje debe estar entre 0 y 1"*. | [ ERROR ] |
| **CP-09** | Parámetros Texto | 1. Poner letras en Semilla o Porcentaje.<br>2. Clic "Crear modelo". | Muestra mensaje de error controlado (no cierra la app). | [ CORRECTO ] |
| **CP-10** | Creación Exitosa | 1. Datos correctos (0.8, 42).<br>2. Clic "Crear modelo". | Muestra ventana con métricas (R², ECM), fórmula y gráficos. | [ CORRECTO ] |

### D. Persistencia y Predicción

| ID | Escenario | Pasos / Acción | Resultado Esperado | Estado |
|:---|:---|:---|:---|:---:|
| **CP-11** | Carga de Modelo Inválido | 1. Clic "CARGAR MODELO".<br>2. Elegir un `.txt` o imagen. | Muestra error: *"No se pudo cargar el archivo seleccionado"* o error de joblib. | [ CORRECTO ] |
| **CP-12** | Carga Exitosa | 1. Clic "CARGAR MODELO".<br>2. Elegir `.joblib` válido. | Limpia la pantalla, muestra info del modelo y genera panel de predicción. | [ CORRECTO ] |
| **CP-13** | Predicción (Input Error) | 1. En panel predicción, escribir texto en input numérico.<br>2. Clic "Predecir". | Muestra error indicando que se requieren valores numéricos. | [ CORRECTO ] |
| **CP-14** | Predicción Correcta | 1. Ingresar valores numéricos.<br>2. Clic "Predecir". | Muestra el resultado de la predicción calculado por el modelo. | [ CORRECTO ] |


## 2. Registro de Errores y Correcciones


| Fecha | ID Test | Descripción del Fallo | Corrección Aplicada | Retest |
|:---|:---|:---|:---|:---:|
| [09/12] | [Ej: CP-08] | [Ej: La app creaba el modelo sin hacer la comprobación de los datos de separación] | [Ej: Se reestableció el orden lógico al ejecutar y mostrar el panel de separación] | CORRECTO |



## 3. Conclusión

**Resumen de Ejecución:**
- [ 14 ] Total de casos ejecutados.
- [ 14 ] Total de casos exitosos.
- [ 0 ] Errores críticos pendientes (Blockers).



