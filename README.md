# Fadesa

## Repositorio Proyecto ES

Este repositorio está destinado al desarrollo de una aplicación para llevar a cabo análisis estadísticos y predictivos sobre un dataset a elección del usuario. Su propósito principal es permitir a los usuarios construir, visualizar y gestionar modelos de regresión lineal simple y múltiple de manera intuitiva a través de una interfaz gráfica (GUI).


 ### Instrucciones de instalación y uso:

* Para la correcta instalación de este programa el usuario necesita descargar todos los archivos presentes
en este repositorio y mantener dichos archivos guardados en la misma carpeta.
Una vez disponga del material ha de abrir la terminal de su dispositivo y llegar hasta la carpeta src
donde está el archvio main.py. Luego tendrá que escribir en la terminal: python main.py, y se ejecutará el
programa.
<img width="1731" height="925" alt="image" src="https://github.com/user-attachments/assets/548866f4-f495-4e54-93bf-268294026455" />


* Para un buen uso del programa la propia interfaz gráfica le irá guiando en como utilizar las funciones
disponibles paso a paso.
Primero podrá abrir un archivo de tipo .csv, .xlsx, .xls o .db; o cargar un modelo creado previamente en
este programa.
<img width="2557" height="1524" alt="image" src="https://github.com/user-attachments/assets/5f0ef930-02a6-4d4f-9b19-97e478b0237b" />


* Luego se le dará la opción de volver al menú principal en el caso de haber cargado un modelo o de seleccionar
las filas de entrada y la fila de salida que se utilzarán en la creación del modelo. Al confirmar la selección
se comprobará la aparición de números nulos en dichas columnas y se le dará al usuario la opción de modificar
esos valores entre varias opciones(media, mediana, con una constante introducida por el usuario o eliminar dichas filas con valores nulos).
<img width="2557" height="1525" alt="image" src="https://github.com/user-attachments/assets/40b54b2d-d421-45e8-bebf-ca1f08182aa0" />
<img width="2559" height="1375" alt="image" src="https://github.com/user-attachments/assets/e2810ac9-47df-4fc7-8a57-abbb2712139a" />


* Posteriormente, se le permitirá al usuario la elección entre el porcentaje de entrenamiento (el resto será
utilizado para test), donde dicho porcentaje debe escribirse en formato "tanto por uno" (por ejemplo, el 30% sería 0.3) y una semilla para crear el modelo lineal para mostrar los resultados del modelo.
<img width="2559" height="1380" alt="Captura de pantalla 2025-12-15 113648" src="https://github.com/user-attachments/assets/1108367f-66ff-4445-9d51-b043aa665fe6" />

* A continuación se se le permitirá la opción de escribir una descripción para guardar el modelo y si el usuario ha decidido previamente elegir sólo una columna de entrada, aparecerá en pantalla una gráfica del modelo creado. También es posible realizar una predicción para los valores que usted desee para las distintas columnas de entrada (donde sólo será posible introducir números).
 <img width="2559" height="1493" alt="image" src="https://github.com/user-attachments/assets/dde4335b-b6d4-462a-af04-bc518beb3048" />

* Finalmente, se mostrará un gráfico de los valores reales contra la predicción.
<img width="2558" height="1385" alt="image" src="https://github.com/user-attachments/assets/91d74d0c-05bb-4e84-86de-434dac819bde" />

* Además, también se le permitirá cargar un modelo previamente guardado, seleccionando en el buscador un archivo de tipo .joblib o .pickle y relizar predicciones sobre dicho modelo.
<img width="767" height="1126" alt="image" src="https://github.com/user-attachments/assets/cea6411d-2b9b-4c36-8f19-ec8fee93155f" />

