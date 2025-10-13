# 🎯 Sistema de Ofertas Laborales - Tacna

## 📌 Versión 2.0 - Arquitectura Renovada

Sistema web para la extracción, gestión y visualización de ofertas laborales en la ciudad de Tacna, Perú. Desarrollado para la Universidad Privada de Tacna (UPT) - Oficina de Responsabilidad Social Universitaria.

---

## ✨ Novedades Versión 2.0

### 🗄️ Base de Datos NoSQL (MongoDB)
- ✅ Cambio de SQL Server a MongoDB
- ✅ Esquema flexible y escalable
- ✅ Búsquedas de texto optimizadas
- ✅ Agregaciones eficientes

### 🔧 Servicio de Scraping Independiente
- ✅ Separado del backend web
- ✅ Ejecutable por línea de comandos
- ✅ Programable con cron/Task Scheduler
- ✅ Mejor manejo de errores

### 📊 Extracción Mejorada
- ✅ Más información de las publicaciones
- ✅ Detección automática de palabras clave
- ✅ Validación robusta de datos
- ✅ Análisis de requisitos y beneficios

---

## 🚀 Inicio Rápido

### 1. Requisitos

- Python 3.8 o superior
- MongoDB 4.4 o superior
- Navegador web moderno

### 2. Instalación

```bash
# Clonar o descargar el proyecto
cd E:\Ofertas_Laborales

# Instalar dependencias
pip install -r requirements.txt

# Asegurarse que MongoDB esté corriendo
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

### 3. Configuración

Crear archivo `.env` (opcional):

```env
MONGODB_URI=mongodb://localhost:27017/
SECRET_KEY=tu-clave-secreta-super-segura
```

### 4. Ejecutar

```bash
# Iniciar servidor web
python app.py
```

Abrir navegador en: http://127.0.0.1:5000

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

---

## 📖 Documentación

- [🏗️ Nueva Arquitectura](NUEVA_ARQUITECTURA.md) - Detalles técnicos de la arquitectura
- [🔄 Guía de Migración](GUIA_MIGRACION.md) - Migración desde SQL Server
- [📋 Resumen del Proyecto](RESUMEN_PROYECTO.md) - Información general

---

## 🛠️ Uso del Sistema

### Backend Web (Flask)

```bash
# Iniciar servidor
python app.py

# El servidor estará en http://127.0.0.1:5000
```

### Servicio de Scraping

```bash
# Extraer de todos los portales
python scraping_service.py --portals all

# Extraer de portales específicos
python scraping_service.py --portals computrabajo indeed

# Con MongoDB remoto
python scraping_service.py --mongodb-uri mongodb://user:pass@host:27017/
```

### Uso Programático

```python
from mongodb_database import MongoDBManager
from scraping_service import ScrapingService

# Conectar a MongoDB
db = MongoDBManager()

# Obtener estadísticas
stats = db.get_estadisticas()
print(f"Total ofertas: {stats['total_ofertas']}")

# Obtener ofertas con filtros
ofertas = db.get_ofertas(
    filtros={'nivel_academico': 'Profesional'},
    limit=20
)

# Scraping programático
service = ScrapingService(db)
results = service.run_scraping(['computrabajo'])
print(f"Nuevas ofertas: {results['nuevas']}")
```

---

## 📁 Estructura del Proyecto

```
Ofertas_Laborales/
├── 🌐 Backend
│   ├── app.py                      # Aplicación Flask principal
│   ├── mongodb_database.py         # ✨ Gestor de MongoDB
│   ├── scraping_service.py         # ✨ Servicio de scraping independiente
│   ├── config.py                   # Configuración
│   └── database.py                 # [DEPRECADO] SQL Server
│
├── 🎨 Frontend
│   ├── templates/                  # Templates HTML
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── ofertas.html
│   │   ├── ver_oferta.html
│   │   └── estadisticas.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
│
├── 📚 Documentación
│   ├── README_NUEVO.md             # ✨ Este archivo
│   ├── NUEVA_ARQUITECTURA.md       # ✨ Documentación técnica
│   ├── GUIA_MIGRACION.md          # ✨ Guía de migración
│   ├── RESUMEN_PROYECTO.md         # Resumen general
│   └── DOCUMENTO_ARQUITECTURA_SOLUCION.md
│
├── ⚙️ Configuración
│   ├── requirements.txt            # Dependencias Python
│   ├── config.py                   # Configuración del sistema
│   └── .env                        # Variables de entorno (crear)
│
└── 🔧 Scripts
    ├── migrate_to_mongodb.py       # Script de migración
    └── extractor_simple.py         # [DEPRECADO] Scraping antiguo
```

---

## 🌐 Portales Soportados

El sistema extrae ofertas de los siguientes portales laborales peruanos:

- 🔵 **Computrabajo** - https://pe.computrabajo.com
- 🟢 **Indeed** - https://pe.indeed.com
- 🔴 **Bumeran** - https://www.bumeran.com.pe
- 🟡 **Trabajos.pe** - https://www.trabajos.pe

**Filtros aplicados:**
- 📍 Solo ubicaciones en **Tacna**
- 🎓 Niveles: **Practicante**, **Bachiller**, **Profesional**

---

## 📊 Características Principales

### 1. Dashboard Interactivo
- Estadísticas en tiempo real
- Gráficos de Chart.js
- Últimas ofertas publicadas
- Distribución por fuente y nivel

### 2. Búsqueda Avanzada
- Búsqueda de texto completo
- Filtros por empresa, nivel, modalidad
- Ordenamiento por fecha
- Paginación

### 3. Extracción Automática
- 4 portales laborales
- Validación de datos
- Deduplicación inteligente
- Logs detallados

### 4. API REST
- Endpoints JSON para integración
- Autenticación de sesión
- Filtros dinámicos
- Paginación

---

## 🔧 API Endpoints

### Autenticación

```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

