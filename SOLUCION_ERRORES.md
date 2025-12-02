# 🔧 Solución de Errores - Extracción de Ofertas

## Problema: Error 500 al extraer ofertas

Si ves un error 500 al intentar extraer ofertas, sigue estos pasos:

### 1. Verificar MongoDB

El error más común es que MongoDB no esté corriendo:

**Windows:**
```bash
# Verificar si MongoDB está corriendo
net start MongoDB

# Si no está corriendo, iniciarlo:
net start MongoDB
```

**Linux/Mac:**
```bash
# Verificar estado
sudo systemctl status mongod

# Iniciar si no está corriendo
sudo systemctl start mongod
```

### 2. Verificar los logs del servidor

Cuando ejecutas la aplicación, revisa la consola donde está corriendo. Busca mensajes que digan:
- `Error conectando a MongoDB`
- `Error en extracción`
- `Traceback` (esto muestra dónde está fallando)

### 3. Verificar las dependencias

Asegúrate de que todas las dependencias estén instaladas:

```bash
pip install Flask Werkzeug requests beautifulsoup4 pymongo python-dotenv
```

### 4. Verificar el servicio de scraping

El servicio de scraping puede fallar si:
- No hay conexión a internet
- Los portales web han cambiado su estructura
- Hay bloqueos por parte de los portales

### 5. Mensajes de error comunes

**"MongoDB no disponible"**
- Solución: Inicia MongoDB antes de extraer ofertas

**"Error durante la extracción"**
- Solución: Revisa los logs para ver qué portal está fallando

**"Módulo no encontrado"**
- Solución: Verifica que todos los archivos estén en su lugar

### 6. Modo de prueba

Para probar sin extraer de portales reales, puedes crear ofertas de prueba manualmente en MongoDB o desactivar temporalmente el scraping.

---

**Si el problema persiste**, comparte:
1. El mensaje de error completo de la consola del servidor
2. El mensaje que aparece en el navegador
3. Si MongoDB está corriendo o no

