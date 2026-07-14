#Copyright (c) 2026 Daniel Alejandro Ramirez Palma. Todos los derechos reservados.
#Este software es propiedad intelectual privada. Prohibida su copia, distribución o ingeniería inversa sin autorización expresa del autor.
import pandas as pd

class LibroDiario:
    """Contiene la lógica de negocio para gestionar los asientos contables."""
    
    def __init__(self, bd):
        self.bd = bd

    def registrar_asiento(self, fecha, descripcion, lineas):
        total_debe = round(sum(linea['debe'] for linea in lineas), 2)
        total_haber = round(sum(linea['haber'] for linea in lineas), 2)

        if total_debe != total_haber:
            raise ValueError(f"Error de Partida Doble: El Debe ({total_debe}) no cuadra con el Haber ({total_haber}).")

        if total_debe == 0 and total_haber == 0:
            raise ValueError("El asiento no puede tener valor cero.")

        # Creamos un cursor exclusivo para esta transacción
        cursor = self.bd.conexion.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            cursor.execute(
                "INSERT INTO asientos (fecha, descripcion) VALUES (?, ?)", 
                (fecha, descripcion)
            )
            id_asiento = cursor.lastrowid
            
            for linea in lineas:
                cursor.execute('''
                    INSERT INTO lineas_asiento (id_asiento, codigo_cuenta, nombre_cuenta, debe, haber)
                    VALUES (?, ?, ?, ?, ?)
                ''', (id_asiento, linea['codigo'], linea['nombre'], linea['debe'], linea['haber']))
            
            self.bd.conexion.commit()
            
        except Exception as e:
            self.bd.conexion.rollback()
            raise RuntimeError(f"Error al guardar en la base de datos: {e}")

    def obtener_registros(self, filtro_tiempo="7 days"):
        """Devuelve los registros filtrados por tiempo para no saturar la memoria."""
        query = f'''
            SELECT a.fecha, a.id_asiento, a.descripcion, l.codigo_cuenta, l.nombre_cuenta, l.debe, l.haber
            FROM asientos a
            JOIN lineas_asiento l ON a.id_asiento = l.id_asiento
            WHERE a.fecha >= date('now', '-{filtro_tiempo}')
            ORDER BY a.fecha, a.id_asiento, l.id_linea
        '''
        # Este cursor se ejecutará de forma segura en el hilo de segundo plano
        cursor = self.bd.conexion.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def obtener_saldos(self):
        """Devuelve los totales del libro diario."""
        cursor = self.bd.conexion.cursor()
        cursor.execute("SELECT SUM(debe), SUM(haber) FROM lineas_asiento")
        totales = cursor.fetchone()
        total_debe = totales[0] if totales[0] else 0.0
        total_haber = totales[1] if totales[1] else 0.0
        return total_debe, total_haber
    
    def exportar_a_excel(self, ruta_archivo):
        """Convierte los registros de la base de datos en un archivo Excel profesional."""
        datos = self.obtener_registros()
        
        columnas = [
            'Fecha', 'ID Asiento', 'Descripción General', 
            'Código Cuenta', 'Nombre Cuenta', 'Debe', 'Haber'
        ]
        
        df = pd.DataFrame(datos, columns=columnas)
        df['Debe'] = df['Debe'].replace(0, '')
        df['Haber'] = df['Haber'].replace(0, '')
        
        df.to_excel(ruta_archivo, index=False, engine='openpyxl')