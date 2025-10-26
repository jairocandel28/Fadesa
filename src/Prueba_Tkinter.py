
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from lector import *


def limpiar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()



def pantalla_principal(ventana):
    limpiar_ventana(ventana)
    ventana.title("Explorado de Archivos")

    frame_superior = tk.Frame(ventana)
    frame_superior.pack(fill="x", pady=10, padx=10)

    boton_explorar = tk.Button(frame_superior, text="📁", font=("Arial", 18))
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

    # FRAME PARA DETECCION DE DATOS INEXISTENTES
    frame_deteccion = tk.LabelFrame(ventana, text='Detección de valores inexistentes', padx=10, pady=10)
    frame_deteccion.pack(fill="x", padx=10, pady=10)

    boton_detectar = tk.Button(frame_deteccion, text="Detectar valores inexistentes")
    boton_detectar.pack(side="left", padx=10)

    # Solo un Label para mostrar resultados
    etiqueta_resultado = tk.Label(frame_deteccion, text="", justify="left")
    etiqueta_resultado.pack(side="left", padx=10)

    # Variables
    entrada_var = tk.StringVar()
    salida_var = tk.StringVar()

    # Entrada
    etiqueta_entrada = tk.Label(frame_inferior, text="Selecciona la columna ENTRADA:")
    etiqueta_entrada.pack(side="left", padx=5)
    combo_entrada = ttk.Combobox(frame_inferior, textvariable=entrada_var, state="readonly", width=30)
    combo_entrada.pack(side="left", padx=5)

    # Salida
    etiqueta_salida = tk.Label(frame_inferior, text="Selecciona la columna SALIDA:")
    etiqueta_salida.pack(side="left", padx=10)
    combo_salida = ttk.Combobox(frame_inferior, textvariable=salida_var, state="readonly", width=30)
    combo_salida.pack(side="left", padx=5)

    # Botón para confirmar la selección de columnas
    boton_confirmar = tk.Button(
        frame_inferior, 
        text="CONFIRMAR SELECCIÓN", 
        font=("Arial", 10, "bold"),
        bg="#d0f0c0"
    )
    boton_confirmar.pack(side="left", padx=15)

    # Variables para guardar la selección
    seleccion_entrada = {"columna": None}
    seleccion_salida = {"columna": None}


    def explorar_archivo():
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(
                ("Todos los archivos", "*.*"),
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
            datos = leer_archivo(ruta)


            if datos is None or datos.empty:
                messagebox.showwarning("Archivo vacío", "El archivo no contiene datos o no fue posible cargarlos.")
                return
            
            boton_detectar.config(command=lambda d=datos: detectar_val_inexistentes(d))

            
            columnas = list(datos.columns)
            tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

            # Encabezados
            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=120, anchor="center")

            # Filas
            for _, fila in datos.iterrows():
                tabla.insert("", "end", values=list(fila))

            tabla.pack(fill="both", expand=True)

            # Scrollbars
            vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
            hsb = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
            tabla.configure(yscroll=vsb.set, xscroll=hsb.set)
            vsb.pack(side="right", fill="y")
            hsb.pack(side="bottom", fill="x")

            # Actualización de los desplegables con las columnas del archivo
            combo_entrada["values"] = columnas
            combo_salida["values"] = columnas

            # Reiniciar selección anterior y variables
            entrada_var.set("")
            salida_var.set("")

            seleccion_entrada["columna"] = None
            seleccion_salida["columna"] = None

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el archivo:\n{e}")
    
    def detectar_val_inexistentes(datos):
        if datos is None:
            messagebox.showwarning("Sin datos","Debes cargar un archivo con datos.")
            return
        try:
            nulos_columna = datos.isna().sum()
            nulos_columna = nulos_columna[nulos_columna>0]
            if nulos_columna.empty:
                messagebox.showinfo("Comprobación completada", "No se detectaron valores inexistentes")
                return
            total_nulos = int(nulos_columna.sum())
            texto = f"Se detectaron {total_nulos} valores inexistentes en {len(nulos_columna)} columnas:\n"
            for col, cantidad in nulos_columna.items():
                texto += f"• {col}: {cantidad} valores faltantes\n"

            messagebox.showwarning("Valores inexistentes detectados", texto)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al analizar los datos:\n{e}")


    def seleccionar_entrada(event):
        """Guarda la columna seleccionada como entrada."""
        seleccion_entrada["columna"] = entrada_var.get()


    def seleccionar_salida(event):
        """Guarda la columna seleccionada como salida."""
        seleccion_salida["columna"] = salida_var.get()


    def confirmar_seleccion():
        entrada = seleccion_entrada["columna"]
        salida = seleccion_salida["columna"]

        if not entrada or not salida:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una columna ENTRADA y una columna SALIDA antes de confirmar."
            )
            return

        # Confirmación final
        messagebox.showinfo(
            "Selección confirmada",
            f"Entrada seleccionada: {entrada}\nSalida seleccionada: {salida}"
        )

    # Asociaciones
    boton_explorar.config(command=explorar_archivo)
    combo_entrada.bind("<<ComboboxSelected>>", seleccionar_entrada)
    combo_salida.bind("<<ComboboxSelected>>", seleccionar_salida)
    boton_confirmar.config(command=confirmar_seleccion)







