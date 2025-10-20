import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout

class VentanaSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setGeometry(400, 100,700, 300)
        layout = QVBoxLayout()
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Escribe tu nombre")
        boton = QPushButton("Enviar")
        boton.clicked.connect(self.mostrar_mensaje)
        layout.addWidget(QLabel("Escribe tu nombre:"))
        layout.addWidget(self.entrada)
        layout.addWidget(boton)
        self.setLayout(layout)
    
    def mostrar_mensaje(self):
        texto = self.entrada.text()
        if texto:
            QMessageBox.information(self,'', f"Hola! {texto}")
        else:
            QMessageBox.warning(self, "Error", "Escribe algo primero")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaSimple()
    ventana.show()
    sys.exit(app.exec())