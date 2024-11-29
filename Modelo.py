import sqlite3

class DataBase:
    def __init__(self,nombre_archivo):
        self.nombre_archivo=nombre_archivo
        self.conexion=sqlite3.connect(nombre_archivo)
        self.cursor=self.conexion.cursor()
        self.crear_tabla_login()
        self.crear_tabla_pacientes()

    def crear_tabla_login(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                                Usuario TEXT,
                                Contraseña INTEGER,
                            )''')
        self.conexion.commit()
    def crear_tabla_pacientes(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
                                Cedula INTEGER,
                                Nombre TEXT,
                                
                            )''')
        self.conexion.commit() 
    




        
