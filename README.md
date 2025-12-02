# Sistema de Ofertas Laborales - Tacna

Sistema web para la extracción, gestión y visualización de ofertas laborales en la ciudad de Tacna, Perú.

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura por capas bien definida:

```
Ofertas_Laborales/
├── app/                          # Aplicación principal
│   ├── __init__.py              # Factory pattern para Flask
│   ├── controllers/             # Controladores (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py              # Autenticación
│   │   ├── ofertas.py           # Gestión de ofertas
│   │   └── dashboard.py         # Dashboard y estadísticas
│   ├── services/                # Servicios (Lógica de negocio)
│   │   ├── __init__.py
│   │   ├── database_service.py  # Gestor de MongoDB
│   │   └── scraping_service.py  # Servicio de scraping
│   ├── utils/                    # Utilidades
│   │   ├── __init__.py
│   │   ├── validators.py        # Validadores de datos
│   │   └── helpers.py           # Funciones auxiliares
│   ├── templates/               # Plantillas HTML
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── ofertas.html
│   │   ├── ver_oferta.html
│   │   └── estadisticas.html
│   └── static/                  # Archivos estáticos
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── config/                       # Configuración
│   ├── __init__.py
│   └── settings.py              # Configuración del sistema
├── scripts/                       # Scripts de utilidad
│   └── migrate_to_mongodb.py    # Script de migración
├── tests/                        # Tests (opcional)
├── requirements.txt              # Dependencias
├── .env.example                  # Ejemplo de variables de entorno
└── run.py                        # Punto de entrada principal
```

## 📋 Capas de la Arquitectura

### 1. **Capa de Presentación** (`app/controllers/`)
- **Blueprints de Flask** para organizar rutas
- Separación por funcionalidad (auth, ofertas, dashboard)
- Decoradores para autenticación

### 2. **Capa de Servicios** (`app/services/`)
- **Lógica de negocio** separada de los controladores
- `database_service.py`: Gestión de MongoDB
- `scraping_service.py`: Extracción de ofertas

### 3. **Capa de Utilidades** (`app/utils/`)
- Validadores de datos
- Funciones auxiliares
- Helpers reutilizables

### 4. **Capa de Configuración** (`config/`)
- Configuración centralizada
- Variables de entorno
- Settings por ambiente

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Asegurarse que MongoDB esté corriendo
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

### 2. Configuración

Crear archivo `.env` (opcional):

```env
MONGODB_URI=mongodb://localhost:27017/
SECRET_KEY=tu-clave-secreta-super-segura
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### 3. Ejecutar

```bash
python run.py
```

Abrir navegador en: http://127.0.0.1:5000

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📦 Estructura de Módulos

### Controllers (Blueprints)

- **`auth.py`**: Maneja login, logout y autenticación
- **`ofertas.py`**: CRUD de ofertas, API, extracción
- **`dashboard.py`**: Dashboard principal y estadísticas

### Services

- **`database_service.py`**: 
  - Conexión a MongoDB
  - CRUD de ofertas y usuarios
  - Agregaciones y estadísticas
  
- **`scraping_service.py`**:
  - Extracción de ofertas de portales web
  - Validación y normalización de datos
  - Ejecutable independiente

### Utils

- **`validators.py`**: Validación de datos de ofertas y usuarios
- **`helpers.py`**: Funciones auxiliares (formateo, generación de IDs)

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `MONGODB_URI` | URI de conexión a MongoDB | `mongodb://localhost:27017/` |
| `SECRET_KEY` | Clave secreta de Flask | `dev-secret-key...` |
| `FLASK_DEBUG` | Modo debug | `False` |
| `FLASK_HOST` | Host del servidor | `0.0.0.0` |
| `FLASK_PORT` | Puerto del servidor | `5000` |
| `OFERTAS_PER_PAGE` | Ofertas por página | `20` |

### Ejecutar Scraping Independiente

```bash
# Desde la raíz del proyecto
python -m app.services.scraping_service --portals all

# O desde scripts
python scripts/scraping_service.py --portals all
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
python -m pytest tests/
```

## 📝 Principios de la Arquitectura

1. **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad única
2. **Factory Pattern**: Flask app creada mediante factory function
3. **Blueprints**: Rutas organizadas por funcionalidad
4. **Dependency Injection**: Servicios inyectados donde se necesitan
5. **Configuración Externa**: Variables de entorno para configuración


## 📚 Tecnologías

- **Backend**: Python 3.8+, Flask 2.3.3
- **Base de Datos**: MongoDB
- **Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## 🤝 Contribuir

1. Seguir la estructura de carpetas establecida
2. Usar Blueprints para nuevas rutas
3. Mantener servicios separados de controladores
4. Documentar funciones y clases

---

**Desarrollado para la ciudad de Tacna, Perú** 🇵🇪  
**Universidad Privada de Tacna (UPT)** 🎓  
**Oficina de Responsabilidad Social Universitaria (RSU)** 🤝

