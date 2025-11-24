import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lector import leer_archivo
import joblib
from modelo import crear_modelo_lineal_gui, configurar_panel_prediccion, separacion_entrenamiento_test


def limpiar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

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


def pantalla_principal(ventana):
    """Función principal para ejecutar la interfaz gráfica."""
    limpiar_ventana(ventana)
    ventana.title("Fadesa")

    # Frame principal
    main_frame = tk.Frame(ventana)
    main_frame.pack(fill="both", expand=True)

    # Canvas que contendrá todo el contenido desplazable
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Barra vertical
    scrollbar = ttk.Scrollbar(
        main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Vincular la barra
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno que contendrá todos los widgets
    content_frame = tk.Frame(canvas)
    content_frame.bind(
        "<Configure>",
        # Actualiza el área desplazable
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    mensaje_bienvenida = tk.Label(
        content_frame,
        text="👋 Bienvenido.\nPara comenzar, cargue un archivo con el " \
        "botón 'ABRIR ARCHIVO'.",
        font=("Arial", 14),
        fg="gray"
    )
    mensaje_bienvenida.pack(pady=20)

    # PARA MIRAR QUE EL CONTENIDO SE AJUSTE AL ANCHO DE LA PANTALLA
    def resize_canvas(event):
        canvas.itemconfig("all", width=event.width)
    canvas.bind("<Configure>", resize_canvas)

    # Permitir bajar con la rueda del ratón
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    datos = None

    frame_superior = tk.Frame(content_frame)
    frame_superior.pack(fill="x", pady=10, padx=10)

    boton_explorar = tk.Button(
        frame_superior, text="📁 ABRIR ARCHIVO", font=("Arial", 14))
    boton_explorar.pack(side="left", padx=10)

    boton_cargar = tk.Button(
        frame_superior, text="📁 CARGAR MODELO", font=("Arial", 14))
    boton_cargar.pack(side="right", padx=10)

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
    frame_tabla = tk.Frame(content_frame, bd=2, relief="groove", height=200)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # mostrar el marco incluso antes de cargar archivo
    placeholder = tk.Label(
        frame_tabla, text="📄 Carga un archivo para ver los datos", fg="gray")
    placeholder.pack(pady=20)

    # FRAME PRINCIPAL PARA SELECTORES Y PREPROCESADO
    frame_principal_inferior = tk.Frame(content_frame)
    frame_principal_inferior.pack(fill="x", padx=10, pady=10)

    # Configuración del grid
    frame_principal_inferior.columnconfigure(0, weight=1)  # Selectores
    frame_principal_inferior.columnconfigure(1, weight=0)  # Espacio
    frame_principal_inferior.columnconfigure(2, weight=1)  # Preprocesado

    # FRAME PARA LOS SELECTORES DE COLUMNAS
    frame_selectores = tk.Frame(frame_principal_inferior)
    frame_selectores.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

    # Sub-frame para entradas y salidas dentro de frame_selectores
    frame_entrada_salida = tk.Frame(frame_selectores)
    frame_entrada_salida.pack(fill="x", pady=5)

    frame_entrada = tk.Frame(frame_entrada_salida)
    frame_entrada.pack(side="left", padx=20, anchor="n")

    frame_salida = tk.Frame(frame_entrada_salida)
    frame_salida.pack(side="left", padx=40, anchor="n")

    frame_manejo = tk.LabelFrame(
        frame_principal_inferior,
        text='Manejo de valores inexistentes',
        padx=10,
        pady=10
    )

    # Variables
    salida_var = tk.StringVar()
    opcion_var = tk.StringVar(value="Eliminar")

    rb_eliminar = tk.Radiobutton(
        frame_manejo, text='Eliminar filas con valores inexistentes', 
        variable=opcion_var, value="Eliminar")
    rb_media = tk.Radiobutton(
        frame_manejo, text='Rellenar con media', variable=opcion_var, 
        value="media")
    rb_mediana = tk.Radiobutton(
        frame_manejo, text='Rellenar con mediana', variable=opcion_var, 
        value="mediana")
    rb_constante = tk.Radiobutton(
        frame_manejo, text='Rellenar con constante', variable=opcion_var, 
        value="constante")

    rb_eliminar.pack(anchor="w")
    rb_media.pack(anchor="w")
    rb_mediana.pack(anchor="w")
    rb_constante.pack(anchor="w")

    cte = tk.Entry(frame_manejo, width=10)
    cte.pack(anchor="w", padx=20)

    boton_aplicar = tk.Button(
        frame_manejo, text="Aplicar preprocesado", bg="#d0f0c0")
    boton_aplicar.pack(pady=5)

    # Entrada
    etiqueta_entrada = tk.Label(
        frame_entrada, text="Selecciona la(s) columna(s) ENTRADA:")
    etiqueta_entrada.pack(anchor="w")

    listbox_entrada = tk.Listbox(
        frame_entrada, selectmode='multiple', exportselection=False, 
        height=6, width=30)
    listbox_entrada.pack(pady=5)

    # Salida
    etiqueta_salida = tk.Label(
        frame_salida, text="Selecciona la columna SALIDA:")
    etiqueta_salida.pack(anchor="w")
    combo_salida = ttk.Combobox(
        frame_salida, textvariable=salida_var, state="readonly", width=30)
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
    frame_modelo = tk.LabelFrame(
        content_frame, text='Separación de datos', padx=10, pady=10)

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
            ventana_carga = indicador_de_carga("Cargando archivo...")
            ventana.after(100, lambda: (
                mostrar_datos(ruta), ventana_carga.destroy()))
        else:
            ruta_var.set("Ningún archivo seleccionado")

    def mostrar_datos(ruta):
        """Muestra la tabla con los datos del dataframe que haya seleccionado
        el usuario."""
        try:
            mensaje_bienvenida.destroy()
        except:
            pass

        for widget in frame_tabla.winfo_children():
            widget.destroy()

        try:
            nonlocal datos
            datos = leer_archivo(ruta)

            if datos is None or datos.empty:
                messagebox.showwarning(
                    "Archivo vacío", "El archivo no contiene datos o no fue posible cargarlos.")
                return

            boton_aplicar.config(
                command=lambda d=datos: aplicar_preprocesado(d))

            columnas = list(datos.columns)
            tabla = ttk.Treeview(
                frame_tabla, columns=columnas, show="headings")

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=120, anchor="center")

            for _, fila in datos.iterrows():
                tabla.insert("", "end", values=list(fila))

            tabla.pack(fill="both", expand=True)

            # Barra lateral
            vsb = ttk.Scrollbar(
                frame_tabla, orient="vertical", command=tabla.yview)
            hsb = ttk.Scrollbar(
                frame_tabla, orient="horizontal", command=tabla.xview)
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
            messagebox.showerror(
                "Error", f"No se pudo mostrar el archivo:\n{e}")

    def detectar_val_inexistentes(datos_param):
        """Detecta si existe algún valor inexistente en las columnas de entrada
        seleccionadas por el usuario. Además, muestra en qué columnas y cuantos
        valores inexistentes hay en cada una."""
        if datos_param is None:
            messagebox.showwarning(
                "Sin datos", "Debes cargar un archivo con datos.")
            return
        try:
            seleccion = listbox_entrada.curselection()
            seleccion_entrada_local = [
                listbox_entrada.get(var) for var in seleccion]

            if not seleccion_entrada_local:
                messagebox.showinfo(
                    "Error", "Debes seleccionar al menos una columna")
                return

            datos_f = datos_param[seleccion_entrada_local]
            nulos_columna = datos_f.isna().sum()
            nulos_columna = nulos_columna[nulos_columna > 0]

            if nulos_columna.empty:
                messagebox.showinfo("Comprobación completada",
                                    "No se detectaron valores inexistentes.")
                mostrar_panel_separacion()
            else:
                total_nulos = int(nulos_columna.sum())
                texto = f"Se detectaron {total_nulos} valores inexistentes en {len(nulos_columna)} columnas:\n"
                for col, cantidad in nulos_columna.items():
                    texto += f"• {col}: {cantidad} valores faltantes\n"
                messagebox.showwarning(
                    "Valores inexistentes detectados", texto)
                frame_manejo.grid(row=0, column=2, sticky="nsew", padx=(20, 0))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Ocurrió un problema al analizar los datos:\n{e}")

    def aplicar_preprocesado(datos_param):
        """Ejecuta la opción de preprocesado seleccionada por el usuario:
        Rellenar con media o mediana, con una constante o eliminar aquellas
        filas en las que haya algún dato inexistente."""
        if datos_param is None:
            messagebox.showwarning(
                "Sin datos", "Debes cargar un archivo con datos.")
            return

        opcion = opcion_var.get()
        try:
            if opcion == "Eliminar":
                datos_param.dropna(inplace=True)
            elif opcion == "media":
                datos_param.fillna(datos_param.mean(
                    numeric_only=True), inplace=True)
            elif opcion == "mediana":
                datos_param.fillna(datos_param.median(
                    numeric_only=True), inplace=True)
            elif opcion == "constante":
                valor = cte.get()
                if valor == "":
                    messagebox.showwarning(
                        "Valor vacío", "Debes ingresar un valor constante.")
                    return
                try:
                    valor = float(valor)
                except ValueError:
                    messagebox.showwarning(
                        "Valor incorrecto", "Debes ingresar un número.")
                    return
                datos_param.fillna(valor, inplace=True)
            else:
                messagebox.showwarning(
                    "Opción desconocida", "Ingrese una opción válida.")
                return

            messagebox.showinfo(
                "Éxito", "Preprocesado aplicado correctamente.")
            frame_manejo.grid_forget()
            mostrar_panel_separacion()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Ocurrió un problema al aplicar el preprocesado:\n{e}")

    # --- SEPARACIÓN DE DATOS ---

    def mostrar_panel_separacion():
        """Muestra los controles para separar los datos (entrenamiento/test)"""
        if frame_modelo.winfo_ismapped():
            return

        frame_modelo.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_modelo, text="Porcentaje de entrenamiento (0 - 1):").grid(row=0,
                                                                                 column=0, sticky="w", padx=5, pady=5)
        entry_train = tk.Entry(frame_modelo, width=10)
        entry_train.insert(0, "0.8")
        entry_train.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_modelo, text="Semilla (random_state):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        entry_seed = tk.Entry(frame_modelo, width=10)
        entry_seed.insert(0, "42")
        entry_seed.grid(row=1, column=1, padx=5, pady=5)

        boton_aplicar_sep = tk.Button(
            frame_modelo,
            text="📊 Aplicar división entrenamiento/test",
            bg="#d0f0c0",
            command=lambda: ejecutar_separacion(
                entry_train.get(), entry_seed.get())
        )
        boton_aplicar_sep.grid(row=2, column=0, columnspan=2, pady=10)

        boton_modelo = tk.Button(
            frame_modelo,
            text="Crear modelo lineal",
            bg="#90EE90",
            command=lambda: crear_modelo_lineal_gui(
                ventana, seleccion_entrada, seleccion_salida, datos, content_frame, frame_modelo)
        )
        boton_modelo.grid(row=3, column=0, columnspan=2, pady=10)

    def ejecutar_separacion(train_size, random_state):
        """Ejecuta la separación de datos con los valores introducidos.
        Ahora solo se solicita train_size; test_size se calcula como 1 - train_size."""
        try:
            train_size = float(train_size)
            test_size = 1.0 - train_size
            random_state = int(random_state)

            if datos is None or len(datos) < 5:
                messagebox.showerror(
                    "Datos insuficientes",
                    f"No hay suficientes datos para realizar la separación \n"
                    f"Actualmente hay {len(datos) if datos is not None else 0} filas, y se necesitan al menos 5."
                )
                return

            if not (0.0 < train_size < 1.0):
                messagebox.showwarning(
                    "Valor incorrecto", "El porcentaje de entrenamiento debe estar entre 0 y 1 (exclusivo).")
                return

            columnas_entrada = seleccion_entrada.get("columnas", [])
            columna_salida = seleccion_salida["columna"]

            if not columnas_entrada or not columna_salida:
                messagebox.showwarning(
                    "Faltan columnas", "Debes seleccionar columnas de entrada y salida.")
                return

            X_train, X_test, y_train, y_test = separacion_entrenamiento_test(
                datos,
                columnas_entrada,
                columna_salida,
                porcentaje_test=test_size,
                random_state=random_state
            )

            messagebox.showinfo(
                "División realizada",
                f"Entrenamiento: {len(X_train)} filas\nPrueba: {len(X_test)} filas"
            )

        except Exception as e:
            messagebox.showerror(
                "Error", f"Ocurrió un error al separar los datos:\n{e}")

    def cargar_modelo():
        """Implementa el método para cargar un modelo que el usuario ha guardado anteriormente."""
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(
                ("Archivos Joblib", "*.joblib"),
                ("Archivos Pickle", "*.pkl"),
                ("Todos los archivos", "*.*"),
            )
        )

        if not ruta:
            ruta_var.set("Ningún archivo seleccionado")
            return

        try:
            modelo_cargado = joblib.load(ruta)

            if not isinstance(modelo_cargado, dict):
                raise ValueError(
                    "El archivo no contiene un diccionario válido.")

        except Exception as e:
            messagebox.showerror(
                "Error al cargar archivo",
                "No se pudo cargar el archivo seleccionado."
            )
            return

        limpiar_ventana(ventana)

        main_frame = tk.Frame(ventana)
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        frame_superior = tk.Frame(content_frame)
        frame_superior.pack(fill="x", pady=10, padx=10)

        modelo_cargado = joblib.load(ruta)

        información = (
            f"Modelo: {modelo_cargado['modelo_objeto']}\n\n"
            f"Columnas de entrada: {modelo_cargado['columnas_entrada']}\n\n"
            f"Columna de salida: {modelo_cargado['columna_salida']}\n\n"
            f"Métricas:\n"
            f"  - R2 Train: {modelo_cargado['metricas']['r2_train']}\n"
            f"  - R2 Test: {modelo_cargado['metricas']['r2_test']}\n"
            f"  - ECM Train: {modelo_cargado['metricas']['ecm_train']}\n"
            f"  - ECM Test: {modelo_cargado['metricas']['ecm_test']}\n\n"
            f"Descripción:\n"
            f"{modelo_cargado['descripcion']}\n\n"
            f"Fórmula: {modelo_cargado['formula']}\n"
        )

        label = tk.Label(frame_superior, text=información, font=("Arial", 14))
        label.pack(padx=10, pady=10)

        # --- INICIO DE INTEGRACIÓN: PREDICCIÓN ---
        # Extraer los datos necesarios del diccionario cargado
        modelo_cargado_obj = modelo_cargado['modelo_objeto']
        cols_entrada_cargadas = modelo_cargado['columnas_entrada']
        col_salida_cargada = modelo_cargado['columna_salida']

        # Crear un frame específico para la predicción dentro del frame_superior o crear uno nuevo abajo
        frame_pred_container = tk.Frame(content_frame)
        frame_pred_container.pack(fill="x", padx=10)

        configurar_panel_prediccion(
            frame_pred_container,
            modelo_cargado_obj,
            cols_entrada_cargadas,
            col_salida_cargada
        )
        # --- FIN DE INTEGRACIÓN ---

        boton_regresar = tk.Button(
            frame_superior, text="⬅️ VOLVER A LA PANTALLA DE INICIO", font=("Arial", 14))

        boton_regresar = tk.Button(
            frame_superior, text="⬅️ VOLVER A LA PANTALLA DE INICIO", font=("Arial", 14))
        boton_regresar.pack(side="bottom", padx=10)

        boton_regresar.config(command=lambda: pantalla_principal(ventana))

        messagebox.showinfo(
            "Cargar modelo",
            f"El modelo ha sido cargado exitosamente."
        )

    def seleccionar_entrada():
        """Guarda la(s) entrada(s) seleccionada por el usuario."""
        seleccion = listbox_entrada.curselection()
        seleccion_entrada["columnas"] = [
            listbox_entrada.get(var) for var in seleccion]

    def seleccionar_salida(event):
        """Guarda la salida seleccionada por el usuario."""
        seleccion_salida["columna"] = salida_var.get()

    def confirmar_seleccion():
        """Permite al usuario confirmar la selección de la entrada y la salida."""
        seleccionar_entrada()
        entradas = seleccion_entrada.get("columnas", [])
        salida = seleccion_salida["columna"]

        if datos is None:
            messagebox.showwarning(
                "Sin datos", "Primero carga un archivo con datos.")
            return

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

        detectar_val_inexistentes(datos)

    boton_explorar.config(command=explorar_archivo)
    combo_salida.bind("<<ComboboxSelected>>", seleccionar_salida)
    boton_confirmar.config(command=confirmar_seleccion)
    boton_cargar.config(command=cargar_modelo)
