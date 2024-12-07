import sys
from PyQt5.QtWidgets import QApplication
from Modelo import DataBase, Paciente

class Controlador:
    def __init__(self):

        self.app = QApplication(sys.argv)
        self.db = DataBase("PacientesDataBase.db")
        self.db.añadir_login() 
        self.login = None
        self.menu = None

    def ejecutar(self):
        """Inicia la aplicación mostrando la ventana de login."""
        from Vista import VentanaLogin  
        self.login = VentanaLogin(self.db, self)
        self.login.show()
        sys.exit(self.app.exec_())

    def Ver_Menu(self):
        """Abre la ventana del menú principal."""
        from Vista import VentanaMenu 
        self.menu = VentanaMenu(self.db, self)
        self.login.close() 
        self.menu.show()

    def guardar_paciente(self, nombre, cedula, edad, eeg_ruta, dicom_ruta,diagnostico=None):
        """Guarda un paciente en la base de datos."""
        try:
            paciente = Paciente(cedula, nombre, edad, eeg_ruta, dicom_ruta)
            if diagnostico is None:
                paciente.diag=paciente.diagnosticar()
            else:
                paciente.Diag=diagnostico
            self.db.añadir_paciente(paciente)
                          
        except Exception as e:
            print(f"Error al guardar el paciente: {e}")

    def abrir_buscar_paciente(self):
        """Abre la ventana para buscar pacientes."""
        from Vista import VentanaBusqueda  
        ventana_buscar = VentanaBusqueda(self)
        ventana_buscar.show()


if __name__ == "__main__":
    controlador = Controlador()
    controlador.ejecutar()
