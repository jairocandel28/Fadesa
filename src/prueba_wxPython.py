#Inicia

import wx

class Ventana(wx.Frame):
    def __init__(self, *args, **kw):
        super(Ventana, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)

        panel.SetBackgroundColour(wx.Colour(220, 220, 220))   # Color del fondo

        # Para ponerle icono a la ventana, no funciona
        """
        bitmap = wx.Bitmap("mi_icono.png", wx.BITMAP_TYPE_PNG)
        icono = wx.Icon()
        icono.CopyFromBitmap(bitmap)
        self.SetIcon(icono)
        """

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Para poner imagen dentor de la ventana, no funciona
        """
        imagen = wx.Bitmap("Fadesa_logo.png", wx.BITMAP_TYPE_PNG)
        img_widget = wx.StaticBitmap(panel, bitmap=imagen)
        vbox.Add(img_widget, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        """

        self.text_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.text_ctrl, flag=wx.EXPAND | wx.ALL, border=10)

        self.boton1 = wx.Button(panel, label='Mostrar lectura')
        vbox.Add(self.boton1, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        self.boton1.Bind(wx.EVT_BUTTON, self.OnBotonLectura)

        self.boton2 = wx.Button(panel, label='Mostrar mensaje')
        vbox.Add(self.boton2, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        self.boton2.Bind(wx.EVT_BUTTON, self.OnBotonMensaje)

        self.boton3 = wx.Button(panel, label='Cerrar programa')
        vbox.Add(self.boton3, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self.boton3.Bind(wx.EVT_BUTTON, self.OnBotonCerrar)

        panel.SetSizer(vbox)

        self.SetTitle('Título')
        self.SetSize((300, 200))
        self.Centre()

    def OnBotonLectura(self, event):
        texto = self.text_ctrl.GetValue()
        wx.MessageBox(f'Ingresaste: {texto}', 'Mensaje Introducido', wx.OK | wx.ICON_INFORMATION)

    def OnBotonMensaje(self, event):
        wx.MessageBox(f'Texto preestablecido por el creador.', 'Mensaje Fijo', wx.OK | wx.ICON_INFORMATION)

    def OnBotonCerrar(self, event):
        self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    ventana = Ventana(None)
    ventana.Show()
    app.MainLoop()



# Pros y contras librería wxPython:

# PROS:
# - Lenguaje simple de utilizar
# - Bastante información en Internet sobre la librería

# CONTRAS:
# - Las interfaces se ven desfasadas por la antigüedad de la librería
# - Problemas a la hora de implementar imágenes a la interfaz