### Obtener Ofertas

```http
GET /api/ofertas?busqueda=python&nivel_academico=Profesional&limit=20&page=1
Authorization: Session cookie
```

### Extraer Nuevas Ofertas

```http
POST /extraer
Content-Type: application/json
Authorization: Session cookie

{
  "portals": ["computrabajo", "indeed"]
}
```

---

## 📈 Estadísticas y Agregaciones

### Obtener Estadísticas Generales

```python
from mongodb_database import MongoDBManager

db = MongoDBManager()
stats = db.get_estadisticas()

print(f"Total de ofertas: {stats['total_ofertas']}")
print(f"Por nivel académico: {stats['por_nivel']}")
print(f"Por modalidad: {stats['por_modalidad']}")
print(f"Por fuente: {stats['por_fuente']}")
print(f"Top 10 empresas: {stats['top_empresas']}")
```

### Consultas Personalizadas

```python
# Ofertas de programación para profesionales
ofertas = db.get_ofertas(
    filtros={
        'busqueda': 'python javascript',
        'nivel_academico': 'Profesional'
    },
    limit=50
)

# Ofertas remotas
ofertas_remotas = db.get_ofertas(
    filtros={'modalidad': 'Remoto'},
    limit=100
)

# Contar ofertas por empresa
count = db.count_ofertas(filtros={'empresa': 'Tech Company'})
```

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Sesiones seguras con Flask
- ✅ Validación de entrada
- ✅ Sin inyección SQL (NoSQL)
- ✅ CSRF protection recomendado para producción

---

## ⚙️ Configuración Avanzada

### MongoDB Atlas (Cloud)

```env
# .env
MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/ofertas_laborales?retryWrites=true&w=majority
```

### Programar Scraping Automático

#### Windows Task Scheduler

Crear archivo `scraping_task.bat`:

```batch
@echo off
cd /d E:\Ofertas_Laborales
python scraping_service.py --portals all
```

Programar en Task Scheduler para ejecutar cada 6 horas.

#### Linux Crontab

```bash
# Editar crontab
crontab -e

# Agregar línea
0 */6 * * * cd /ruta/ofertas && python3 scraping_service.py --portals all >> cron.log 2>&1
```

---

## 🐛 Troubleshooting

### MongoDB no conecta

```bash
# Verificar servicio
net start MongoDB  # Windows
sudo systemctl status mongod  # Linux

# Verificar puerto
netstat -an | findstr 27017  # Windows
netstat -an | grep 27017  # Linux
```

### Error al instalar pymongo

```bash
# Windows: Requiere Microsoft Visual C++ Build Tools
# O usar wheel pre-compilado
pip install --only-binary :all: pymongo
```

### Scraping retorna 0 ofertas

1. Verificar conexión a Internet
2. Revisar `scraping.log`
3. Algunos portales pueden bloquear temporalmente
4. Intentar con `--portals` uno a la vez

### Error de permisos en Windows

```powershell
# Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 Métricas de Rendimiento

| Operación | Tiempo |
|-----------|--------|
| Carga de dashboard | ~300ms |
| Búsqueda de ofertas | ~100ms |
| Scraping completo | ~2-3 min |
| Inserción 1000 ofertas | ~2 seg |

---

## 🤝 Contribuir

Este es un proyecto académico, pero aceptamos sugerencias:

1. Reportar bugs
2. Sugerir mejoras
3. Contribuir código
4. Mejorar documentación

---

## 📝 Licencia

Proyecto desarrollado para la Universidad Privada de Tacna (UPT).  
Todos los derechos reservados © 2024

---

## 👥 Créditos

**Desarrollado para:**
- 🏛️ Universidad Privada de Tacna (UPT)
- 🤝 Oficina de Responsabilidad Social Universitaria (RSU)
- 🇵🇪 Ciudad de Tacna, Perú

**Tecnologías:**
- Python 3.13
- Flask 2.3.3
- MongoDB 6.0
- Bootstrap 5
- Chart.js

---

## 📞 Contacto y Soporte

Para consultas sobre el proyecto:
- **Institución:** Universidad Privada de Tacna
- **Oficina:** RSU - Responsabilidad Social Universitaria
- **Ubicación:** Tacna, Perú

---

## 🗺️ Roadmap Futuro

- [ ] Autenticación con JWT
- [ ] API pública documentada con Swagger
- [ ] Notificaciones por email
- [ ] Exportación a PDF/Excel
- [ ] App móvil (Flutter)
- [ ] Machine Learning para clasificación
- [ ] Integración con LinkedIn
- [ ] Sistema de postulaciones

---

**¡Gracias por usar el Sistema de Ofertas Laborales de Tacna!** 🎉

---

*Última actualización: Diciembre 2024 - Versión 2.0*


