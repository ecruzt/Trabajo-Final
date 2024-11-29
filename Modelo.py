import sqlite3
class Paciente:
    def __init__(self,cedula,nombre,edad,EEG,DICOM,Diag):
        self.cedula=cedula
        self.nombre=nombre
        self.edad=edad
        self.EEG=EEG
        self.Dicom=DICOM
        self.Diag=Diag
        
class DataBase:
    def __init__(self,nombre_archivo):
        self.nombre_archivo=nombre_archivo
        self.conexion=sqlite3.connect(nombre_archivo)
        self.cursor=self.conexion.cursor()
        self.crear_tabla_login()
        self.crear_tabla_pacientes()
        self.Tablas_vacias()

    def crear_tabla_login(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                                Usuario TEXT,
                                Contraseña INTEGER
                            )''')
        self.conexion.commit()
    def crear_tabla_pacientes(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
                                Cedula INTEGER,
                                Nombre TEXT,
                            Edad INTEGER,
                            Ruta_EEG TEXT,
                            Ruta_Dicom TEXT,
                            Diagnostico TEXT                                
                            )''')
        self.conexion.commit() 
    def Tablas_vacias(self,tabla):
        self.cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        espacio = self.cursor.fetchone()[0]
        return espacio == 0
    def añadir_login(self):
        if self.Tablas_vacias("Usuarios"):
            sql_insert_users = """INSERT  INTO  Usuarios (Usuario, Contraseña)  
                  VALUES (?,?)"""

            val_users = [
            ('Maria','123'),
            ('Felipe','123'),
            ('Jhonny','123'),
            ('Camila','123'),
            ('Kate','123')
            ]
            self.cursor.executemany(sql_insert_users, val_users)
            self.conexion.commit()
    def añadir_paciente(self,paciente):
        self.cursor.execute('''INSERT INTO pacientes 
                                (Cedula, nombre, edad, Ruta_EEG,Ruta_Dicom,Diagnostico)
                                VALUES (?, ?, ?, ?, ?,?)''',
                            (paciente.cedula, paciente.nombre, paciente.edad,
                             paciente.EEG, paciente.DICOM,paciente.Diag))
        self.conexion.commit()

    




        
