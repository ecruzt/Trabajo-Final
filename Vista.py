from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog
from Modelo import*
class VentanaLogin(QDialog):
    def __init__(self,base_datos,controlador):
        super().__init__()
        loadUi("Login.ui",self)
        self.db=base_datos
        self.controlador=controlador
        self.setup()
    def setup(self):
        self.buttonBox.accepted.connect(self.Aceptar_op)
        self.buttonBox.rejected.connect(self.Cancelar_op)
    def Aceptar_op(self):
        usuario=self.lineEdit.text()
        contraseña=self.lineEdit_2.text()
        if self.db.verificar_login(usuario,contraseña):
            self.controlador.Ver_Menu()
            self.close()
        else:
            pass
    def Cancelar_op(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

class VentanaMenu(QMainWindow):
    def __init__(self,base_datos):
        super().__init__()
        loadUi("Menu.ui",self)
        self.db=base_datos
        self.setup()
    def setup(self):
        self.Agregar_paciente.clicked.connect(self.abrir_ingreso_paciente)
        self.Buscar_paciente.clicked.connect(self.abrir_buscar_paciente)
    def abrir_ingreso_paciente(self):
        ventana_ingreso=VentanaIngreso(self)
        self.hide()
        ventana_ingreso.show()
    def abrir_buscar_paciente(self):
        ventana_buscar=VentanaBusqueda(self)
        self.hide()
        ventana_buscar.show()
class VentanaIngreso(QDialog):
    def __init__(self):
        super().__init__(self)
        loadUi("Ingreso_Paciente.ui",self)
class VentanaBusqueda(QDialog):
    def __init__(self):
        super().__init__(self)
        loadUi("Buscar_paciente.ui",self)





    