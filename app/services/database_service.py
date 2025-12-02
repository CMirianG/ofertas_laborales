"""
Gestor de base de datos MongoDB para el sistema de ofertas laborales
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError, ConnectionFailure
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from bson import ObjectId

class MongoDBManager:
    def __init__(self, connection_string: str = None):
        """
        Inicializa la conexión a MongoDB
        Args:
            connection_string: URI de conexión a MongoDB (por defecto usa localhost)
        """
        self.logger = logging.getLogger(__name__)
        
        # Configuración por defecto para MongoDB local
        if not connection_string:
            connection_string = "mongodb://localhost:27017/"
        
        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self.client.admin.command('ping')
            self.logger.info("Conexión exitosa a MongoDB")
            
            # Base de datos principal
            self.db = self.client['ofertas_laborales']
            
            # Colecciones
            self.ofertas_collection = self.db['ofertas']
            self.usuarios_collection = self.db['usuarios']
            self.logs_collection = self.db['logs_extraccion']
            
            # Crear índices para optimizar consultas
            self._create_indexes()
            
            self._connected = True
            
        except (ConnectionFailure, Exception) as e:
            self.logger.error(f"Error conectando a MongoDB: {e}")
            self.logger.warning("La aplicación continuará pero algunas funcionalidades no estarán disponibles")
            self._connected = False
            # Crear objetos None para evitar errores
            self.client = None
            self.db = None
            self.ofertas_collection = None
            self.usuarios_collection = None
            self.logs_collection = None
    
    def _create_indexes(self):
        """Crea índices para optimizar las consultas"""
        try:
            # Índice único para el ID de oferta
            self.ofertas_collection.create_index([("id", ASCENDING)], unique=True)
            
            # Índices para búsquedas frecuentes
            self.ofertas_collection.create_index([("empresa", ASCENDING)])
            self.ofertas_collection.create_index([("nivel_academico", ASCENDING)])
            self.ofertas_collection.create_index([("modalidad", ASCENDING)])
            self.ofertas_collection.create_index([("fuente", ASCENDING)])
            self.ofertas_collection.create_index([("fecha_publicacion", DESCENDING)])
            self.ofertas_collection.create_index([("created_at", DESCENDING)])
            
            # Índice de texto para búsquedas
            self.ofertas_collection.create_index([
                ("titulo_oferta", "text"),
                ("puesto", "text"),
                ("conocimientos_clave", "text"),
                ("responsabilidades_breve", "text")
            ])
            
            # Índice único para username en usuarios
            self.usuarios_collection.create_index([("username", ASCENDING)], unique=True)
            
            self.logger.info("Índices creados exitosamente")
        except Exception as e:
            self.logger.error(f"Error creando índices: {e}")
    
    def _check_connection(self) -> bool:
        """Verifica si hay conexión a MongoDB"""
        if not self._connected or not self.client:
            return False
        try:
            self.client.admin.command('ping')
            return True
        except:
            return False
    
    def insert_oferta(self, oferta_data: Dict) -> bool:
        """
        Inserta o actualiza una oferta laboral
        Args:
            oferta_data: Diccionario con los datos de la oferta
        Returns:
            True si se insertó/actualizó correctamente
        """
        if not self._check_connection():
            self.logger.warning("No hay conexión a MongoDB. No se puede insertar oferta.")
            return False
        
        try:
            # Añadir timestamps
            oferta_data['updated_at'] = datetime.now()
            
            # Intentar insertar o actualizar si ya existe
            result = self.ofertas_collection.update_one(
                {'id': oferta_data['id']},
                {
                    '$set': oferta_data,
                    '$setOnInsert': {'created_at': datetime.now()}
                },
                upsert=True
            )
            
            if result.upserted_id:
                self.logger.info(f"Oferta insertada: {oferta_data['id']}")
            else:
                self.logger.info(f"Oferta actualizada: {oferta_data['id']}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error insertando/actualizando oferta: {e}")
            return False
    
    def get_ofertas(self, filtros: Dict = None, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Obtiene ofertas con filtros opcionales
        Args:
            filtros: Diccionario con los filtros a aplicar
            limit: Número máximo de resultados
            offset: Número de resultados a saltar (paginación)
        Returns:
            Lista de ofertas
        """
        if not self._check_connection():
            return []
        
        try:
            query = {}
            
            if filtros:
                # Filtro por empresa
                if filtros.get('empresa'):
                    query['empresa'] = {'$regex': filtros['empresa'], '$options': 'i'}
                
                # Filtro por nivel académico
                if filtros.get('nivel_academico'):
                    query['nivel_academico'] = filtros['nivel_academico']
                
                # Filtro por modalidad
                if filtros.get('modalidad'):
                    query['modalidad'] = filtros['modalidad']
                
                # Búsqueda de texto
                if filtros.get('busqueda'):
                    query['$text'] = {'$search': filtros['busqueda']}
            
            # Ejecutar consulta con paginación
            cursor = self.ofertas_collection.find(query).sort('created_at', DESCENDING).skip(offset).limit(limit)
            
            # Convertir ObjectId a string para serialización JSON
            ofertas = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                # Convertir fechas a string si son datetime
                if isinstance(doc.get('created_at'), datetime):
                    doc['created_at'] = doc['created_at'].isoformat()
                if isinstance(doc.get('updated_at'), datetime):
                    doc['updated_at'] = doc['updated_at'].isoformat()
                ofertas.append(doc)
            
            return ofertas
            
        except Exception as e:
            self.logger.error(f"Error obteniendo ofertas: {e}")
            return []
    
    def get_oferta_by_id(self, oferta_id: str) -> Optional[Dict]:
        """
        Obtiene una oferta específica por su ID
        Args:
            oferta_id: ID de la oferta
        Returns:
            Diccionario con los datos de la oferta o None
        """
        if not self._check_connection():
            return None
        
        try:
            oferta = self.ofertas_collection.find_one({'id': oferta_id})
            
            if oferta:
                oferta['_id'] = str(oferta['_id'])
                # Convertir fechas a string
                if isinstance(oferta.get('created_at'), datetime):
                    oferta['created_at'] = oferta['created_at'].isoformat()
                if isinstance(oferta.get('updated_at'), datetime):
                    oferta['updated_at'] = oferta['updated_at'].isoformat()
            
            return oferta
            
        except Exception as e:
            self.logger.error(f"Error obteniendo oferta: {e}")
            return None
    
    def count_ofertas(self, filtros: Dict = None) -> int:
        """
        Cuenta el número de ofertas que cumplen con los filtros
        Args:
            filtros: Diccionario con los filtros
        Returns:
            Número de ofertas
        """
        if not self._check_connection():
            return 0
        
        try:
            query = {}
            
            if filtros:
                if filtros.get('empresa'):
                    query['empresa'] = {'$regex': filtros['empresa'], '$options': 'i'}
                if filtros.get('nivel_academico'):
                    query['nivel_academico'] = filtros['nivel_academico']
                if filtros.get('modalidad'):
                    query['modalidad'] = filtros['modalidad']
                if filtros.get('busqueda'):
                    query['$text'] = {'$search': filtros['busqueda']}
            
            return self.ofertas_collection.count_documents(query)
            
        except Exception as e:
            self.logger.error(f"Error contando ofertas: {e}")
            return 0
    
    def get_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas generales de las ofertas
        Returns:
            Diccionario con estadísticas
        """
        if not self._check_connection():
            return {
                'total_ofertas': 0,
                'por_nivel': {},
                'por_modalidad': {},
                'por_fuente': {},
                'top_empresas': {}
            }
        
        try:
            # Total de ofertas
            total_ofertas = self.ofertas_collection.count_documents({})
            
            # Ofertas por nivel académico
            niveles = list(self.ofertas_collection.aggregate([
                {'$group': {'_id': '$nivel_academico', 'count': {'$sum': 1}}}
            ]))
            
            # Ofertas por modalidad
            modalidades = list(self.ofertas_collection.aggregate([
                {'$group': {'_id': '$modalidad', 'count': {'$sum': 1}}}
            ]))
            
            # Ofertas por fuente
            fuentes = list(self.ofertas_collection.aggregate([
                {'$group': {'_id': '$fuente', 'count': {'$sum': 1}}}
            ]))
            
            # Ofertas por empresa (top 10)
            empresas = list(self.ofertas_collection.aggregate([
                {'$group': {'_id': '$empresa', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]))
            
            return {
                'total_ofertas': total_ofertas,
                'por_nivel': {item['_id']: item['count'] for item in niveles},
                'por_modalidad': {item['_id']: item['count'] for item in modalidades},
                'por_fuente': {item['_id']: item['count'] for item in fuentes},
                'top_empresas': {item['_id']: item['count'] for item in empresas}
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def create_user(self, username: str, password_hash: str, email: str = None) -> bool:
        """
        Crea un nuevo usuario
        Args:
            username: Nombre de usuario
            password_hash: Hash de la contraseña
            email: Email del usuario (opcional)
        Returns:
            True si se creó correctamente
        """
        if not self._check_connection():
            return False
        
        try:
            user_data = {
                'username': username,
                'password_hash': password_hash,
                'email': email,
                'created_at': datetime.now(),
                'is_active': True
            }
            
            self.usuarios_collection.insert_one(user_data)
            self.logger.info(f"Usuario creado: {username}")
            return True
            
        except DuplicateKeyError:
            self.logger.warning(f"Usuario ya existe: {username}")
            return False
        except Exception as e:
            self.logger.error(f"Error creando usuario: {e}")
            return False
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Obtiene un usuario por su nombre de usuario
        Args:
            username: Nombre de usuario
        Returns:
            Diccionario con los datos del usuario o None
        """
        if not self._check_connection():
            return None
        
        try:
            user = self.usuarios_collection.find_one({'username': username})
            
            if user:
                user['_id'] = str(user['_id'])
                user['id'] = str(user['_id'])  # Para compatibilidad con el código existente
                if isinstance(user.get('created_at'), datetime):
                    user['created_at'] = user['created_at'].isoformat()
            
            return user
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario: {e}")
            return None
    
    def insert_log_extraccion(self, log_data: Dict) -> bool:
        """
        Registra un log de extracción
        Args:
            log_data: Datos del log
        Returns:
            True si se insertó correctamente
        """
        try:
            log_data['fecha_ejecucion'] = datetime.now()
            self.logs_collection.insert_one(log_data)
            return True
            
        except Exception as e:
            self.logger.error(f"Error insertando log: {e}")
            return False
    
    def get_logs_extraccion(self, limit: int = 50) -> List[Dict]:
        """
        Obtiene los últimos logs de extracción
        Args:
            limit: Número máximo de logs a retornar
        Returns:
            Lista de logs
        """
        try:
            cursor = self.logs_collection.find().sort('fecha_ejecucion', DESCENDING).limit(limit)
            
            logs = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                if isinstance(doc.get('fecha_ejecucion'), datetime):
                    doc['fecha_ejecucion'] = doc['fecha_ejecucion'].isoformat()
                logs.append(doc)
            
            return logs
            
        except Exception as e:
            self.logger.error(f"Error obteniendo logs: {e}")
            return []
    
    def delete_oferta(self, oferta_id: str) -> bool:
        """
        Elimina una oferta por su ID
        Args:
            oferta_id: ID de la oferta
        Returns:
            True si se eliminó correctamente
        """
        try:
            result = self.ofertas_collection.delete_one({'id': oferta_id})
            return result.deleted_count > 0
            
        except Exception as e:
            self.logger.error(f"Error eliminando oferta: {e}")
            return False
    
    def clear_old_ofertas(self, days: int = 90) -> int:
        """
        Elimina ofertas antiguas
        Args:
            days: Número de días a mantener
        Returns:
            Número de ofertas eliminadas
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            result = self.ofertas_collection.delete_many({
                'created_at': {'$lt': cutoff_date}
            })
            
            self.logger.info(f"Eliminadas {result.deleted_count} ofertas antiguas")
            return result.deleted_count
            
        except Exception as e:
            self.logger.error(f"Error eliminando ofertas antiguas: {e}")
            return 0
    
    def close(self):
        """Cierra la conexión a MongoDB"""
        try:
            self.client.close()
            self.logger.info("Conexión a MongoDB cerrada")
        except Exception as e:
            self.logger.error(f"Error cerrando conexión: {e}")


if __name__ == "__main__":
    # Prueba de conexión
    logging.basicConfig(level=logging.INFO)
    
    try:
        db = MongoDBManager()
        print("✓ Conexión a MongoDB exitosa")
        
        # Mostrar estadísticas
        stats = db.get_estadisticas()
        print(f"\nEstadísticas:")
        print(f"  Total de ofertas: {stats.get('total_ofertas', 0)}")
        print(f"  Por nivel: {stats.get('por_nivel', {})}")
        print(f"  Por modalidad: {stats.get('por_modalidad', {})}")
        print(f"  Por fuente: {stats.get('por_fuente', {})}")
        
        db.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")

