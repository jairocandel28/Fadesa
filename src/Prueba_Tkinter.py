
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk


# Crear ventana principal
ventana = tk.Tk()
ventana.title("-- VENTANA PRINCIPAL --")
ventana.geometry("300x200")


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


# Crear una etiqueta
etiqueta = tk.Label(ventana, text="¡Hola desde Tkinter!", font=("Arial", 14))
etiqueta.pack(pady=20)

# Crear un botón
def saludar():
    messagebox.showinfo("Saludo", "¡Hola, usuario!")

boton = tk.Button(ventana, text="Saludar", command=saludar)
boton.pack()

# Iniciar el bucle principal
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
"""
