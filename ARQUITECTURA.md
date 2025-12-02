# 🏗️ Arquitectura del Sistema - Ofertas Laborales Tacna

## 📐 Visión General

El sistema ha sido reestructurado siguiendo una **arquitectura por capas** bien definida, separando responsabilidades y facilitando el mantenimiento y escalabilidad.

## 🎯 Principios de Diseño

1. **Separación de Responsabilidades**: Cada módulo tiene una única responsabilidad
2. **Factory Pattern**: Aplicación Flask creada mediante factory function
3. **Blueprints**: Rutas organizadas por funcionalidad
4. **Dependency Injection**: Servicios inyectados donde se necesitan
5. **Configuración Externa**: Variables de entorno para configuración

## 📁 Estructura de Directorios

```
Ofertas_Laborales/
│
├── app/                          # 🎯 Aplicación principal
│   ├── __init__.py              # Factory pattern para Flask
│   │
│   ├── controllers/             # 🎮 Controladores (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py              # Autenticación (login, logout)
│   │   ├── ofertas.py           # Gestión de ofertas (CRUD, API)
│   │   └── dashboard.py         # Dashboard y estadísticas
│   │
│   ├── services/                 # ⚙️ Servicios (Lógica de negocio)
│   │   ├── __init__.py
│   │   ├── database_service.py  # Gestor de MongoDB
│   │   └── scraping_service.py  # Servicio de scraping
│   │
│   ├── utils/                    # 🔧 Utilidades
│   │   ├── __init__.py
│   │   ├── validators.py        # Validadores de datos
│   │   └── helpers.py           # Funciones auxiliares
│   │
│   ├── templates/                # 📄 Plantillas HTML
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── ofertas.html
│   │   ├── ver_oferta.html
│   │   └── estadisticas.html
│   │
│   └── static/                    # 🎨 Archivos estáticos
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
│
├── config/                        # ⚙️ Configuración
│   ├── __init__.py
│   └── settings.py               # Configuración del sistema
│
├── scripts/                       # 📜 Scripts de utilidad
│   ├── migrate_to_mongodb.py     # Script de migración
│   └── scraping_cli.py           # CLI para scraping
│
├── tests/                         # 🧪 Tests (opcional)
│
├── requirements.txt              # 📦 Dependencias
├── .env.example                  # Ejemplo de variables de entorno
└── run.py                        # 🚀 Punto de entrada principal
```

## 🔄 Flujo de Datos

```
┌─────────────┐
│   Cliente   │
│  (Browser)  │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────────────────────┐
│   app/controllers/              │  ← Capa de Presentación
│   (Blueprints)                  │
│   - auth.py                     │
│   - ofertas.py                  │
│   - dashboard.py                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   app/services/                 │  ← Capa de Servicios
│   - database_service.py         │
│   - scraping_service.py         │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   MongoDB                       │  ← Capa de Datos
│   (Base de datos)               │
└─────────────────────────────────┘
```

## 📦 Módulos Principales

### 1. Controllers (Blueprints)

**Responsabilidad**: Manejar las peticiones HTTP y coordinar con los servicios.

- **`auth.py`**: 
  - `/login` - Autenticación de usuarios
  - `/logout` - Cerrar sesión
  - Decorador `@login_required`

- **`ofertas.py`**:
  - `/ofertas` - Lista de ofertas con filtros
  - `/ofertas/<id>` - Detalle de oferta
  - `/api/ofertas` - API JSON para AJAX
  - `/extraer` - Endpoint para extraer ofertas

- **`dashboard.py`**:
  - `/dashboard` - Dashboard principal
  - `/estadisticas` - Página de estadísticas

### 2. Services

**Responsabilidad**: Contener la lógica de negocio y acceso a datos.

- **`database_service.py`** (MongoDBManager):
  - Conexión a MongoDB
  - CRUD de ofertas
  - Gestión de usuarios
  - Agregaciones y estadísticas
  - Índices optimizados

