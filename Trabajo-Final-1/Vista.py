from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow,QDialog,QFileDialog 
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
        self.pushButton.clicked.connect(self.añadir_egg)
        self.pushButton_2.clicked.connect(self.añadir_dicom)
        self.pushButton_3.clicked.connect(self.guardar_paciente)

    def añadir_egg(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo EEG", "", "Archivos EEG (*.egg)")
        if archivo:
            self.lineEdit.setText(archivo)
    def añadir_dicom(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo DICOM", "", "Archivos DICOM (*.dcm)")
        if archivo:
            self.lineEdit_2.setText(archivo)
    def guardar_paciente(self):
        nombre = self.NombrePaciente.text()
        cedula = self.CedulaPaciente.text()
        edad = self.EdadPaciente.text()
        eeg_ruta = self.lineEdit.text()
        dicom_ruta = self.lineEdit_2.text()
        diagnostico = self.DiagnosticoPaciente.text()
        self.controlador.guardar_paciente(nombre, cedula, edad, eeg_ruta, dicom_ruta, diagnostico)
class VentanaBusqueda(QDialog):
    def __init__(self,ventana_padre=None):
        super().__init__()
        loadUi("Buscar_paciente.ui",self)
        self.ventana_padre=ventana_padre
