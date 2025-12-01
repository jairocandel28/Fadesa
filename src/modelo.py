import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
import joblib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def indicador_de_carga(texto="Procesando..."):
    ventana_carga = tk.Toplevel()
    ventana_carga.title("Cargando")
    ventana_carga.geometry("300x90")
    ventana_carga.resizable(False, False)

    tk.Label(ventana_carga, text=texto, font=("Arial", 12)).pack(pady=5)
    pb = ttk.Progressbar(ventana_carga, mode="indeterminate")
    pb.pack(fill="x", padx=20, pady=10)
    pb.start()

    return ventana_carga


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
    formula = " + ".join([f"{coef:.3f}·{col}" for coef,
                         col in zip(modelo.coef_, columnas_entrada)])
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

# ---CREACIÓN Y GUARDADO DEL MODELO---

def crear_modelo_lineal_gui(ventana, seleccion_entrada, seleccion_salida, datos, content_frame, frame_modelo):
    """Crea el modelo lineal con las entradas y la salida que el usuario ha seleccionado anteriormente.
    También muestra la fórmula y los datos de entrenamiento, así como una gráfica cuando el usuario sólo
    ha seleccionado una entrada."""
    try:
        ventana_carga = indicador_de_carga("Creando modelo...")
        ventana.update()

        columnas_entrada = seleccion_entrada.get("columnas", [])
        columna_salida = seleccion_salida["columna"]

        if not columnas_entrada or not columna_salida:
            messagebox.showwarning(
                "Faltan columnas", "Selecciona columnas de entrada y salida antes de continuar")
            return

        if datos is None or len(datos) < 5:
            messagebox.showwarning(
                "Sin datos", "Primero carga y prepara los datos.")
            return

        X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
            datos, columnas_entrada, columna_salida, porcentaje_test=0.2, random_state=42
        )

        resultados = crear_modelo_lineal(
            X_train, X_test, y_train, y_test, columnas_entrada)

        texto = (
            f"Modelo lineal creado correctamente\n\n"
            f"Fórmula:\n{columna_salida} = {resultados['formula']}\n\n"
            f"Entrenamiento:\n"
            f"  R² = {resultados['r2_train']:.4f}\n"
            f"  ECM = {resultados['ecm_train']:.4f}\n\n"
            f"Test:\n"
            f"  R² = {resultados['r2_test']:.4f}\n"
            f"  ECM = {resultados['ecm_test']:.4f}"
        )

        messagebox.showinfo("Modelo creado", texto)
        modelo_objeto = resultados['modelo']
        configurar_panel_prediccion(
            content_frame, modelo_objeto, columnas_entrada, columna_salida)

        if len(columnas_entrada) == 1:
            col = columnas_entrada[0]
            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)

            ax.scatter(X_train[col], y_train, label="Entrenamiento")
            ax.scatter(X_test[col], y_test, label="Test")
            ax.plot(X_train[col], resultados["y_train_pred"],
                    label="Recta de ajuste")
            ax.set_xlabel(col)
            ax.set_ylabel(columna_salida)
            ax.set_title("Regresión lineal: entrenamiento vs test")
            ax.legend()

            frame_grafico = tk.LabelFrame(
                content_frame, text="Gráfico de modelo", padx=10, pady=10)
            frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

            canvas_fig = FigureCanvasTkAgg(fig, frame_grafico)
            canvas_fig.draw()
            canvas_fig.get_tk_widget().pack(fill="both", expand=True)

        # --- Gráfico de dispersión Predicción vs. Real (para el conjunto de test) ---
        
        # Crear la figura
        fig_pred = Figure(figsize=(6, 4))
        ax_pred = fig_pred.add_subplot(111)

        # Scatter plot de valores reales vs. valores predichos
        ax_pred.scatter(y_test, resultados["y_test_pred"], label="Predicciones Test")
        
        # Línea ideal (y=x): Determina el rango de valores para la línea
        y_test_numpy = y_test.values if isinstance(y_test, pd.Series) else y_test
        
        min_val = min(y_test_numpy.min(), resultados["y_test_pred"].min())
        max_val = max(y_test_numpy.max(), resultados["y_test_pred"].max())
        line_coords = [min_val, max_val]

        # Dibuja la línea y=x (ideal) en rojo
        ax_pred.plot(line_coords, line_coords, 'r--', label="Predicción Ideal ($y=x$)", alpha=0.7)

        # Etiquetas y título
        ax_pred.set_xlabel(f"Valores Reales de {columna_salida}")
        ax_pred.set_ylabel(f"Predicciones de {columna_salida}")
        ax_pred.set_title("Predicción vs. Valores Reales (Conjunto de Test)")
        ax_pred.legend()
        ax_pred.grid(True, linestyle='--', alpha=0.6)

        frame_grafico_pred = tk.LabelFrame(
            content_frame, 
            text="Gráfico de Predicción vs. Real (Test)", 
            padx=10, pady=10)
        
        frame_grafico_pred.pack(fill="both", expand=True, padx=10, pady=10)

        canvas_fig_pred = FigureCanvasTkAgg(fig_pred, frame_grafico_pred)
        canvas_fig_pred.draw()
        canvas_fig_pred.get_tk_widget().pack(fill="both", expand=True)
        


        if len(columnas_entrada) != 1:
            messagebox.showinfo(
                "Gráfico de regresión no disponible",
                 "El gráfico de la recta de regresión simple solo se genera si hay una variable de entrada numérica.")
        ventana_carga.destroy()

        frame_descripcion = tk.LabelFrame(
            content_frame, text="Descripción y Guardado del Modelo", padx=10, pady=10)
        frame_descripcion.pack(
            fill="x", padx=10, pady=10, after=frame_modelo)

        tk.Label(frame_descripcion, text="Escribe una descripción para este modelo (opcional):").pack(
            anchor="w")

        texto_descripcion = tk.Text(
            frame_descripcion, width=100, height=6, wrap="word")
        texto_descripcion.pack(pady=5, fill="x", expand=True)

        def preparar_y_guardar_modelo():
            """Obtiene los datos del modelo e implementa un botón en la interfaz que le permita
            al usuario guardar dicho modelo."""
            descripcion = texto_descripcion.get("1.0", tk.END).strip()

            # Obtener el objeto del modelo desde los resultados
            modelo_obj = resultados.get('modelo')
            if not isinstance(modelo_obj, LinearRegression):
                messagebox.showerror(
                    "Error", "No se encontró un objeto de modelo válido para guardar.")
                return

            metricas = {
                'r2_train': resultados.get('r2_train'),
                'r2_test': resultados.get('r2_test'),
                'ecm_train': resultados.get('ecm_train'),
                'ecm_test': resultados.get('ecm_test')
            }

            guardar_modelo(
                modelo=modelo_obj,
                columnas_entrada=columnas_entrada,
                columna_salida=columna_salida,
                metricas=metricas,
                descripcion=descripcion)

        boton_guardar_modelo = tk.Button(
            frame_descripcion,
            text="💾 Guardar Modelo",
            font=("Arial", 10, "bold"),
            bg="#c0f0ff",
            command=preparar_y_guardar_modelo)
        boton_guardar_modelo.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error al crear modelo", str(e))


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
        fg="#2E8B57")
    frame_prediccion.pack(fill="x", padx=10, pady=20)

    entradas_widgets = {}

    tk.Label(frame_prediccion, text="Ingrese los valores para las variables de entrada:",
             font=("Arial", 9, "italic")).pack(pady=(0, 10), anchor="w")

    frame_inputs = tk.Frame(frame_prediccion)
    frame_inputs.pack(fill="x")

    for i, col in enumerate(columnas_entrada):
        lbl = tk.Label(frame_inputs, text=f"{col}:", font=("Arial", 10))
        lbl.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        entry = tk.Entry(frame_inputs, width=20)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)

        entradas_widgets[col] = entry

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

    def realizar_prediccion():
        valores = []
        try:
            for col in columnas_entrada:
                valor_txt = entradas_widgets[col].get().strip()

                if not valor_txt:
                    messagebox.showwarning(
                        "Datos faltantes", f"Por favor, ingrese un valor para '{col}'.")
                    return

                try:
                    valor_num = float(valor_txt)
                    valores.append(valor_num)
                except ValueError:
                    messagebox.showerror(
                        "Error de formato", f"El valor en '{col}' debe ser numérico.")
                    return

            prediccion = modelo.predict([valores])[0]

            lbl_resultado.config(
                text=f"Predicción para {columna_salida}: {prediccion:.4f}", fg="green")

        except Exception as e:
            messagebox.showerror("Error en predicción",
                                 f"Ocurrió un error inesperado:\n{e}")

    boton_predecir = tk.Button(
        frame_prediccion,
        text="🚀 Calcular Predicción",
        bg="#FFA07A",
        font=("Arial", 10, "bold"),
        command=realizar_prediccion
    )
    boton_predecir.pack(pady=15)

    lbl_resultado.pack(pady=5)
