
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from lector import *


def limpiar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()


def pantalla_principal(ventana):
    limpiar_ventana(ventana)
    ventana.title("Visor de Archivos")

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

    frame_tabla = tk.Frame(ventana, bd=2, relief="groove")
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)


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
        # Limpiar tabla anterior
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

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el archivo:\n{e}")

    boton_explorar.config(command=explorar_archivo)








