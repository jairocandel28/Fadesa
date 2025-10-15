from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título
        self.label = Label(text="¡Hola! Ingresa tu nombre abajo:")

        # Cuadro de texto
        self.text_input = TextInput(hint_text="Escribe aquí...")

        # Botón
        self.button = Button(text="Saludar")
        self.button.bind(on_press=self.mostrar_mensaje)

        # Mensaje de salida
        self.output = Label(text="")

        # Agregar widgets al layout
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(self.button)
        layout.add_widget(self.output)

        return layout

    def mostrar_mensaje(self, instance):
        nombre = self.text_input.text
        self.output.text = f"¡Hola, {nombre}!"

# Ejecutar la aplicación
if __name__ == "__main__":
    MyApp().run()
