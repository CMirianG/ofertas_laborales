# 🚀 Inicio Rápido - Sistema de Ofertas Laborales v2.0

## ⚡ Instrucciones en 5 Minutos

### Paso 1: Instalar MongoDB

**Windows:**
```bash
# Descargar de: https://www.mongodb.com/try/download/community
# Ejecutar instalador y seleccionar "Complete Installation"
# Verificar instalación:
net start MongoDB
```

**Linux (Ubuntu):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### Paso 2: Instalar Dependencias Python

```bash
cd E:\Ofertas_Laborales
pip install -r requirements.txt
```

### Paso 3: Ejecutar Sistema

```bash
# Iniciar servidor web
python app.py
```

Abrir navegador: **http://127.0.0.1:5000**

Login:
- **Usuario:** admin
- **Contraseña:** admin123

### Paso 4: Extraer Ofertas

En el dashboard, hacer clic en **"Extraer Ofertas"** o ejecutar:

```bash
python scraping_service.py --portals all
```

---

## 🔄 Migrar desde SQL Server (Opcional)

Si tienes datos en SQL Server:

```bash
python migrate_to_mongodb.py
```

---

## 📊 Verificar que Todo Funciona

```python
# Abrir Python
python

# Ejecutar:
from mongodb_database import MongoDBManager

db = MongoDBManager()
stats = db.get_estadisticas()

print(f"Total ofertas: {stats['total_ofertas']}")
print(f"Por fuente: {stats['por_fuente']}")
```

---

## 🆘 Problemas Comunes

### MongoDB no conecta
```bash
# Windows
net start MongoDB

# Linux
sudo systemctl start mongod
```

### Error al instalar pymongo
```bash
pip install --only-binary :all: pymongo
```

### Puerto 5000 ocupado
Modificar en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 📚 Documentación Completa

- [README_NUEVO.md](README_NUEVO.md) - Guía completa
- [NUEVA_ARQUITECTURA.md](NUEVA_ARQUITECTURA.md) - Arquitectura técnica
- [GUIA_MIGRACION.md](GUIA_MIGRACION.md) - Migración detallada

---

**¡Listo! El sistema debería estar funcionando.** 🎉


