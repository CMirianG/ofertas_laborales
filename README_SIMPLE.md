# Sistema de Ofertas Laborales - Tacna (Versión Simplificada)

Aplicación web simple y funcional para gestionar ofertas laborales en Tacna, Perú.

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Asegurarse que MongoDB esté corriendo
# Windows:
net start MongoDB

# Linux/Mac:
sudo systemctl start mongod
```

### 2. Ejecutar

```bash
python run.py
```

Abrir navegador en: **http://127.0.0.1:5000**

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📁 Estructura Simplificada

```
ofertas_laborales/
├── app.py              # Aplicación Flask principal (TODO EN UNO)
├── run.py              # Punto de entrada
├── requirements.txt    # Dependencias
├── app/
│   ├── templates/      # Plantillas HTML
│   └── static/         # CSS y JS
└── config/
    └── settings.py     # Configuración
```

## ✨ Características

- ✅ Login simple
- ✅ Dashboard con estadísticas
- ✅ Lista de ofertas con filtros
- ✅ Vista detallada de ofertas
- ✅ Estadísticas
- ✅ Extracción de ofertas (opcional)

## 🔧 Configuración

La aplicación usa MongoDB. Si no tienes MongoDB, la aplicación funciona en modo limitado.

Variables de entorno opcionales (archivo `.env`):
```env
MONGODB_URI=mongodb://localhost:27017/
SECRET_KEY=tu-clave-secreta
FLASK_DEBUG=True
```

## 📝 Notas

- Versión simplificada: todo el código principal está en `app.py`
- Fácil de entender y modificar
- Diseño moderno con Bootstrap 5
- Compatible con MongoDB (opcional)

---

**Desarrollado para la ciudad de Tacna, Perú** 🇵🇪

