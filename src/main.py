from interfaz_grafica import *



if __name__ == "__main__":

    ventana = tk.Tk()
    ventana.title("-- VENTANA PRINCIPAL --")
    ventana.state("zoomed")

    pantalla_principal(ventana)
    ventana.mainloop()
