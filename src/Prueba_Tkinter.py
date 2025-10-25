
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

    # Variables
    feature_var = tk.StringVar()
    target_var = tk.StringVar()

    # Feature
    etiqueta_feature = tk.Label(frame_inferior, text="Selecciona la columna FEATURE:")
    etiqueta_feature.pack(side="left", padx=5)
    combo_feature = ttk.Combobox(frame_inferior, textvariable=feature_var, state="readonly", width=30)
    combo_feature.pack(side="left", padx=5)

    # Target
    etiqueta_target = tk.Label(frame_inferior, text="Selecciona la columna TARGET:")
    etiqueta_target.pack(side="left", padx=10)
    combo_target = ttk.Combobox(frame_inferior, textvariable=target_var, state="readonly", width=30)
    combo_target.pack(side="left", padx=5)

    # Botón para confirmar la selección de columnas
    boton_confirmar = tk.Button(
        frame_inferior, 
        text="CONFIRMAR SELECCIÓN", 
        font=("Arial", 10, "bold"),
        bg="#d0f0c0"
    )
    boton_confirmar.pack(side="left", padx=15)

    # Variables para guardar la selección
    seleccion_feature = {"columna": None}
    seleccion_target = {"columna": None}


    def explorar_archivo():
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(
                ("Archivos CSV", "*.csv"),
                ("Archivos Excel", "*.xlsx;*.xls"),
                ("Archivos DB", "*.db*")
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
            combo_feature["values"] = columnas
            combo_target["values"] = columnas

            # Reiniciar selección anterior y variables
            feature_var.set("")
            target_var.set("")

            seleccion_feature["columna"] = None
            seleccion_target["columna"] = None

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el archivo:\n{e}")


    def seleccionar_feature(event):
        """Guarda la columna seleccionada como feature."""
        seleccion_feature["columna"] = feature_var.get()


    def seleccionar_target(event):
        """Guarda la columna seleccionada como target."""
        seleccion_target["columna"] = target_var.get()


    def confirmar_seleccion():
        feature = seleccion_feature["columna"]
        target = seleccion_target["columna"]

        if not feature or not target:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, selecciona una columna FEATURE y una columna TARGET antes de confirmar."
            )
            return

        # Confirmación final
        messagebox.showinfo(
            "Selección confirmada",
            f"Feature seleccionada: {feature}\nTarget seleccionada: {target}"
        )

    # Asociaciones
    boton_explorar.config(command=explorar_archivo)
    combo_feature.bind("<<ComboboxSelected>>", seleccionar_feature)
    combo_target.bind("<<ComboboxSelected>>", seleccionar_target)
    boton_confirmar.config(command=confirmar_seleccion)







