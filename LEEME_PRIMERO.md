# 🚀 Sistema de Ofertas Laborales - Tacna

## ⚡ Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python app.py
```

### 3. Abrir en el Navegador

Abre: **http://127.0.0.1:5000**

**Credenciales:**
- Usuario: `admin`
- Contraseña: `admin123`

---

## 📋 Modos de Uso

### ✅ Modo Sin MongoDB (Solo Lectura)

**La aplicación funciona sin MongoDB**, pero con limitaciones:

- ✅ Ver dashboard
- ✅ Ver ofertas (si ya hay datos)
- ✅ Navegar por la interfaz
- ❌ **NO** extraer nuevas ofertas
- ❌ **NO** guardar datos

**Para usar este modo:**
- Simplemente ejecuta `python app.py`
- La aplicación funcionará en modo limitado
- Puedes iniciar sesión con `admin` / `admin123`

### 🔧 Modo Completo (Con MongoDB)

Para usar todas las funciones, incluyendo extraer ofertas:

1. **Instala MongoDB** (ver `INSTALAR_MONGODB.md`)
2. **Inicia el servicio MongoDB**
3. **Reinicia la aplicación**

**Con MongoDB puedes:**
- ✅ Extraer ofertas de portales web
- ✅ Guardar y gestionar ofertas
- ✅ Ver estadísticas completas
- ✅ Todas las funcionalidades

---

## 📦 Instalación de MongoDB

MongoDB es **OPCIONAL** pero necesario para extraer ofertas.

**Ver instrucciones detalladas en:** `INSTALAR_MONGODB.md`

**Opciones rápidas:**

1. **MongoDB Atlas (Recomendado para empezar):**
   - Gratis en la nube
   - No requiere instalación local
   - Ve a: https://www.mongodb.com/cloud/atlas

2. **MongoDB Local:**
   - Descarga de: https://www.mongodb.com/try/download/community
   - Instala y ejecuta como servicio

---

## 🐛 Solución de Problemas

### Error 500 al extraer ofertas

**Causa más común:** MongoDB no está instalado o no está corriendo.

**Solución:**
- Instala MongoDB (ver `INSTALAR_MONGODB.md`)
- O usa la aplicación en modo solo lectura (sin extraer ofertas)

### Error de conexión a MongoDB

- Verifica que MongoDB esté corriendo
- En Windows: `Get-Service | Where-Object {$_.DisplayName -like "*Mongo*"}`
- Revisa los logs al iniciar la aplicación

### Error al instalar dependencias

Si falla la instalación de `lxml`:
- No es crítico, la aplicación funciona sin él
- Continúa con el resto de las dependencias

---

## 📁 Estructura

```
ofertas_laborales/
├── app.py              ⭐ Aplicación principal (TODO EN UNO)
├── run.py              → Ejecuta app.py
├── requirements.txt    → Dependencias
├── INSTALAR_MONGODB.md → Instrucciones MongoDB
├── SOLUCION_ERRORES.md → Solución de problemas
└── app/
    ├── templates/      → Plantillas HTML
    └── static/         → CSS y JS
```

---

## ✨ Características

- ✅ Interfaz moderna con Bootstrap 5
- ✅ Dashboard con estadísticas
- ✅ Filtros de búsqueda
- ✅ Extracción de ofertas (requiere MongoDB)
- ✅ Vista detallada de ofertas
- ✅ Responsive design

---

## 📝 Notas

- **Sin MongoDB:** Funciona en modo lectura
- **Con MongoDB:** Funcionalidad completa
- **Fácil de modificar:** Todo en `app.py`
- **Bonito y funcional:** Interfaz moderna

---

**¡Listo para usar!** 🎉

