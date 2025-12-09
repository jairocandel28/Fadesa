# Fadesa

Repositorio Proyecto ES

Un cliente contacta con nuestro equipo de desarrollo y nos dice:
“Quiero contrataros para hacer una aplicación que me permita crear y visualizar modelos de
regresión lineal simple [y múltiple] a partir de datos almacenados en archivos csv, excel, y bases
de datos (SQLite), y hacer predicciones con ellos. También quiero que me permita guardar los
modelos, cargarlos, y hacer predicciones. La aplicación debe tener una interfaz gráfica que me
permita hacer todo lo anterior.”
El objetivo de este repositorio es llevar a cabo esta tarea.


Instrucciones de instalación y uso:

Para la correcta instalación de este programa el usuario necesita descargar todos los archivos presentes
en este repositorio y mantener dichos archivos guardados en la misma carpeta.
Una vez disponga del material ha de abrir la terminal de su dispositivo y llegar hasta la carpeta src
donde está el archvio main.py. Luego tendrá que escribir en la terminal: python main.py, y se ejecutará el
progrma.

Para un buen uso del programa la propia interfaz gráfica le irá guiando en como utilizar las funciones
disponibles paso a paso.
Primero podrá abrir un archivo de tipo .csv, .xlsx, .xls o .db; o cargar un modelo creado previamente en
este programa.
Luego se le dará la opción de vovler al menú principal en el caso de haber cargado un modelo o de seleccionar
las filas de entrada y la fila de salida que se utilzarán en la creación del modelo. Al confirmar la selección
se comprobará la aparición de números nulos en dichas columnas y se le dará al usuario la opción de modificar
esos valores entre varias opciones.
Posteriormente, se le permitirá al usuario la elección entre el porcentaje de entrenamiento (el resto será
utilizado para test) y una semilla para crear el modelo lienal.
A continuación, se le mostrarán los resultados del modelo, una gráfica de los valores reales contra la predicción
y se le permitirá la opción de escribir una descripción para guardar el modelo. También tendrá la posibilidad
de ingresar valores para las columnas de entrada y realizar una predicción para dichos valores.
Finalmente, si el usuario ha decidido previamente elegir solo una columna de entrada aparecerá un gráfico del
modelo creado.