from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow,QDialog,QMessageBox,QDialogButtonBox,QFileDialog
from Modelo import*
class VentanaLogin(QDialog):
    def __init__(self,base_datos,controlador):
        super().__init__()
        loadUi("Login.ui",self)
        self.db=base_datos
        self.controlador=controlador
        self.setup()
    def setup(self):
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.disconnect()
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.disconnect()
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.Aceptar_op)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)
    def Mostrar_mensaje(self,titulo,mensaje):
        msg=QMessageBox()
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def Aceptar_op(self):
        usuario=self.lineEdit.text()
        contraseña=self.lineEdit_2.text()
        if self.db.verificar_login(usuario,contraseña):
            self.controlador.Ver_Menu()
            self.close()
        else:
            self.Mostrar_mensaje("Error","Usuario o contraseña incorrectos")
            self.lineEdit_2.clear()


class VentanaMenu(QMainWindow):
    def __init__(self, base_datos,controlador):
        super().__init__()
        loadUi("Menu.ui",self)
        self.db = base_datos
        self.controlador=controlador
        self.setup()
        self.ventana_ingreso = None
        self.ventana_buscar = None

    def setup(self):
        self.pushButton.clicked.connect(self.abrir_ingreso_paciente)
        self.Ventana_Menu.clicked.connect(self.abrir_buscar_paciente)

    def abrir_ingreso_paciente(self):
        self.ventana_ingreso = VentanaIngreso(self.controlador,self)
        self.hide()  
        self.ventana_ingreso.show()

    def abrir_buscar_paciente(self):
        self.ventana_buscar = VentanaBusqueda(self)
        self.hide()  
        self.ventana_buscar.show()


class VentanaIngreso(QDialog):
    def __init__(self,controlador,ventana_padre=None):
        super().__init__()
        loadUi("Ingreso_Paciente.ui",self)
        self.ventana_padre = ventana_padre
        self.controlador=controlador
        self.setup()

    def setup(self):
        self.pushButton.clicked.connect(self.agregar_eeg)
        self.pushButton_2.clicked.connect(self.agregar_dicom)
        self.pushButton_3.clicked.connect(self.guardar_paciente)
        self.SALIR.clicked.connect(self.regresar_menu)

    def regresar_menu(self):
        self.close()  
        if self.ventana_padre:
            self.ventana_padre.show() 
    
    def agregar_eeg(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo EEG", "", "Archivos EEG (*.mat)")
        if archivo:
            self.eeg_ruta = archivo
            # self.lineEdit.setText(archivo)
    def agregar_dicom(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo DICOM", "", "Archivos DICOM (*.dcm)")
        if archivo:
            self.dicom_ruta = archivo
            # self.lineEdit_2.setText(archivo)
    def guardar_paciente(self):
    #     nombre = self.NombrePaciente.text()
    #     cedula = self.CedulaPaciente.text()
    #     edad = self.EdadPaciente.text()
    #     eeg_ruta = self.lineEdit.text()
    #     dicom_ruta = self.lineEdit_2.text()
    #     diagnostico = self.DiagnosticoPaciente.text()
    #     self.controlador.guardar_paciente(nombre, cedula, edad, eeg_ruta, dicom_ruta, diagnostico)
        nombre = self.lineEdit.text() 
        cedula = int(self.lineEdit_2.text())  
        edad = int(self.lineEdit_3.text())  
        eeg_ruta = getattr(self, 'eeg_ruta', None)
        dicom_ruta = getattr(self, 'dicom_ruta', None) 
        
        if not all([nombre, cedula, edad, eeg_ruta, dicom_ruta]):
            raise ValueError("Faltan datos obligatorios")

        self.controlador.guardar_paciente(nombre, cedula, edad, eeg_ruta, dicom_ruta, None)
        # self.label_4.setText("Paciente guardado exitosamente.")


class VentanaBusqueda(QDialog):
    def __init__(self, ventana_padre=None):
        super().__init__()
        loadUi("Buscar_paciente.ui",self)
        self.ventana_padre = ventana_padre
        self.setup()

    def setup(self):
       
        self.SALIR.clicked.connect(self.regresar_menu)

    def regresar_menu(self):
        self.close()
        if self.ventana_padre:
            self.ventana_padre.show()  
