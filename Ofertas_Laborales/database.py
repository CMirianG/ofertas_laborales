import pyodbc
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from config import Config

class DatabaseManager:
    def __init__(self):
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={Config.SQL_SERVER_HOST};"
            f"DATABASE={Config.SQL_SERVER_DATABASE};"
            f"UID={Config.SQL_SERVER_USER};"
            f"PWD={Config.SQL_SERVER_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self):
        """Establece conexión con SQL Server"""
        try:
            conn = pyodbc.connect(self.connection_string)
            return conn
        except Exception as e:
            self.logger.error(f"Error conectando a SQL Server: {e}")
            return None
    
    def create_database(self):
        """Crea la base de datos si no existe"""
        try:
            # Conexión sin especificar base de datos
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={Config.SQL_SERVER_HOST};"
                f"UID={Config.SQL_SERVER_USER};"
                f"PWD={Config.SQL_SERVER_PASSWORD};"
                f"TrustServerCertificate=yes;"
            )
            conn = pyodbc.connect(conn_str)
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Crear base de datos
            cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{Config.SQL_SERVER_DATABASE}') CREATE DATABASE {Config.SQL_SERVER_DATABASE}")
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Error creando base de datos: {e}")
            return False
    
    def create_tables(self):
        """Crea las tablas necesarias"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='usuarios' AND xtype='U')
                CREATE TABLE usuarios (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(50) UNIQUE NOT NULL,
                    password_hash NVARCHAR(255) NOT NULL,
                    email NVARCHAR(100),
                    created_at DATETIME2 DEFAULT GETDATE(),
                    is_active BIT DEFAULT 1
                )
            """)
            
            # Tabla de ofertas laborales
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ofertas_laborales' AND xtype='U')
                CREATE TABLE ofertas_laborales (
                    id NVARCHAR(50) PRIMARY KEY,
                    titulo_oferta NVARCHAR(80) NOT NULL,
                    empresa NVARCHAR(100) NOT NULL,
                    nivel_academico NVARCHAR(20) NOT NULL,
                    puesto NVARCHAR(100) NOT NULL,
                    experiencia_minima_anios INT DEFAULT 0,
                    conocimientos_clave NVARCHAR(500),
                    responsabilidades_breve NVARCHAR(200),
                    modalidad NVARCHAR(20) NOT NULL,
                    ubicacion NVARCHAR(100) NOT NULL,
                    jornada NVARCHAR(30),
                    salario NVARCHAR(50),
                    fecha_publicacion DATE,
                    fecha_cierre DATE,
                    como_postular NVARCHAR(500),
                    url_oferta NVARCHAR(500) NOT NULL,
                    documentos_requeridos NVARCHAR(300),
                    contacto NVARCHAR(100),
                    etiquetas NVARCHAR(200),
                    fuente NVARCHAR(50) NOT NULL,
                    fecha_estimacion BIT DEFAULT 0,
                    created_at DATETIME2 DEFAULT GETDATE(),
                    updated_at DATETIME2 DEFAULT GETDATE()
                )
            """)
            
            # Tabla de logs de extracción
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='logs_extraccion' AND xtype='U')
                CREATE TABLE logs_extraccion (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    fuente NVARCHAR(50) NOT NULL,
                    ofertas_encontradas INT DEFAULT 0,
                    ofertas_nuevas INT DEFAULT 0,
                    ofertas_actualizadas INT DEFAULT 0,
                    errores INT DEFAULT 0,
                    fecha_ejecucion DATETIME2 DEFAULT GETDATE(),
                    duracion_segundos INT,
                    detalles NVARCHAR(MAX)
                )
            """)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Error creando tablas: {e}")
            return False
    
    def insert_oferta(self, oferta_data):
        """Inserta una nueva oferta laboral"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM ofertas_laborales WHERE id = ?", oferta_data['id'])
            if cursor.fetchone():
                # Actualizar oferta existente
                cursor.execute("""
                    UPDATE ofertas_laborales SET
                        titulo_oferta = ?, empresa = ?, nivel_academico = ?, puesto = ?,
                        experiencia_minima_anios = ?, conocimientos_clave = ?, responsabilidades_breve = ?,
                        modalidad = ?, ubicacion = ?, jornada = ?, salario = ?,
                        fecha_publicacion = ?, fecha_cierre = ?, como_postular = ?,
                        url_oferta = ?, documentos_requeridos = ?, contacto = ?,
                        etiquetas = ?, fuente = ?, fecha_estimacion = ?, updated_at = GETDATE()
                    WHERE id = ?
                """, (
                    oferta_data['titulo_oferta'], oferta_data['empresa'], oferta_data['nivel_academico'],
                    oferta_data['puesto'], oferta_data['experiencia_minima_anios'], oferta_data['conocimientos_clave'],
                    oferta_data['responsabilidades_breve'], oferta_data['modalidad'], oferta_data['ubicacion'],
                    oferta_data['jornada'], oferta_data['salario'], oferta_data['fecha_publicacion'],
                    oferta_data['fecha_cierre'], oferta_data['como_postular'], oferta_data['url_oferta'],
                    oferta_data['documentos_requeridos'], oferta_data['contacto'], oferta_data['etiquetas'],
                    oferta_data['fuente'], oferta_data['fecha_estimacion'], oferta_data['id']
                ))
            else:
                # Insertar nueva oferta
                cursor.execute("""
                    INSERT INTO ofertas_laborales (
                        id, titulo_oferta, empresa, nivel_academico, puesto, experiencia_minima_anios,
                        conocimientos_clave, responsabilidades_breve, modalidad, ubicacion, jornada,
                        salario, fecha_publicacion, fecha_cierre, como_postular, url_oferta,
                        documentos_requeridos, contacto, etiquetas, fuente, fecha_estimacion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    oferta_data['id'], oferta_data['titulo_oferta'], oferta_data['empresa'],
                    oferta_data['nivel_academico'], oferta_data['puesto'], oferta_data['experiencia_minima_anios'],
                    oferta_data['conocimientos_clave'], oferta_data['responsabilidades_breve'],
                    oferta_data['modalidad'], oferta_data['ubicacion'], oferta_data['jornada'],
                    oferta_data['salario'], oferta_data['fecha_publicacion'], oferta_data['fecha_cierre'],
                    oferta_data['como_postular'], oferta_data['url_oferta'], oferta_data['documentos_requeridos'],
                    oferta_data['contacto'], oferta_data['etiquetas'], oferta_data['fuente'],
                    oferta_data['fecha_estimacion']
                ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Error insertando oferta: {e}")
            return False
    
    def get_ofertas(self, filtros=None, limit=50, offset=0):
        """Obtiene ofertas laborales con filtros opcionales"""
        try:
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            
            query = "SELECT * FROM ofertas_laborales WHERE 1=1"
            params = []
            
            if filtros:
                if filtros.get('empresa'):
                    query += " AND empresa LIKE ?"
                    params.append(f"%{filtros['empresa']}%")
                
                if filtros.get('nivel_academico'):
                    query += " AND nivel_academico = ?"
                    params.append(filtros['nivel_academico'])
                
                if filtros.get('modalidad'):
                    query += " AND modalidad = ?"
                    params.append(filtros['modalidad'])
                
                if filtros.get('busqueda'):
                    query += " AND (titulo_oferta LIKE ? OR puesto LIKE ? OR conocimientos_clave LIKE ?)"
                    search_term = f"%{filtros['busqueda']}%"
                    params.extend([search_term, search_term, search_term])
            
            query += " ORDER BY created_at DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
            params.extend([offset, limit])
            
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                oferta = dict(zip(columns, row))
                results.append(oferta)
            
            conn.close()
            return results
        except Exception as e:
            self.logger.error(f"Error obteniendo ofertas: {e}")
            return []
    
    def get_oferta_by_id(self, oferta_id):
        """Obtiene una oferta específica por ID"""
        try:
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ofertas_laborales WHERE id = ?", oferta_id)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            
            if row:
                oferta = dict(zip(columns, row))
                conn.close()
                return oferta
            
            conn.close()
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo oferta: {e}")
            return None
    
    def create_user(self, username, password_hash, email=None):
        """Crea un nuevo usuario"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Error creando usuario: {e}")
            return False
    
    def get_user_by_username(self, username):
        """Obtiene un usuario por nombre de usuario"""
        try:
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", username)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            
            if row:
                user = dict(zip(columns, row))
                conn.close()
                return user
            
            conn.close()
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario: {e}")
            return None
