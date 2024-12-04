import sys
from PyQt5.QtWidgets import QApplication
from Modelo import *
from Vista import *

class Controlador:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = DataBase('PacientesDataBase.db')
        self.db.añadir_login()
        self.login = VentanaLogin(self.db,self)
        
    def ejecutar(self):
        self.login.show()
        self.app.exec_()
    def Ver_Menu(self):
        self.Ventana_Menu= VentanaMenu(self.db)
        self.Ventana_Menu.show()
    def guardar_paciente(self, nombre, cedula, edad, eeg_ruta, dicom_ruta, diagnostico):
        paciente = Paciente(cedula, nombre, edad, eeg_ruta, dicom_ruta, diagnostico)
        self.db.añadir_paciente(paciente)

if __name__=="__main__":
    controlador=Controlador()
    controlador.ejecutar()