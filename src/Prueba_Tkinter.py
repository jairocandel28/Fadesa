
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

from lector import *


# -----------------------------
# Función para limpiar ventana
# -----------------------------
def limpiar_ventana():
    for widget in ventana.winfo_children():
        widget.destroy()



def pantalla_inicio():
    limpiar_ventana()
    # Crear una etiqueta
    etiqueta = tk.Label(ventana, text="¡Hola desde Tkinter!", font=("Arial", 14))
    etiqueta.pack(pady=10)

    # Nueva etiqueta para el cuadro de texto
    etiqueta_nombre = tk.Label(ventana, text="Introduce tu nombre:")
    etiqueta_nombre.pack()

    # Cuadro de texto (entrada de usuario)
    entrada = tk.Entry(ventana, width=30)
    entrada.pack(pady=5)

    # Función del botón para saludar
    def saludar():
        nombre = entrada.get().strip()  # Obtener texto del cuadro de texto
        if nombre.strip() == "":
            messagebox.showwarning("Advertencia", "Por favor, introduce tu nombre.")
        else:
            messagebox.showinfo("Saludo", f"¡Hola, {nombre}. Redirigiéndote al menú...")
            menu(nombre) # Cambiamos al menú

    boton = tk.Button(ventana, text = "Saludar", command=saludar)
    boton.pack(pady=10)




# -----------------------------
# Pantalla para introducir datos
# -----------------------------
def pantalla_analizar_archivo():
    limpiar_ventana()

    etiqueta = tk.Label(ventana, text="Selecciona el archivo que quieras cargar:", font=("Arial", 14))
    etiqueta.pack(pady=10)

    ruta_var = tk.StringVar(value="Ningúan archivo seleccionado")

    etiqueta_ruta = tk.Label(ventana, textvariable=ruta_var, wraplength=400, justify="center", fg="blue")
    etiqueta_ruta.pack(pady=5)

    # Frame para tabla
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10, fill="both", expand=True)

    # Función para abrir explorador de archivos
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

    # Función para mostrar datos del archivo
    def mostrar_datos(ruta):
        # Limpia la tabla anterior si existe
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        try:
            datos = leer_archivo(ruta)

            if datos is None or datos.empty:
                messagebox.showwarning("Archivo vacío", "El archivo no contiene datos o no fue posible cargarlos.")
                return
            
            # Para crear la tabla gráficamente
            columnas = list(datos.columns)
            tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

            # Encabezados
            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=100, anchor="center")

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

    # Botones
    boton_explorar = tk.Button(ventana, text="Explorar archivo", command=explorar_archivo)
    boton_explorar.pack(pady=5)

    boton_volver = tk.Button(ventana, text="Volver al menú", command=lambda: menu("Usuario"))
    boton_volver.pack(pady=10)    

# -----------------------------
# Pantalla de menú
# -----------------------------
def menu(nombre):
    limpiar_ventana()

    etiqueta = tk.Label(ventana, text=f"Bienvenido, {nombre}. ¿Que deseas hacer?", font=("Arial", 14))
    etiqueta.pack(pady=10)

    # Botón para ir a introducir datos
    boton_datos = tk.Button(ventana, text="Introducir un archivo (.csv, .db, .xlsx)", command=pantalla_analizar_archivo)
    boton_datos.pack(pady=10)

    # Botón para volver al inicio
    boton_volver = tk.Button(ventana, text="Cerrar sesión", command=pantalla_inicio)
    boton_volver.pack(pady=10)
    





if __name__ == "__main__":

    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("-- VENTANA PRINCIPAL --")
    ventana.geometry("500x300")

    pantalla_inicio()
    ventana.mainloop()





"""
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from lector import *

def seleccionar_archivo():
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los soportados", "*.csv *.xlsx *.db"),
                   ("CSV", "*.csv"),
                   ("Excel", "*.xlsx"),
                   ("Base de datos", "*.db")]
    )
    if ruta:
        datos = leer_archivo(ruta)
        messagebox.showinfo("Resultado", f"Archivo leído correctamente: {ruta}")
    else:
        messagebox.showwarning("Atención", "No se seleccionó ningún archivo.")

ventana = tk.Tk()
ventana.title("Lector de archivos")
tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack(padx=20, pady=20)
ventana.mainloop()






### IMAGEN ###

# Cargar la imagen usando PIL
imagen = Image.open("C:/Users/ander/Downloads/el_bich.jpg")  
imagen_tk = ImageTk.PhotoImage(imagen)

# Crear un label para mostrar la imagen
label_imagen = tk.Label(ventana, image=imagen_tk)
label_imagen.pack()

# Mostrar la ventana
ventana.mainloop()


### FIN IMAGEN ###
"""