- **`scraping_service.py`** (ScrapingService):
  - Extracción de ofertas de portales web
  - Validación y normalización
  - Ejecutable independiente
  - Manejo de errores y reintentos

### 3. Utils

**Responsabilidad**: Funciones auxiliares reutilizables.

- **`validators.py`**:
  - `validate_oferta_data()` - Validar datos de oferta
  - `validate_user_data()` - Validar datos de usuario

- **`helpers.py`**:
  - `format_date()` - Formatear fechas
  - `generate_oferta_id()` - Generar IDs únicos
  - `truncate_text()` - Truncar textos

### 4. Config

**Responsabilidad**: Configuración centralizada del sistema.

- **`settings.py`** (Config):
  - Configuración de Flask
  - Configuración de MongoDB
  - URLs de portales
  - Parámetros de scraping
  - Variables de entorno

## 🚀 Inicialización de la Aplicación

### Factory Pattern

La aplicación se crea mediante `create_app()` en `app/__init__.py`:

```python
from app import create_app
from config.settings import Config

app = create_app(Config)
```

**Ventajas**:
- Fácil testing (crear múltiples instancias)
- Configuración por ambiente
- Inicialización controlada

### Punto de Entrada

`run.py` es el punto de entrada principal:

```bash
python run.py
```

## 🔌 Integración de Componentes

### 1. Inicialización de Base de Datos

```python
# En app/__init__.py
def initialize_database(config_class, logger):
    db_manager = MongoDBManager(config_class.MONGODB_URI)
    # Crear usuario admin si no existe
```

### 2. Registro de Blueprints

```python
# En app/__init__.py
app.register_blueprint(auth_bp)
app.register_blueprint(ofertas_bp)
app.register_blueprint(dashboard_bp)
```

### 3. Uso de Servicios en Controladores

```python
# En app/controllers/ofertas.py
from app.services.database_service import MongoDBManager

def get_db_manager():
    return MongoDBManager(Config.MONGODB_URI)
```

## 📊 Ventajas de esta Arquitectura

1. **Mantenibilidad**: Código organizado y fácil de encontrar
2. **Escalabilidad**: Fácil agregar nuevas funcionalidades
3. **Testabilidad**: Componentes aislados y testeables
4. **Reutilización**: Servicios y utilidades reutilizables
5. **Separación de Concerns**: Cada capa tiene su responsabilidad

## 🔄 Migración desde Estructura Antigua

### Archivos Eliminados (limpieza completada)

- ✅ `app.py` (raíz) → Reemplazado por `run.py` + `app/__init__.py`
- ✅ `config.py` (raíz) → Movido a `config/settings.py`
- ✅ `database.py` - SQL Server (eliminado, ya no se usa)
- ✅ `extractor_simple.py` - Extractor antiguo (eliminado)
- ✅ `01_create_database.sql` - Script SQL (eliminado)
- ✅ `migrate_to_mongodb.py` - Script de migración (eliminado, ya no necesario)

## 🧪 Testing (Futuro)

Estructura propuesta para tests:

```
tests/
├── __init__.py
├── test_controllers/
│   ├── test_auth.py
│   ├── test_ofertas.py
│   └── test_dashboard.py
├── test_services/
│   ├── test_database_service.py
│   └── test_scraping_service.py
└── test_utils/
    ├── test_validators.py
    └── test_helpers.py
```

## 📝 Convenciones de Código

1. **Nombres de archivos**: snake_case
2. **Nombres de clases**: PascalCase
3. **Nombres de funciones**: snake_case
4. **Imports**: Absolutos desde la raíz del proyecto
5. **Docstrings**: En todas las funciones y clases públicas

## 🔐 Seguridad

- Autenticación mediante sesiones Flask
- Contraseñas hasheadas con Werkzeug
- Validación de entrada en controladores
- Sanitización de datos en servicios

---

**Arquitectura diseñada para escalabilidad y mantenibilidad** 🏗️

