import sqlite3
import numpy as np
from scipy.io import loadmat
import pydicom

class Paciente:
    def __init__(self, cedula, nombre, edad, EEG, DICOM, Diag=None):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.EEG = EEG 
        self.DICOM = DICOM  
        self.Diag = Diag  
        self.thresholds = {
            'alpha': 25,
            'theta': 25, 
            'delta': 35,  
            'hippocampus': 4500  
        }

    def procesar_eeg(self):
        try:
            data = loadmat(self.EEG)
            eeg_data = data['EEG']  

            fs = 256  
            freqs = np.fft.rfftfreq(eeg_data.shape[1], d=1/fs)
            fft_values = np.abs(np.fft.rfft(eeg_data, axis=1))**2

            alpha_power = np.sum(fft_values[:, (freqs >= 8) & (freqs <= 12)], axis=1)
            beta_power = np.sum(fft_values[:, (freqs >= 13) & (freqs <= 30)], axis=1)
            theta_power = np.sum(fft_values[:, (freqs >= 4) & (freqs <= 7)], axis=1)
            delta_power = np.sum(fft_values[:, (freqs >= 0.5) & (freqs <= 3)], axis=1)

            total_power = alpha_power + beta_power + theta_power + delta_power

            return {
                'alpha_mean': np.mean(alpha_power / total_power) * 100,
                'beta_mean': np.mean(beta_power / total_power) * 100,
                'theta_mean': np.mean(theta_power / total_power) * 100,
                'delta_mean': np.mean(delta_power / total_power) * 100,
            }
        except Exception as e:
            print(f"Error procesando EEG: {e}")
            return None

    def procesar_dicom(self, threshold_percentile=90):
        try:
            dicom_data = pydicom.dcmread(self.DICOM)
            pixel_array = dicom_data.pixel_array
            
            hipocampo_coords = (0, pixel_array.shape[0], 0, pixel_array.shape[1])
            x_min, x_max, y_min, y_max = hipocampo_coords
            hipocampo_region = pixel_array[x_min:x_max, y_min:y_max]

            threshold = np.percentile(hipocampo_region, threshold_percentile)
            hipocampo_segment = hipocampo_region > threshold

            estimated_volume = np.sum(hipocampo_segment)
            return estimated_volume
        except Exception as e:
            print(f"Error procesando DICOM: {e}")
            return None

    def diagnosticar(self):
        eeg_features = self.procesar_eeg()
        print(f"Características del EEG: {eeg_features}")
        hippocampus_volume = self.procesar_dicom()
        print(f"Volumen del hipocampo: {hippocampus_volume}")

        if eeg_features is None or hippocampus_volume is None:
            self.Diag = "Datos insuficientes para diagnóstico"
        else:
            alpha_threshold = self.thresholds['alpha']
            theta_threshold = self.thresholds['theta']
            delta_threshold = self.thresholds['delta']
            hippocampus_threshold = self.thresholds['hippocampus']

            if (eeg_features['alpha_mean'] < alpha_threshold and
                eeg_features['theta_mean'] > theta_threshold and
                eeg_features['delta_mean'] > delta_threshold and
                hippocampus_volume < hippocampus_threshold):
                self.Diag = "Posible Alzheimer"
            else:
                self.Diag = "No Alzheimer"

        return self.Diag


class DataBase:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        try:
            self.conexion = sqlite3.connect(nombre_archivo)
            self.cursor = self.conexion.cursor()
            self.crear_tabla_login()
            self.crear_tabla_pacientes()
        except sqlite3.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            self.conexion = None
            self.cursor = None

    def crear_tabla_login(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                                    Usuario TEXT,
                                    Contraseña INTEGER
                                )''')
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de login: {e}")

    def crear_tabla_pacientes(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
                                    Cedula INTEGER,
                                    Nombre TEXT,
                                    Edad INTEGER,
                                    Ruta_EEG TEXT,
                                    Ruta_Dicom TEXT,
                                    Diagnostico TEXT
                                )''')
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de pacientes: {e}")

    def Tablas_vacias(self, tabla):
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            espacio = self.cursor.fetchone()[0]
            return espacio == 0
        except sqlite3.Error as e:
            print(f"Error al verificar si la tabla {tabla} está vacía: {e}")
            return False

    def añadir_login(self):
        try:
            if self.Tablas_vacias("Usuarios"):
                sql_insert_users = """INSERT INTO Usuarios (Usuario, Contraseña)  
                                      VALUES (?, ?)"""
                val_users = [
                    ('Maria', '123'),
                    ('Felipe', '123'),
                    ('Jhonny', '123'),
                    ('Camila', '123'),
                    ('Kate', '123')
                ]
                self.cursor.executemany(sql_insert_users, val_users)
                self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al añadir usuarios de login: {e}")

    def añadir_paciente(self, paciente):
        try:
            self.cursor.execute('''INSERT INTO Pacientes 
                                    (Cedula, Nombre, Edad, Ruta_EEG, Ruta_Dicom, Diagnostico)
                                    VALUES (?, ?, ?, ?, ?, ?)''',
                                (paciente.cedula, paciente.nombre, paciente.edad,
                                 paciente.EEG, paciente.DICOM, paciente.Diag))
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al añadir paciente: {e}")

    def verificar_login(self, user, passw):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE Usuario = ? AND Contraseña = ?", (user, passw))
            result = self.cursor.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print(f"Error al verificar login: {e}")
            return False

    def buscar_paciente(self, cedula):
        try:
            self.cursor.execute("SELECT * FROM Pacientes WHERE Cedula = ?", (cedula,))
            paciente = self.cursor.fetchone()
            if paciente:
                return {
                    'Cedula': paciente[0],        
                    'Nombre': paciente[1],       
                    'Edad': paciente[2],         
                    'Ruta_EEG': paciente[3],     
                    'Ruta_Dicom': paciente[4],   
                    'Diagnostico': paciente[5],  
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al buscar paciente: {e}")
            return None
