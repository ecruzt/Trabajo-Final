from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow,QDialog
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
        self.ventana_ingreso = None
        self.ventana_buscar=None
    def setup(self):
        self.pushButton.clicked.connect(self.abrir_ingreso_paciente)
        self.Ventana_Menu.clicked.connect(self.abrir_buscar_paciente)
    def abrir_ingreso_paciente(self):
        self.ventana_ingreso=VentanaIngreso(self)
        self.hide()
        self.ventana_ingreso.show()
    def abrir_buscar_paciente(self):
        self.ventana_buscar=VentanaBusqueda(self)
        self.hide()
        self.ventana_buscar.show()
class VentanaIngreso(QDialog):
    def __init__(self,ventana_padre=None):
        super().__init__()
        loadUi("Ingreso_Paciente.ui",self)
        self.ventana_padre=ventana_padre
        self.setup()
    def setup(self):
        pass

class VentanaBusqueda(QDialog):
    def __init__(self,ventana_padre=None):
        super().__init__()
        loadUi("Buscar_paciente.ui",self)
        self.ventana_padre=ventana_padre
