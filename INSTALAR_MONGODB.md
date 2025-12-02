# 📦 Instalación de MongoDB (Opcional)

MongoDB es necesario **SOLO** para extraer ofertas de los portales web. La aplicación funciona sin MongoDB para visualizar datos, pero no podrás extraer nuevas ofertas.

## ✅ Opciones

### Opción 1: Instalar MongoDB Localmente (Recomendado para desarrollo)

#### Windows:

1. **Descargar MongoDB Community Server:**
   - Ve a: https://www.mongodb.com/try/download/community
   - Selecciona:
     - Version: Latest (o 7.0)
     - Platform: Windows
     - Package: MSI

2. **Instalar:**
   - Ejecuta el instalador
   - Selecciona "Complete" installation
   - Marca "Install MongoDB as a Service"
   - El servicio se llamará `MongoDB` o `MongoDB Server`

3. **Verificar instalación:**
   ```powershell
   # Verificar que el servicio existe
   Get-Service | Where-Object {$_.DisplayName -like "*Mongo*"}
   
   # Iniciar el servicio
   net start MongoDB
   # o
   Start-Service MongoDB
   ```

4. **Probar conexión:**
   ```powershell
   # MongoDB debería estar corriendo en localhost:27017
   # La aplicación se conectará automáticamente
   ```

### Opción 2: MongoDB Atlas (Gratis, en la nube)

1. **Crear cuenta gratuita:**
   - Ve a: https://www.mongodb.com/cloud/atlas/register
   - Crea una cuenta (gratis para siempre con límites)

2. **Crear cluster:**
   - Crea un cluster gratuito (M0)
   - Selecciona la región más cercana

3. **Obtener cadena de conexión:**
   - Ve a "Connect" → "Connect your application"
   - Copia la cadena de conexión (URI)

4. **Configurar en la aplicación:**
   - Crea un archivo `.env` en la raíz del proyecto:
     ```
     MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/?retryWrites=true&w=majority
     ```
   - Reemplaza `usuario` y `contraseña` con tus credenciales

### Opción 3: Usar Docker (Si tienes Docker instalado)

```bash
# Ejecutar MongoDB en un contenedor
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Para iniciarlo después:
docker start mongodb
```

## 🔍 Verificar si MongoDB está corriendo

**Windows:**
```powershell
# Ver servicios de MongoDB
Get-Service | Where-Object {$_.DisplayName -like "*Mongo*"}

# Verificar conexión
Test-NetConnection -ComputerName localhost -Port 27017
```

**Verificar en la aplicación:**
- Al iniciar la aplicación, verás en la consola:
  - `✓ Conexión a MongoDB exitosa` → MongoDB está funcionando
  - `✗ Error conectando a MongoDB` → MongoDB no está disponible

## ⚠️ Importante

- **Sin MongoDB:** La aplicación funciona pero NO podrás extraer ofertas
- **Con MongoDB:** Puedes extraer ofertas de los portales web

## 🚀 Inicio Rápido (Sin MongoDB)

Si solo quieres probar la aplicación sin instalar MongoDB:
1. Ejecuta la aplicación: `python app.py`
2. Inicia sesión con: `admin` / `admin123`
3. Podrás ver el dashboard y navegar, pero NO extraer ofertas

Para extraer ofertas, necesitas MongoDB instalado y corriendo.

