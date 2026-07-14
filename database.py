#Copyright (c) 2026 Daniel Alejandro Ramirez Palma. Todos los derechos reservados.
#Este software es propiedad intelectual privada. Prohibida su copia, distribución o ingeniería inversa sin autorización expresa del autor.
import sqlite3 

class BaseDatosContable:
    """Maneja la conexión y la estructura de la base de datos SQLite."""
    
    def __init__(self, db_name="contabilidad.db"):
        # check_same_thread=False le permite a SQLite trabajar con hilos en segundo plano
        self.conexion = sqlite3.connect(db_name, check_same_thread=False)
        self._crear_tablas()

    def _crear_tablas(self):
        """Crea las tablas relacionales para el Libro Diario si no existen."""
        cursor = self.conexion.cursor() # Cursor local temporal
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asientos (
                id_asiento INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lineas_asiento (
                id_linea INTEGER PRIMARY KEY AUTOINCREMENT,
                id_asiento INTEGER,
                codigo_cuenta TEXT NOT NULL,
                nombre_cuenta TEXT NOT NULL,
                debe REAL DEFAULT 0.0,
                haber REAL DEFAULT 0.0,
                FOREIGN KEY(id_asiento) REFERENCES asientos(id_asiento)
            )
        ''')
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()