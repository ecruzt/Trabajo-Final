import sys
from PyQt5.QtWidgets import QApplication
from Modelo import DataBase, Paciente

class Controlador:
    def __init__(self):
        # Inicializamos la aplicación y la base de datos
        self.app = QApplication(sys.argv)
        self.db = DataBase(r'C:\Users\VICTUS\Desktop\UdeA\Cuarto Semestre\Informática 2\Trabajo-Final\PacientesDataBase.db')
        self.db.añadir_login()  # Agregamos los datos de login a la base de datos
        self.login = None
        self.menu = None

    def ejecutar(self):
        """Inicia la aplicación mostrando la ventana de login."""
        from Vista import VentanaLogin  # Importamos Vista solo cuando se necesite
        self.login = VentanaLogin(self.db, self)
        self.login.show()
        sys.exit(self.app.exec_())

    def Ver_Menu(self):
        """Abre la ventana del menú principal."""
        from Vista import VentanaMenu  # Importamos Vista solo cuando se necesite
        self.menu = VentanaMenu(self.db, self)
        self.login.close()  # Cerramos la ventana de login al abrir el menú
        self.menu.show()

    def guardar_paciente(self, nombre, cedula, edad, eeg_ruta, dicom_ruta, diagnostico):
        """Guarda un paciente en la base de datos."""
        try:
            paciente = Paciente(cedula, nombre, edad, eeg_ruta, dicom_ruta, diagnostico)
            self.db.añadir_paciente(paciente)
        except Exception as e:
            print(f"Error al guardar el paciente: {e}")

    def abrir_buscar_paciente(self):
        """Abre la ventana para buscar pacientes."""
        from Vista import VentanaBusqueda  # Importamos Vista solo cuando se necesite
        ventana_buscar = VentanaBusqueda(self)
        ventana_buscar.show()


if __name__ == "__main__":
    controlador = Controlador()
    controlador.ejecutar()
