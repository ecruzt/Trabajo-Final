import sys
from PyQt5.Qtwidgets import QApplication
from Modelo import *
from Vista import *

class Controlador:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = DataBase('PacientesDataBase.db')
        # self.conectar_eventos()
        # self.vista.cargar_pacientes()
        self.db.añadir_login()
        self.login = VentanaLogin(self.db,self)
        
    def ejecutar(self):
        self.login.show()
        self.app.exec_()
    def Ver_Menu(self):
        self.VentanaMenu= VentanaMenu(self.db)
        self.VentanaMenu.show()


