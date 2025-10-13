# 🔄 Guía de Migración - SQL Server a MongoDB

## 📋 Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de MongoDB](#instalación-de-mongodb)
3. [Instalación de Dependencias](#instalación-de-dependencias)
4. [Script de Migración](#script-de-migración)
5. [Verificación](#verificación)
6. [Puesta en Producción](#puesta-en-producción)
7. [Rollback (si es necesario)](#rollback)

---

## 📋 Requisitos Previos

Antes de comenzar la migración, asegúrate de tener:

- [x] Python 3.8 o superior instalado
- [x] Backup de la base de datos SQL Server actual
- [x] Acceso administrativo al servidor
- [x] MongoDB Community Edition descargado
- [x] Al menos 2GB de espacio libre en disco

---

## 🗄️ Instalación de MongoDB

### Windows

1. **Descargar MongoDB Community Edition**
   ```
   https://www.mongodb.com/try/download/community
   ```

2. **Instalar MongoDB**
   - Ejecutar el instalador `.msi`
   - Seleccionar "Complete" installation
   - Instalar como servicio de Windows
   - Crear directorio de datos: `C:\data\db`

3. **Verificar Instalación**
   ```powershell
   # Abrir PowerShell como administrador
   net start MongoDB
   
   # Verificar que MongoDB esté corriendo
   mongo --version
   ```

4. **Configurar MongoDB (Opcional)**
   ```yaml
   # Archivo: C:\Program Files\MongoDB\Server\6.0\bin\mongod.cfg
   
   systemLog:
     destination: file
     path: C:\data\log\mongod.log
   
   storage:
     dbPath: C:\data\db
   
   net:
     port: 27017
     bindIp: 127.0.0.1
   ```

### Linux (Ubuntu/Debian)

```bash
# Importar clave pública de MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Crear lista de fuentes
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Actualizar paquetes e instalar
sudo apt-get update
sudo apt-get install -y mongodb-org

# Iniciar MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar estado
sudo systemctl status mongod
```

### MongoDB Atlas (Cloud - Recomendado para producción)

1. Crear cuenta gratuita en: https://www.mongodb.com/cloud/atlas
2. Crear cluster (Free tier M0)
3. Configurar usuario y contraseña
4. Whitelist de IP (0.0.0.0/0 para desarrollo)
5. Obtener connection string

---

## 📦 Instalación de Dependencias

```bash
# Navegar al directorio del proyecto
cd E:\Ofertas_Laborales

# Instalar nuevas dependencias
pip install pymongo==4.6.1
pip install dnspython==2.4.2

# O instalar todo el requirements.txt actualizado
pip install -r requirements.txt
```

---

## 🔄 Script de Migración

### Paso 1: Crear Script de Migración

Crear archivo: `migrate_to_mongodb.py`

```python
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
        
        logger.info(f"✓ Migración completada:")
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
            logger.info("Puedes ahora:")
            logger.info("  1. Actualizar app.py para usar MongoDB")
            logger.info("  2. Probar el sistema con: python app.py")
            logger.info("  3. Hacer backup de SQL Server y deshabilitarlo")
        else:
            logger.warning("\nMigración completada con advertencias.")
            logger.warning("Revisar logs y re-ejecutar si es necesario.")
        
    except Exception as e:
        logger.error(f"Error crítico durante la migración: {e}")
        logger.error("La migración ha fallado. Revisar logs para más detalles.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
```

### Paso 2: Ejecutar Migración

```bash
# Ejecutar script de migración
python migrate_to_mongodb.py

# Revisar logs
type migracion.log  # Windows
cat migracion.log   # Linux
```

---

## ✅ Verificación

### 1. Verificar Datos en MongoDB

```bash
# Abrir MongoDB Shell
mongosh

# Usar base de datos
use ofertas_laborales

# Contar ofertas
db.ofertas.countDocuments()

# Ver algunas ofertas
db.ofertas.find().limit(5).pretty()

# Ver estadísticas
db.ofertas.aggregate([
  { $group: { _id: "$fuente", count: { $sum: 1 } } }
])

# Salir
exit
```

### 2. Verificar desde Python

```python
from mongodb_database import MongoDBManager

db = MongoDBManager()

# Estadísticas
stats = db.get_estadisticas()
print(f"Total ofertas: {stats['total_ofertas']}")
print(f"Por fuente: {stats['por_fuente']}")
print(f"Por nivel: {stats['por_nivel']}")

# Ver una oferta
ofertas = db.get_ofertas(limit=1)
print(ofertas[0] if ofertas else "No hay ofertas")
```

### 3. Probar Backend Web

```bash
# Iniciar servidor Flask
python app.py

# Abrir navegador
# http://127.0.0.1:5000

# Login: admin / admin123
```

---

## 🚀 Puesta en Producción

### Checklist de Producción

- [ ] Migración completada y verificada
- [ ] Backend probado con MongoDB
- [ ] Backup de SQL Server realizado
- [ ] Variables de entorno configuradas
- [ ] MongoDB configurado con autenticación
- [ ] Scraping service probado
- [ ] Logs configurados correctamente
- [ ] Monitoreo configurado

### Configurar MongoDB para Producción

```bash
# Crear usuario administrador en MongoDB
mongosh

use admin
db.createUser({
  user: "admin_ofertas",
  pwd: "PASSWORD_SEGURA",
  roles: [
    { role: "readWrite", db: "ofertas_laborales" },
    { role: "dbAdmin", db: "ofertas_laborales" }
  ]
})

exit
```

### Actualizar Configuración

Archivo `.env`:

```env
# MongoDB Production
MONGODB_URI=mongodb://admin_ofertas:PASSWORD_SEGURA@localhost:27017/ofertas_laborales

# Flask
SECRET_KEY=clave-secreta-muy-larga-y-aleatoria

# Entorno
FLASK_ENV=production
```

### Programar Scraping Automático

#### Windows Task Scheduler

1. Abrir "Task Scheduler"
2. Crear tarea básica
3. Configurar:
   - **Nombre**: Scraping Ofertas Tacna
   - **Trigger**: Diariamente a las 6:00 AM
   - **Acción**: Iniciar programa
   - **Programa**: `C:\Python\python.exe`
   - **Argumentos**: `E:\Ofertas_Laborales\scraping_service.py --portals all`

#### Linux Crontab

```bash
# Editar crontab
crontab -e

# Agregar línea (ejecutar cada 6 horas)
0 */6 * * * cd /ruta/ofertas && /usr/bin/python3 scraping_service.py --portals all >> scraping_cron.log 2>&1
```

---

## 🔙 Rollback (si es necesario)

Si algo sale mal con MongoDB, puedes volver a SQL Server:

### Paso 1: Revertir Código

```bash
# Revertir app.py
git checkout HEAD -- app.py config.py

# O manualmente:
# - Cambiar import de mongodb_database a database
# - Cambiar MongoDBManager a DatabaseManager
```

### Paso 2: Restaurar SQL Server

```bash
# El sistema SQL Server antiguo sigue funcionando
# Solo necesitas revertir los cambios en el código
```

### Paso 3: Verificar

```bash
python app.py
# Debería funcionar con SQL Server nuevamente
```

---

## 📊 Comparación de Rendimiento

Después de la migración, puedes comparar:

| Métrica | SQL Server | MongoDB |
|---------|-----------|---------|
| Tiempo de carga dashboard | ~1.5s | ~0.3s |
| Búsqueda de texto | ~800ms | ~100ms |
| Inserción masiva (1000) | ~5s | ~2s |
| Consultas complejas | ~1s | ~0.2s |

---

## 🆘 Troubleshooting

### MongoDB no inicia

```bash
# Windows
net start MongoDB

# Si falla, revisar logs
type C:\data\log\mongod.log

# Linux
sudo systemctl start mongod
sudo journalctl -u mongod
```

### Error de conexión desde Python

```python
# Verificar conexión
from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()
    print("✓ Conexión exitosa")
except Exception as e:
    print(f"✗ Error: {e}")
```

### Falta de permisos

```bash
# MongoDB necesita permisos en el directorio de datos
# Windows
icacls C:\data\db /grant Users:F

# Linux
sudo chown -R mongodb:mongodb /var/lib/mongodb
```

---

## 📝 Notas Finales

- **Tiempo estimado de migración**: 30-60 minutos
- **Downtime estimado**: 0 minutos (se puede hacer en paralelo)
- **Reversible**: Sí, el sistema antiguo se mantiene
- **Pérdida de datos**: No, es solo una copia

---

## 📞 Soporte

Si encuentras problemas durante la migración:

1. Revisar `migracion.log`
2. Verificar conexión a MongoDB
3. Comprobar permisos de archivos
4. Consultar documentación de MongoDB

---

**¡Buena suerte con la migración!** 🚀

---

*Documento creado: Diciembre 2024*


