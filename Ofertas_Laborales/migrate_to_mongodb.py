#!/usr/bin/env python3
"""
Script de Migración: SQL Server → MongoDB
Migra ofertas laborales y usuarios del sistema antiguo al nuevo
"""

import logging
from datetime import datetime
from database import DatabaseManager  # SQL Server (antiguo)
from mongodb_database import MongoDBManager  # MongoDB (nuevo)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migracion.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def migrate_ofertas(sql_db, mongo_db):
    """Migra ofertas laborales de SQL Server a MongoDB"""
    logger.info("=== Iniciando migración de ofertas ===")
    
    try:
        # Obtener todas las ofertas de SQL Server
        ofertas = sql_db.get_ofertas(limit=10000)
        total = len(ofertas)
        logger.info(f"Total de ofertas a migrar: {total}")
        
        migradas = 0
        errores = 0
        
        for i, oferta in enumerate(ofertas, 1):
            try:
                # Convertir fechas datetime a string si es necesario
                if isinstance(oferta.get('created_at'), datetime):
                    oferta['created_at'] = oferta['created_at'].isoformat()
                if isinstance(oferta.get('updated_at'), datetime):
                    oferta['updated_at'] = oferta['updated_at'].isoformat()
                if isinstance(oferta.get('fecha_publicacion'), datetime):
                    oferta['fecha_publicacion'] = oferta['fecha_publicacion'].strftime('%Y-%m-%d')
                if isinstance(oferta.get('fecha_cierre'), datetime):
                    oferta['fecha_cierre'] = oferta['fecha_cierre'].strftime('%Y-%m-%d')
                
                # Insertar en MongoDB
                if mongo_db.insert_oferta(oferta):
                    migradas += 1
                    if i % 100 == 0:
                        logger.info(f"Progreso: {i}/{total} ofertas procesadas")
                else:
                    logger.warning(f"Oferta duplicada o error: {oferta.get('id')}")
                    
            except Exception as e:
                logger.error(f"Error migrando oferta {oferta.get('id')}: {e}")
                errores += 1
        
        logger.info(f"✓ Migración de ofertas completada:")
        logger.info(f"  - Migradas: {migradas}")
        logger.info(f"  - Errores: {errores}")
        
        return migradas, errores
        
    except Exception as e:
        logger.error(f"Error crítico en migración de ofertas: {e}")
        raise

def migrate_usuarios(sql_db, mongo_db):
    """Migra usuarios de SQL Server a MongoDB"""
    logger.info("=== Iniciando migración de usuarios ===")
    
    try:
        # Obtener usuario admin (ejemplo)
        usuario = sql_db.get_user_by_username('admin')
        
        if usuario:
            # Verificar si ya existe en MongoDB
            existing = mongo_db.get_user_by_username('admin')
            
            if not existing:
                mongo_db.create_user(
                    username=usuario['username'],
                    password_hash=usuario['password_hash'],
                    email=usuario.get('email')
                )
                logger.info(f"✓ Usuario migrado: {usuario['username']}")
            else:
                logger.info(f"Usuario ya existe en MongoDB: {usuario['username']}")
        else:
            logger.warning("No se encontró usuario admin en SQL Server")
        
    except Exception as e:
        logger.error(f"Error en migración de usuarios: {e}")

def verificar_migracion(sql_db, mongo_db):
    """Verifica que la migración se haya realizado correctamente"""
    logger.info("=== Verificando migración ===")
    
    try:
        # Contar ofertas en ambas bases de datos
        sql_count = len(sql_db.get_ofertas(limit=10000))
        mongo_count = mongo_db.count_ofertas()
        
        logger.info(f"Ofertas en SQL Server: {sql_count}")
        logger.info(f"Ofertas en MongoDB: {mongo_count}")
        
        if mongo_count >= sql_count * 0.95:  # Al menos 95%
            logger.info("✓ Verificación exitosa: Migración completa")
            return True
        else:
            logger.warning("⚠ Advertencia: Faltan ofertas por migrar")
            logger.warning(f"  Esperadas: {sql_count}, Migradas: {mongo_count}")
            return False
            
    except Exception as e:
        logger.error(f"Error en verificación: {e}")
        return False

def main():
    """Función principal de migración"""
    logger.info("="*60)
    logger.info("INICIO DE MIGRACIÓN: SQL Server → MongoDB")
    logger.info("="*60)
    
    try:
        # Conectar a ambas bases de datos
        logger.info("Conectando a SQL Server...")
        sql_db = DatabaseManager()
        
        logger.info("Conectando a MongoDB...")
        mongo_db = MongoDBManager()
        
        # Migrar ofertas
        ofertas_migradas, ofertas_errores = migrate_ofertas(sql_db, mongo_db)
        
        # Migrar usuarios
        migrate_usuarios(sql_db, mongo_db)
        
        # Verificar migración
        exito = verificar_migracion(sql_db, mongo_db)
        
        # Resumen final
        logger.info("="*60)
        logger.info("RESUMEN DE MIGRACIÓN")
        logger.info("="*60)
        logger.info(f"Ofertas migradas: {ofertas_migradas}")
        logger.info(f"Errores: {ofertas_errores}")
        logger.info(f"Estado: {'✓ EXITOSO' if exito else '⚠ CON ADVERTENCIAS'}")
        logger.info("="*60)
        
        if exito:
            logger.info("\n¡Migración completada exitosamente!")
            logger.info("\nPróximos pasos:")
            logger.info("  1. Probar el sistema con: python app.py")
            logger.info("  2. Verificar que todo funcione correctamente")
            logger.info("  3. Hacer backup de SQL Server")
            logger.info("  4. Configurar scraping automático")
        else:
            logger.warning("\nMigración completada con advertencias.")
            logger.warning("Revisar logs y re-ejecutar si es necesario.")
        
    except Exception as e:
        logger.error(f"Error crítico durante la migración: {e}")
        logger.error("La migración ha fallado. Revisar logs para más detalles.")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())


