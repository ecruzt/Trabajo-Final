import sys
from PyQt5.Qtwidgets import QApplication
from modelo import *
from vista import *

class Controlador:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.base_datos = DataBase('')
        self.vista = VentanaPrincipal(self.base_datos)
        self.conectar_eventos()
        self.vista.cargar_pacientes()
