import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from lector import *
from modelo import separacion_entrenamiento_test


def limpiar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()


def pantalla_principal(ventana):
    limpiar_ventana(ventana)
    ventana.title("Fadesa")

    datos = None

    frame_superior = tk.Frame(ventana)
    frame_superior.pack(fill="x", pady=10, padx=10)

    boton_explorar = tk.Button(frame_superior, text="📁 ABRIR ARCHIVO", font=("Arial", 14))
    boton_explorar.pack(side="left", padx=10)

    ruta_var = tk.StringVar(value="Ningún archivo seleccionado")

    etiqueta_ruta = tk.Label(
        frame_superior,
        textvariable=ruta_var,
        wraplength=800,
        anchor="w",
        justify="left",
        fg="blue"
    )
    etiqueta_ruta.pack(side="left", fill="x", expand=True, padx=10)

    # FRAME TABLA
    frame_tabla = tk.Frame(ventana, bd=2, relief="groove")
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # FRAME PARA LOS SELECTORES DE COLUMNAS
    frame_inferior = tk.Frame(ventana)
    frame_inferior.pack(fill="x", padx=10, pady=10)

    frame_entrada = tk.Frame(frame_inferior)
    frame_entrada.pack(side="left", padx=20, anchor="n")

    frame_salida = tk.Frame(frame_inferior)
    frame_salida.pack(side="left", padx=40, anchor="n")

    # FRAME PARA DETECCION DE DATOS INEXISTENTES
    frame_deteccion = tk.LabelFrame(ventana, text='Detección de valores inexistentes', padx=10, pady=10)
    frame_deteccion.pack(fill="x", padx=10, pady=10)

    boton_detectar = tk.Button(frame_deteccion, text="Detectar valores inexistentes")
    boton_detectar.pack(side="left", padx=10)

    etiqueta_resultado = tk.Label(frame_deteccion, text="", justify="left")
    etiqueta_resultado.pack(side="left", padx=10)

    # FRAME PARA MANEJO DE ERRORES:
    frame_manejo = tk.LabelFrame(ventana, text='Manejo de valores inexistentes', padx=10, pady=10)

    # Variables
    salida_var = tk.StringVar()
    opcion_var = tk.StringVar(value="Eliminar")

    # OPCIONES QUE SE PROPORCIONAN AL USUARIO:
    rb_eliminar = tk.Radiobutton(frame_manejo, text='Eliminar filas con valores inexistentes', variable=opcion_var, value="Eliminar")
    rb_media = tk.Radiobutton(frame_manejo, text='Rellenar con media', variable=opcion_var, value="media")
    rb_mediana = tk.Radiobutton(frame_manejo, text='Rellenar con mediana', variable=opcion_var, value="mediana")
    rb_constante = tk.Radiobutton(frame_manejo, text='Rellenar con constante', variable=opcion_var, value="constante")

    rb_eliminar.pack(anchor="w")
    rb_media.pack(anchor="w")
    rb_mediana.pack(anchor="w")
    rb_constante.pack(anchor="w")

    # Pedir constante al usuario
    cte = tk.Entry(frame_manejo, width=10)
    cte.pack(anchor="w", padx=20)

    # Botón para aplicar preprocesado:
    boton_aplicar = tk.Button(frame_manejo, text="Aplicar preprocesado", bg="#d0f0c0")
    boton_aplicar.pack(pady=5)

    # Entrada
    etiqueta_entrada = tk.Label(frame_entrada, text="Selecciona la(s) columna(s) ENTRADA:")
    etiqueta_entrada.pack(anchor="w")

    listbox_entrada = tk.Listbox(frame_entrada, selectmode='multiple', exportselection=False, height=6, width=30)
    listbox_entrada.pack(pady=5)

    # Salida
    etiqueta_salida = tk.Label(frame_salida, text="Selecciona la columna SALIDA:")
    etiqueta_salida.pack(anchor="w")
    combo_salida = ttk.Combobox(frame_salida, textvariable=salida_var, state="readonly", width=30)
    combo_salida.pack(pady=5)

    # Botón para confirmar la selección de columnas
    boton_confirmar = tk.Button(
        frame_salida,
        text="CONFIRMAR SELECCIÓN",
        font=("Arial", 10, "bold"),
        bg="#d0f0c0"
    )
    boton_confirmar.pack(pady=10)

    # Frame para SEPARACIÓN DE DATOS
    frame_modelo = tk.LabelFrame(ventana, text='Separación de datos', padx=10, pady=10)
    # Se mostrará solo cuando corresponda

    # Variables para guardar la selección
    seleccion_entrada = {"columna": None}
    seleccion_salida = {"columna": None}

    # --- FUNCIONES ---

    def explorar_archivo():
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(
                ("Archivos CSV", "*.csv"),
                ("Archivos Excel XLSX", "*.xlsx"),
                ("Archivos Excel XLS", "*.xls"),
                ("Archivos DB", "*.db*"),
            )
        )

        if ruta:
            ruta_var.set(ruta)
            mostrar_datos(ruta)
        else:
            ruta_var.set("Ningún archivo seleccionado")


    def mostrar_datos(ruta):
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        try:
            nonlocal datos
            datos = leer_archivo(ruta)

            if datos is None or datos.empty:
                messagebox.showwarning("Archivo vacío", "El archivo no contiene datos o no fue posible cargarlos.")
                return

            boton_detectar.config(command=lambda d=datos: detectar_val_inexistentes(d))
            boton_aplicar.config(command=lambda d=datos: aplicar_preprocesado(d))

            columnas = list(datos.columns)
            tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=120, anchor="center")

            for _, fila in datos.iterrows():
                tabla.insert("", "end", values=list(fila))

            tabla.pack(fill="both", expand=True)

            # Scrollbars
            vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
            hsb = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
            tabla.configure(yscroll=vsb.set, xscroll=hsb.set)
            vsb.pack(side="right", fill="y")
            hsb.pack(side="bottom", fill="x")

            # Actualizar desplegables
            listbox_entrada.delete(0, tk.END)
            for col in columnas:
                listbox_entrada.insert(tk.END, col)
            combo_salida["values"] = columnas

            salida_var.set("")
            seleccion_entrada["columna"] = None
            seleccion_salida["columna"] = None

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el archivo:\n{e}")


    def detectar_val_inexistentes(datos_param):
        if datos_param is None:
            messagebox.showwarning("Sin datos", "Debes cargar un archivo con datos.")
            return
        try:
            seleccion = listbox_entrada.curselection()
            seleccion_entrada_local = [listbox_entrada.get(var) for var in seleccion]

            if not seleccion_entrada_local:
                messagebox.showinfo("Error", "Debes seleccionar al menos una columna")
                return

            datos_f = datos_param[seleccion_entrada_local]
            nulos_columna = datos_f.isna().sum()
            nulos_columna = nulos_columna[nulos_columna > 0]

            frame_manejo.pack(fill="x", padx=10, pady=10)

            if nulos_columna.empty:
                messagebox.showinfo("Comprobación completada", "No se detectaron valores inexistentes.")
            else:
                total_nulos = int(nulos_columna.sum())
                texto = f"Se detectaron {total_nulos} valores inexistentes en {len(nulos_columna)} columnas:\n"
                for col, cantidad in nulos_columna.items():
                    texto += f"• {col}: {cantidad} valores faltantes\n"
                messagebox.showwarning("Valores inexistentes detectados", texto)

            mostrar_panel_separacion()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al analizar los datos:\n{e}")


    def aplicar_preprocesado(datos_param):
        if datos_param is None:
            messagebox.showwarning("Sin datos", "Debes cargar un archivo con datos.")
            return

        opcion = opcion_var.get()
        try:
            if opcion == "Eliminar":
                datos_param.dropna(inplace=True)
            elif opcion == "media":
                datos_param.fillna(datos_param.mean(numeric_only=True), inplace=True)
            elif opcion == "mediana":
                datos_param.fillna(datos_param.median(numeric_only=True), inplace=True)
            elif opcion == "constante":
                valor = cte.get()
                if valor == "":
                    messagebox.showwarning("Valor vacío", "Debes ingresar un valor constante.")
                    return
                try:
                    valor = float(valor)
                except ValueError:
                    messagebox.showwarning("Valor incorrecto", "Debes ingresar un número.")
                    return
                datos_param.fillna(valor, inplace=True)
            else:
                messagebox.showwarning("Opción desconocida", "Ingrese una opción válida.")
                return

            messagebox.showinfo("Éxito", "Preprocesado aplicado correctamente.")
            mostrar_panel_separacion()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al aplicar el preprocesado:\n{e}")


    # --- SEPARACIÓN DE DATOS ANDER ---


    def mostrar_panel_separacion():
        """Muestra los controles para separar los datos (entrenamiento/test)"""
        if frame_modelo.winfo_ismapped():
            return  

        frame_modelo.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_modelo, text="Porcentaje de entrenamiento (0 - 1):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_train = tk.Entry(frame_modelo, width=10)
        entry_train.insert(0, "0.8")
        entry_train.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_modelo, text="Porcentaje de test (0 - 1):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_test = tk.Entry(frame_modelo, width=10)
        entry_test.insert(0, "0.2")
        entry_test.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_modelo, text="Semilla (random_state):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_seed = tk.Entry(frame_modelo, width=10)
        entry_seed.insert(0, "42")
        entry_seed.grid(row=2, column=1, padx=5, pady=5)

        boton_aplicar_sep = tk.Button(
            frame_modelo,
            text="Aplicar separación",
            bg="#d0f0c0",
            command=lambda: ejecutar_separacion(entry_train.get(), entry_test.get(), entry_seed.get())
        )
        boton_aplicar_sep.grid(row=3, column=0, columnspan=2, pady=10)


    def ejecutar_separacion(train_size, test_size, random_state):
        """Ejecuta la separación de datos con los valores introducidos"""
        try:
            train_size = float(train_size)
            test_size = float(test_size)
            random_state = int(random_state)

            if datos is None or len(datos) < 5:
                messagebox.showerror(
                    "Datos insuficientes",
                    f"No hay suficientes datos para realizar la separación \n"
                    f"Actualmente hay {len(datos) if datos is not None else 0} filas, y se necesitan al menos 5."
                )

            if abs((train_size + test_size) - 1.0) > 0.0001:
                messagebox.showwarning("Advertencia", "Los porcentajes de entrenamiento y test deberían sumar aproximadamente 1.0")

            columnas_entrada = seleccion_entrada.get("columnas", [])
            columna_salida = seleccion_salida["columna"]

            if not columnas_entrada or not columna_salida:
                messagebox.showwarning("Faltan columnas", "Debes seleccionar columnas de entrada y salida.")
                return

            X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
                datos,
                columnas_entrada,
                columna_salida,
                porcentaje_test=test_size,
                random_state=random_state
            )

            messagebox.showinfo(
                "Separación completada",
                f"Entrenamiento: {len(X_train)} filas\nPrueba: {len(X_test)} filas"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al separar los datos:\n{e}")


    def seleccionar_entrada():
        seleccion = listbox_entrada.curselection()
        seleccion_entrada["columnas"] = [listbox_entrada.get(var) for var in seleccion]

    def seleccionar_salida(event):
        seleccion_salida["columna"] = salida_var.get()

    def confirmar_seleccion():
        seleccionar_entrada()
        entradas = seleccion_entrada.get("columnas", [])
        salida = seleccion_salida["columna"]

        if not entradas or not salida:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona al menos una columna de ENTRADA y una de SALIDA antes de confirmar."
            )
            return

        messagebox.showinfo(
            "Selección confirmada",
            f"Entradas seleccionadas: {', '.join(entradas)}\nSalida seleccionada: {salida}"
        )

    # Asociaciones
    boton_explorar.config(command=explorar_archivo)
    combo_salida.bind("<<ComboboxSelected>>", seleccionar_salida)
    boton_confirmar.config(command=confirmar_seleccion)
