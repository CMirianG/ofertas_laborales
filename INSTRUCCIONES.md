# 🚀 Instrucciones para Ejecutar la Aplicación Simplificada

## ✅ Dependencias Instaladas

Las dependencias principales ya están instaladas:
- ✅ Flask
- ✅ Werkzeug  
- ✅ requests
- ✅ beautifulsoup4
- ✅ pymongo
- ✅ python-dotenv

## ⚡ Inicio Rápido

### Opción 1: Ejecutar directamente (RECOMENDADO)

```bash
python app.py
```

### Opción 2: Usar run.py

```bash
python run.py
```

Ambos métodos funcionan. La aplicación se ejecutará en **http://127.0.0.1:5000**

## 📋 Credenciales

- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 🗂️ Estructura Simplificada

```
ofertas_laborales/
├── app.py              ⭐ Aplicación Flask completa (TODO EN UNO)
├── run.py              → Ejecuta app.py
├── requirements.txt    → Dependencias (actualizado)
│
├── app/                → Carpeta con recursos
│   ├── templates/      → Plantillas HTML
│   └── static/         → CSS y JS
│
└── config/             → Configuración (opcional)
    └── settings.py
```

## 🔑 Características

✅ **Todo el código principal está en `app.py`**
- Fácil de entender
- Fácil de modificar
- Sin complejidad innecesaria

✅ **Funciona con o sin MongoDB**
- Si MongoDB no está disponible, funciona en modo limitado
- Login de emergencia: admin/admin123

✅ **Interfaz moderna con Bootstrap 5**
- Diseño responsivo
- Bonito y funcional

## 🔧 Configuración

### MongoDB (Opcional pero Recomendado)

Si tienes MongoDB instalado, la aplicación lo usará automáticamente:
- URI por defecto: `mongodb://localhost:27017/`
- Base de datos: `ofertas_laborales`

Para cambiar la configuración, crea un archivo `.env`:
```env
MONGODB_URI=mongodb://localhost:27017/
SECRET_KEY=tu-clave-secreta
FLASK_DEBUG=True
```

## 🐛 Solución de Problemas

### Error: ModuleNotFoundError: No module named 'flask'

Si ves este error, instala las dependencias:

```bash
pip install Flask Werkzeug requests beautifulsoup4 pymongo python-dotenv
```

O instala desde requirements.txt:
```bash
pip install -r requirements.txt
```

**Nota**: Si `lxml` falla durante la instalación, no es problema. La aplicación funciona sin él usando `html.parser` por defecto.

### MongoDB no conecta

No es problema. La aplicación funciona sin MongoDB, solo en modo limitado.
- Login de emergencia: `admin` / `admin123`
- Funciones básicas disponibles

### Error al ejecutar

Asegúrate de estar en el directorio correcto:
```bash
cd c:\Users\HP\Documents\GitHub\ofertas_laborales
python app.py
```

### Puerto 5000 ocupado

Si el puerto 5000 está ocupado, puedes cambiar el puerto editando `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar a 5001
```

## 📝 Notas Importantes

- **Versión simplificada**: Todo está en un solo archivo principal (`app.py`)
- **Fácil de modificar**: No hay capas complejas
- **Funcional**: Tiene todas las características principales
- **Bonito**: Interfaz moderna con Bootstrap 5
- **Sin lxml**: Si falla la instalación de lxml, la app funciona igual

## 🎯 Siguiente Paso

1. Ejecuta la aplicación: `python app.py`
2. Abre tu navegador en: http://127.0.0.1:5000
3. Inicia sesión con: `admin` / `admin123`
4. ¡Listo! 🎉

---

**¡La aplicación está lista para usar!** 🚀
