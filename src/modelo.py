import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from tkinter import filedialog, messagebox, ttk
import joblib
import tkinter as tk


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


def mostrar_descripcion_modelo(resultados, content_frame):
        """Muestra un área de texto donde el usuario puede escribir una descripción del modelo."""
        frame_descripcion = tk.LabelFrame(
            content_frame, text="Descripción del modelo", padx=10, pady=10)
        frame_descripcion.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_descripcion,
                 text="Escribe una descripción para este modelo:").pack(anchor="w")

        texto_descripcion = tk.Text(
            frame_descripcion, width=100, height=6, wrap="word")
        texto_descripcion.pack(pady=5)

        def guardar_descripcion():
            descripcion = texto_descripcion.get("1.0", tk.END).strip()
            if descripcion == "":
                messagebox.showwarning(
                    "Descripción vacía", "No se ha escrito ninguna descripción (se guardará como vacía).")
            try:
                with open("descripcion_modelo.txt", "w", encoding="utf-8") as f:
                    f.write("=== Descripción del modelo ===\n\n")
                    f.write(f"Fórmula: {resultados['formula']}\n\n")
                    f.write(
                        f"Descripción del usuario:\n{descripcion if descripcion else '(sin descripción)'}\n")
                messagebox.showinfo(
                    "Guardado", "La descripción del modelo se ha guardado correctamente en 'descripcion_modelo.txt'.")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo guardar la descripción:\n{e}")

        boton_guardar_desc = tk.Button(
            frame_descripcion, text="💾 Guardar descripción", bg="#c0f0ff", command=guardar_descripcion)
        boton_guardar_desc.pack(pady=5)


def guardar_modelo(modelo, columnas_entrada, columna_salida, metricas, descripcion):
        """Implementa el método para guardar un modelo en la ubicación que 
        desee el usuario."""
        try:
            pedir_usuario = filedialog.asksaveasfilename(
                title="Guardar modelo",
                defaultextension=".joblib",
                filetypes=[
                    ("Archivos Joblib", "*.joblib"),
                    ("Archivos Pickle", "*.pkl"),
                    ("Todos los archivos", "*.*")])

            if not pedir_usuario:
                return
            datos_para_guardar = {
                'modelo_objeto': modelo,
                'columnas_entrada': columnas_entrada,
                'columna_salida': columna_salida,
                'metricas': metricas,
                'descripcion': descripcion,
                'formula': f"{modelo.intercept_:.4f} + " + " + ".join([f"{coef:.4f} * {col}" for coef, col in zip(modelo.coef_, columnas_entrada)])}

            joblib.dump(datos_para_guardar, pedir_usuario)

            messagebox.showinfo(
                "Modelo guardado",
                f"El modelo y sus metadatos han sido guardados correctamente en:\n{pedir_usuario}")

        except Exception as e:
            messagebox.showerror(
                "Error al guardar",
                f"Ocurrió un problema al intentar guardar el modelo:\n{e}\n\n"
                "Por favor, verifica los permisos de escritura o el espacio en disco.")


def configurar_panel_prediccion(frame_padre, modelo, columnas_entrada, columna_salida):
        """
        Genera el panel de predicción con campos dinámicos basados en las columnas de entrada.
        Cumple con los criterios de aceptación de entradas dinámicas, validación y visualización.
        """
        frame_prediccion = tk.LabelFrame(
            frame_padre, 
            text="🔮 Realizar Predicción Interactiva", 
            padx=10, pady=10,
            font=("Arial", 10, "bold"),
            fg="#2E8B57" # Verde bosque para destacar
        )
        frame_prediccion.pack(fill="x", padx=10, pady=20)

        # Diccionario para guardar referencias a los Entry widgets
        entradas_widgets = {}

        # --- Campos de Entrada Dinámicos ---
        tk.Label(frame_prediccion, text="Ingrese los valores para las variables de entrada:", 
                 font=("Arial", 9, "italic")).pack(pady=(0, 10), anchor="w")

        frame_inputs = tk.Frame(frame_prediccion)
        frame_inputs.pack(fill="x")

        for i, col in enumerate(columnas_entrada):
            # Usamos grid para organizar etiquetas y campos
            lbl = tk.Label(frame_inputs, text=f"{col}:", font=("Arial", 10))
            lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            entry = tk.Entry(frame_inputs, width=20)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            
            entradas_widgets[col] = entry

        # --- Etiqueta de Resultado ---
        lbl_resultado = tk.Label(
            frame_prediccion, 
            text="El resultado aparecerá aquí", 
            font=("Arial", 12, "bold"), 
            fg="blue",
            bg="#f0f0f0",
            pady=10,
            width=40,
            relief="sunken"
        )

        # --- Lógica de Predicción ---
        def realizar_prediccion():
            valores = []
            try:
                # Recolectar y validar datos
                for col in columnas_entrada:
                    valor_txt = entradas_widgets[col].get().strip()
                    
                    if not valor_txt:
                        messagebox.showwarning("Datos faltantes", f"Por favor, ingrese un valor para '{col}'.")
                        return
                    
                    try:
                        valor_num = float(valor_txt)
                        valores.append(valor_num)
                    except ValueError:
                        messagebox.showerror("Error de formato", f"El valor en '{col}' debe ser numérico.")
                        return

                # Realizar predicción (sklearn espera un array 2D: [[val1, val2, ...]])
                # Nota: Si el modelo se entrenó con DataFrames, sklearn suele aceptar arrays simples 
                # siempre que el orden sea el mismo.
                prediccion = modelo.predict([valores])[0]
                
                # Mostrar resultado
                lbl_resultado.config(text=f"Predicción para {columna_salida}: {prediccion:.4f}", fg="green")

            except Exception as e:
                messagebox.showerror("Error en predicción", f"Ocurrió un error inesperado:\n{e}")

        # --- Botón de Acción ---
        boton_predecir = tk.Button(
            frame_prediccion, 
            text="🚀 Calcular Predicción", 
            bg="#FFA07A", # Salmón claro
            font=("Arial", 10, "bold"),
            command=realizar_prediccion
        )
        boton_predecir.pack(pady=15)
        
        lbl_resultado.pack(pady=5)




