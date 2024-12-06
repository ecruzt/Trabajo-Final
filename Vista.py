from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QDialogButtonBox, QFileDialog, QLabel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from Modelo import *
import pydicom
from pydicom.pixel_data_handlers.util import apply_windowing
from PyQt5.QtGui import QImage
class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        from Controlador import Controlador
        self.controlador = Controlador()  # Instancia de tu controlador
        loadUi("MainWindow.ui", self)
        
        # Conectar el botón de "Buscar Paciente" con la función correspondiente
        self.Buscar_Paciente.clicked.connect(self.abrir_buscar_paciente)

    def abrir_buscar_paciente(self):
        self.ventana_buscar = VentanaBusqueda(self.controlador)
        self.ventana_buscar.show()

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
        msg = QMessageBox()
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def Aceptar_op(self):
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
        # Conectar el botón de "Agregar Paciente"
        self.Agregar_Paciente.clicked.connect(self.abrir_ingreso_paciente)
        
        # Conectar el botón de "Buscar Paciente"
        self.Buscar_Paciente.clicked.connect(self.abrir_buscar_paciente)

    def abrir_ingreso_paciente(self):
        self.ventana_ingreso = VentanaIngreso(self.controlador, self)
        self.hide()
        self.ventana_ingreso.show()

    def abrir_buscar_paciente(self):
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
        self.close()
        if self.ventana_padre:
            self.ventana_padre.show()

    def agregar_eeg(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo EEG", "", "Archivos EEG (*.mat)")
        if archivo:
            self.eeg_ruta = archivo

    def agregar_dicom(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo DICOM", "", "Archivos DICOM (*.dcm)")
        if archivo:
            self.dicom_ruta = archivo

    def guardar_paciente(self):
        try:
            nombre = self.lineEdit.text()
            cedula = int(self.lineEdit_2.text())
            edad = int(self.lineEdit_3.text())
            eeg_ruta = getattr(self, 'eeg_ruta', None)
            dicom_ruta = getattr(self, 'dicom_ruta', None)

            if not all([nombre, cedula, edad, eeg_ruta, dicom_ruta]):
                raise ValueError("Faltan datos obligatorios")

            self.controlador.guardar_paciente(nombre, cedula, edad, eeg_ruta, dicom_ruta, None)
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
        # Cargar los elementos de la interfaz
        self.lineEdit_cedula = self.findChild(QtWidgets.QLineEdit, 'Cedula')  # QLineEdit para ingresar la cédula
        self.boton_buscar = self.findChild(QtWidgets.QPushButton, 'boton_buscar')  # Botón para buscar
        self.boton_buscar.clicked.connect(self.buscar_paciente)  # Conectar la acción de búsqueda
        
        self.boton_salir = self.findChild(QtWidgets.QPushButton, 'SALIR')  # Botón para salir
        self.boton_salir.clicked.connect(self.regresar_menu)  # Conectar la acción de salir

    def buscar_paciente(self):
        # Obtener la cédula ingresada
        cedula = self.lineEdit_cedula.text()

        # Verificar que la cédula no esté vacía
        if not cedula:
            self.show_error("Por favor ingrese la cédula.")
            return

        # Buscar el paciente en la base de datos utilizando la cédula
        paciente = self.controlador.db.buscar_paciente(cedula)

        if paciente:
            # Si se encuentra al paciente, mostrar la ventana con su información
            ventana_info = VentanaInformacionPaciente(paciente)
            ventana_info.exec_()  # Mostrar la ventana de información del paciente
        else:
            # Si no se encuentra al paciente, mostrar un mensaje de error
            self.show_error("Paciente no encontrado.")

    def show_error(self, mensaje):
        # Mostrar el mensaje de error
        error_label = QLabel(mensaje)
        self.layout().addWidget(error_label)  # Añadir el mensaje al layout de la ventana

    def regresar_menu(self):
        # Cerrar la ventana actual y regresar al menú
        self.close()


class VentanaInformacionPaciente(QDialog):
    def __init__(self, paciente, parent=None):
        super().__init__(parent)
        loadUi("InformacionPaciente.ui", self)
        self.setWindowTitle("Información del Paciente")
        self.setup_ui(paciente)

    def setup_ui(self, paciente):
        self.NombrePaciente.setText(paciente['Nombre'])
        self.CedulaPaciente.setText(str(paciente['Cedula']))
        self.EdadPaciente.setText(str(paciente['Edad']))
        self.DiagnosticoPaciente.setText(paciente['Diagnostico'])
        
        if paciente.get('Ruta_Dicom'):
            pixmap = QPixmap(paciente['Ruta_Dicom'])
            self.ImagenPaciente.setPixmap(pixmap)
        else:
            self.ImagenPaciente.clear()
    def cargar_imagen(self,ruta):
        if ruta.endswith('.dcm'):
            # Cargar el archivo DICOM usando pydicom
            dicom_data = pydicom.dcmread(ruta)
            
            # Acceder a la imagen (en formato numpy array)
            img_array = dicom_data.pixel_array
            
            # Normalizar la imagen si es necesario
            img_array = np.uint8(img_array / np.max(img_array) * 255)  # Normaliza la imagen

            # Convertir a imagen compatible con QPixmap
            height, width = img_array.shape
            qimage = QImage(img_array.data, width, height, QImage.Format_Grayscale8)
            
            # Crear el QPixmap y mostrar la imagen
            pixmap = QPixmap.fromImage(qimage)
            self.ImagenPaciente.setPixmap(pixmap)
        else:
            # Si no es DICOM, tratar como imagen estándar
            pixmap = QPixmap(ruta)
            self.ImagenPaciente.setPixmap(pixmap)