from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QDialogButtonBox, QFileDialog, QLabel,QWidget
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import *
from Modelo import *
import pydicom
import numpy as np

class VentanaLogin(QDialog):
    def __init__(self, base_datos, controlador):
        super().__init__()
        loadUi("Login.ui", self)
        self.db = base_datos
        self.controlador = controlador
        self.setup()

    def setup(self):
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.disconnect()
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.disconnect()
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.Aceptar_op)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)

    def Mostrar_mensaje(self, titulo, mensaje):
        """Muestra una ventana con el mensaje entregado"""
        msg = QMessageBox()
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def Aceptar_op(self):
        """Lógica del botón aceptar"""
        usuario = self.lineEdit.text()
        contraseña = self.lineEdit_2.text()
        if self.db.verificar_login(usuario, contraseña):
            self.controlador.Ver_Menu()
            self.close()
        else:
            self.Mostrar_mensaje("Error", "Usuario o contraseña incorrectos")
            self.lineEdit_2.clear()

class VentanaMenu(QMainWindow):
    def __init__(self, base_datos, controlador):
        super().__init__()
        loadUi("Menu.ui", self)
        self.db = base_datos
        self.controlador = controlador
        self.setup()
        self.ventana_ingreso = None
        self.ventana_buscar = None

    def setup(self):
        self.Agregar_Paciente.clicked.connect(self.abrir_ingreso_paciente)
        self.Buscar_Paciente.clicked.connect(self.abrir_buscar_paciente)

    def abrir_ingreso_paciente(self):
        """Abre la ventana para ingresar un nuevo paciente"""
        self.ventana_ingreso = VentanaIngreso(self.controlador, self)
        self.hide()
        self.ventana_ingreso.show()

    def abrir_buscar_paciente(self):
        """Abre la ventana para buscar a un paciente"""
        self.ventana_buscar = VentanaBusqueda(self.controlador)
        self.hide()
        self.ventana_buscar.show()


class VentanaIngreso(QDialog):
    def __init__(self, controlador, ventana_padre=None):
        super().__init__()
        loadUi("Ingreso_Paciente.ui", self)
        self.ventana_padre = ventana_padre
        self.controlador = controlador
        self.setup()

    def setup(self):
        self.pushButton.clicked.connect(self.agregar_eeg)
        self.pushButton_2.clicked.connect(self.agregar_dicom)
        self.pushButton_3.clicked.connect(self.guardar_paciente)
        self.SALIR.clicked.connect(self.regresar_menu)

    def regresar_menu(self):
        """Lógica del botón para salir, regresa al Menú principal"""
        self.close()
        if self.ventana_padre:
            self.ventana_padre.show()

    def agregar_eeg(self):
        """Permite buscar y añadir a la base de datos un archivo EEG"""
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo EEG", "", "Archivos EEG (*.mat)")
        if archivo:
            self.eeg_ruta = archivo

    def agregar_dicom(self):
        """Permite buscar y añadir a la base de datos un archivo DICOM"""
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo DICOM", "", "Archivos DICOM (*.dcm)")
        if archivo:
            self.dicom_ruta = archivo
    def guardar_paciente(self):
        """Guarda los datos ingresados del paciente"""
        try:
            nombre = self.lineEdit.text()
            cedula = int(self.lineEdit_2.text())
            edad = int(self.lineEdit_3.text())
            eeg_ruta = getattr(self, 'eeg_ruta', None)
            dicom_ruta = getattr(self, 'dicom_ruta', None)

            if not all([nombre, cedula, edad, eeg_ruta, dicom_ruta]):
                raise ValueError("Faltan datos obligatorios")

            self.controlador.guardar_paciente(nombre, cedula, edad, eeg_ruta, dicom_ruta)
            QMessageBox.information(self, "Éxito", "Paciente guardado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar paciente: {e}")

class VentanaBusqueda(QDialog):
    def __init__(self, controlador, parent=None):
        super().__init__(parent)
        self.controlador = controlador
        self.setWindowTitle("Buscar Paciente")
        loadUi("Buscar_paciente.ui",self)
        self.setup_ui()

    def setup_ui(self):
        
        self.lineEdit_cedula = self.findChild(QtWidgets.QLineEdit, 'Cedula') 
        self.boton_buscar = self.findChild(QtWidgets.QPushButton, 'boton_buscar')  
        self.boton_buscar.clicked.connect(self.buscar_paciente) 
        
        self.boton_salir = self.findChild(QtWidgets.QPushButton, 'SALIR')  
        self.boton_salir.clicked.connect(self.regresar_menu)  

    def buscar_paciente(self):
        """Busca a un paciente por su cédula y abre la ventana de su información"""

        cedula = self.lineEdit_cedula.text()
        if not cedula:
            self.show_error("Por favor ingrese la cédula.")
            return
        paciente = self.controlador.db.buscar_paciente(cedula)
        print(paciente)
        if paciente:          
            ventana_info = VentanaInformacionPaciente(paciente)
            ventana_info.exec_()  
        else:
            self.show_error("Paciente no encontrado.")

    def show_error(self, mensaje):
        """Muestra un ventana con el mensaje de error asignado"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)  
        msg_box.setWindowTitle("Error")
        msg_box.setText(mensaje)
        msg_box.exec_()  
    def regresar_menu(self):
        """Cierra la ventana y regresa al menú"""
        self.close()
class VentanaInformacionPaciente(QDialog):
    def __init__(self, paciente, parent=None):
        super().__init__(parent)
        loadUi("InformacionPaciente.ui", self)
        self.paciente=paciente
        self.setWindowTitle("Información del Paciente")
        self.setup_ui(paciente)
        
  

    def setup_ui(self, paciente):
        self.NombrePaciente.setText(paciente['Nombre'])
        self.CedulaPaciente.setText(str(paciente['Cedula']))
        self.EdadPaciente.setText(str(paciente['Edad']))
        self.DiagnosticoPaciente.setText(paciente['Diagnostico'])
        self.boton_salir = self.findChild(QtWidgets.QPushButton, 'SALIR')  
        self.boton_salir.clicked.connect(self.regresar_ventana)
        
        dicom_ruta= paciente.get('Ruta_Dicom')
        if dicom_ruta:
            self.cargar_imagen(dicom_ruta)
        else:
            self.ImagenPaciente.clear()

    def regresar_ventana(self):
        """Cierra la ventana"""        
        self.close()


    def cargar_imagen(self, ruta):
        """Convierte imagenes Dicom en imagenes que pueden ser leidas y utilizadas por QtDesigner""" 
        
        if ruta.endswith('.dcm'):
           
            dicom_data = pydicom.dcmread(ruta)
            img_array = dicom_data.pixel_array
            img_array = np.uint8(img_array / np.max(img_array) * 255)  
            height, width = img_array.shape
            qimage = QImage(img_array.data, width, height, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            pixmap = pixmap.scaled(self.ImagenPaciente.size(), QtCore.Qt.KeepAspectRatio)
            self.ImagenPaciente.setPixmap(pixmap)
            self.ImagenPaciente.setAlignment(QtCore.Qt.AlignCenter)
        else:
            pixmap = QPixmap(ruta)
            self.ImagenPaciente.setPixmap(pixmap)
