# Sistema de Ofertas Laborales - Tacna

## 📋 Información del Proyecto

**Institución**: Universidad Privada de Tacna (UPT)  
**Oficina**: Responsabilidad Social Universitaria (RSU)  
**Tipo**: Prácticas Pre-Profesionales  
**Área**: Ingeniería de Sistemas  
**Objetivo**: Optimización de procesos mediante soluciones tecnológicas innovadoras

Sistema web para la extracción, gestión y visualización de ofertas laborales específicamente para la ciudad de Tacna, Perú. El sistema está diseñado para bachilleres y profesionales, con una interfaz intuitiva y funcionalidades avanzadas de búsqueda y filtrado.

## 📊 Especificación de Requisitos de Software

### Descripción del Problema

La Oficina de Responsabilidad Social Universitaria (RSU) de la UPT requiere un sistema automatizado para la gestión de ofertas laborales específicamente para la ciudad de Tacna. Actualmente, la búsqueda y gestión de oportunidades laborales se realiza de manera manual, lo que genera:

- **Ineficiencia**: Búsqueda manual en múltiples portales web
- **Desactualización**: Información no centralizada ni actualizada
- **Limitación geográfica**: Falta de enfoque específico en ofertas de Tacna
- **Gestión dispersa**: No existe un repositorio centralizado de ofertas
- **Tiempo excesivo**: Proceso manual que consume recursos humanos

### Objetivos de Negocios

1. **Automatizar** la extracción de ofertas laborales de portales web especializados
2. **Centralizar** la información de ofertas laborales en un sistema único
3. **Optimizar** el tiempo de búsqueda y gestión de oportunidades laborales
4. **Facilitar** el acceso a ofertas específicas para la región de Tacna
5. **Mejorar** la eficiencia de los procesos de la Oficina de RSU
6. **Proporcionar** estadísticas y análisis de tendencias del mercado laboral

### Objetivos de Diseño

1. **Interfaz Intuitiva**: Sistema fácil de usar para administradores y usuarios
2. **Escalabilidad**: Arquitectura que permita crecimiento futuro
3. **Confiabilidad**: Sistema estable con mínima intervención manual
4. **Seguridad**: Protección de datos y autenticación robusta
5. **Mantenibilidad**: Código limpio y documentado
6. **Rendimiento**: Respuesta rápida y eficiente

### Alcance del Proyecto

**Incluye:**
- Extracción automática de ofertas de portales web
- Sistema de gestión y visualización de ofertas
- Base de datos centralizada
- Interfaz web administrativa
- Sistema de autenticación
- Reportes y estadísticas

**No incluye:**
- Aplicación móvil
- Integración con redes sociales
- Sistema de notificaciones por email
- API pública para terceros
- Análisis predictivo con IA

### Viabilidad del Sistema

**Técnica**: ✅ **VIABLE**
- Tecnologías probadas y estables (Flask, SQL Server, BeautifulSoup)
- Arquitectura web estándar
- Integración con sistemas existentes

**Económica**: ✅ **VIABLE**
- Costos de desarrollo reducidos
- Infraestructura existente en UPT
- Sin licencias costosas de software

**Operacional**: ✅ **VIABLE**
- Personal técnico disponible
- Procesos claramente definidos
- Soporte institucional garantizado

## 🚀 Características Principales

- **📊 Extracción Automática**: Busca ofertas en múltiples portales especializados en empleos peruanos
- **🎯 Filtrado Específico**: Solo ofertas para Tacna, Perú
- **💻 Interfaz Intuitiva**: Dashboard moderno con gráficos y estadísticas
- **🔍 Búsqueda Avanzada**: Filtros por nivel académico, modalidad, empresa, etc.
- **🗄️ Base de Datos SQL Server**: Almacenamiento robusto y escalable
- **🔐 Sistema de Login**: Autenticación segura con usuario administrador
- **🔄 Sistema de Fallback**: Ofertas de ejemplo cuando los portales no están disponibles
- **⚡ Sin Dependencias de IA**: Sistema simplificado y confiable

## 📋 Campos de Ofertas Extraídas

Cada oferta incluye los siguientes campos normalizados:

- **ID**: Identificador único generado por el sistema
- **Título de Oferta**: Título de la oferta (máx. 80 caracteres)
- **Empresa**: Nombre de la empresa/organización
- **Nivel Académico**: Bachiller, Profesional o Técnico
- **Puesto**: Cargo o posición
- **Experiencia Mínima**: Años de experiencia requeridos
- **Conocimientos Clave**: 3-5 keywords relevantes
- **Responsabilidades**: Descripción breve (máx. 200 caracteres)
- **Modalidad**: Presencial, Remoto o Híbrido
- **Ubicación**: Tacna con distrito/localidad si está disponible
- **Jornada**: Tiempo completo, Medio tiempo, Por horas
- **Salario**: Monto en PEN o "No especificado"
- **Fechas**: Publicación y cierre (formato YYYY-MM-DD)
- **Cómo Postular**: Instrucciones para aplicar
- **URL Original**: Enlace a la oferta original
- **Documentos Requeridos**: Lista de documentos necesarios
- **Contacto**: Email o teléfono si está disponible
- **Etiquetas**: Tags adicionales (urgente, pasantía, etc.)
- **Fuente**: Portal donde se encontró la oferta

## 📋 Información obtenida del Levantamiento de Información

### Análisis de Procesos

**Proceso Actual (Manual):**
1. Búsqueda manual en portales web
2. Revisión individual de ofertas
3. Verificación de ubicación (Tacna)
4. Extracción manual de datos
5. Almacenamiento en documentos
6. Gestión dispersa de información

**Problemas Identificados:**
- Tiempo excesivo en búsqueda (2-3 horas diarias)
- Información desactualizada
- Falta de estandarización
- Duplicación de esfuerzos
- Dificultad para generar reportes

### Diagrama del Proceso Propuesto – Diagrama de Actividades Inicial

```
[Inicio] → [Configurar Sistema] → [Ejecutar Extracción] → [Validar Datos] → [Almacenar en BD] → [Generar Reportes] → [Fin]
     ↓              ↓                    ↓                ↓                ↓              ↓
[Usuario]    [Administrador]    [Sistema Automático]  [Validaciones]  [SQL Server]  [Dashboard]
```

## 🌐 Fuentes de Datos

El sistema extrae ofertas laborales de los siguientes portales especializados:

### Portales Principales
- **Computrabajo Perú**: Portal líder en empleos en Perú
- **Bumeran Perú**: Portal especializado en empleos profesionales
- **Indeed Perú**: Portal internacional con ofertas locales
- **Trabajos.pe**: Portal de empleos peruanos

### Características de Extracción
- **Filtrado Geográfico**: Solo ofertas ubicadas en Tacna, Perú
- **Múltiples Estrategias**: Diferentes selectores CSS para mayor robustez
- **Deduplicación**: Elimina ofertas duplicadas entre portales
- **Validación de Datos**: Verifica la calidad y completitud de la información
- **Ofertas de Ejemplo**: Sistema de fallback con ofertas realistas para Tacna

## 📋 Especificación de Requerimientos de Software

### Cuadro de Requerimientos Funcionales Inicial

| ID | Requerimiento | Descripción | Prioridad |
|----|---------------|-------------|-----------|
| RF-001 | Extracción Automática | Sistema debe extraer ofertas de portales web | Alta |
| RF-002 | Filtrado Geográfico | Solo ofertas de Tacna, Perú | Alta |
| RF-003 | Gestión de Usuarios | Sistema de login y autenticación | Media |
| RF-004 | Visualización de Ofertas | Lista y detalles de ofertas | Alta |
| RF-005 | Búsqueda y Filtros | Búsqueda por múltiples criterios | Media |
| RF-006 | Reportes y Estadísticas | Generación de reportes | Baja |

### Cuadro de Requerimientos No Funcionales

| ID | Requerimiento | Descripción | Prioridad |
|----|---------------|-------------|-----------|
| RNF-001 | Rendimiento | Respuesta < 3 segundos | Alta |
| RNF-002 | Disponibilidad | 99% de tiempo activo | Alta |
| RNF-003 | Seguridad | Autenticación y encriptación | Alta |
| RNF-004 | Escalabilidad | Soporte para 100+ usuarios | Media |
| RNF-005 | Mantenibilidad | Código documentado y modular | Media |
| RNF-006 | Usabilidad | Interfaz intuitiva | Media |

### Cuadro de Requerimientos Funcionales Final

| ID | Requerimiento | Descripción | Estado |
|----|---------------|-------------|--------|
| RF-001 | Extracción de Portales | Extraer ofertas de Computrabajo, Indeed, Bumeran, Trabajos.pe | ✅ Implementado |
| RF-002 | Filtrado por Ubicación | Solo ofertas que mencionen "Tacna" | ✅ Implementado |
| RF-003 | Sistema de Login | Autenticación con usuario/contraseña | ✅ Implementado |
| RF-004 | Dashboard Principal | Vista general con estadísticas | ✅ Implementado |
| RF-005 | Lista de Ofertas | Visualización en tabla con paginación | ✅ Implementado |
| RF-006 | Detalles de Oferta | Vista completa de cada oferta | ✅ Implementado |
| RF-007 | Búsqueda Avanzada | Filtros por empresa, nivel académico, modalidad | ✅ Implementado |
| RF-008 | Estadísticas | Gráficos de distribución por fuente y nivel | ✅ Implementado |
| RF-009 | Gestión de Base de Datos | CRUD completo de ofertas | ✅ Implementado |
| RF-010 | Sistema de Fallback | Ofertas de ejemplo cuando portales no responden | ✅ Implementado |

### Reglas de Negocio

1. **RN-001**: Solo se almacenan ofertas que mencionen "Tacna" en la ubicación
2. **RN-002**: Las ofertas duplicadas se eliminan automáticamente por URL
3. **RN-003**: El sistema debe ejecutarse al menos una vez al día
4. **RN-004**: Solo usuarios autenticados pueden acceder al sistema
5. **RN-005**: Los datos de ofertas se mantienen por un período mínimo de 6 meses
6. **RN-006**: Las ofertas de ejemplo se marcan claramente como tales
7. **RN-007**: El sistema debe validar la integridad de los datos extraídos
8. **RN-008**: Los reportes se generan en tiempo real

## 🛠️ Instalación

### Requisitos Previos

- Python 3.8 o superior
- SQL Server (configurado en 161.132.50.113)
- Navegador web moderno

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes git instalado
   git clone <url-del-repositorio>
   cd Ofertas_Laborales
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicializar la base de datos**
   ```bash
   python init_database.py
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

5. **Acceder al sistema**
   - Abrir navegador en: http://localhost:5000
   - Usuario: `admin`
   - Contraseña: `admin123`

## 📁 Estructura del Proyecto

```
Ofertas_Laborales/
├── app.py                    # Aplicación Flask principal
├── config.py                # Configuración del sistema
├── database.py              # Gestión de base de datos SQL Server
├── extractor_simple.py      # Extractor simplificado de ofertas
├── init_database.py         # Script de inicialización
├── requirements.txt         # Dependencias de Python
├── README.md               # Este archivo
├── run_test.py             # Script para ejecutar y probar
├── test_extractor_simple.py # Pruebas del extractor
├── test_app_completa.py    # Pruebas de la aplicación
├── CAMBIOS_REALIZADOS.md   # Documentación de cambios
├── templates/              # Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── ofertas.html
│   ├── ver_oferta.html
│   └── estadisticas.html
└── static/                 # Archivos estáticos
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🔧 Configuración

### Base de Datos SQL Server

El sistema está configurado para conectarse a:
- **Servidor**: 161.132.50.113
- **Usuario**: sa
- **Contraseña**: Upt2025ii
- **Base de Datos**: OfertasLaborales

### Personalización

Puedes modificar la configuración en `config.py`:

```python
# Configurar fuentes de extracción
PORTALS = {
    'computrabajo': 'https://pe.computrabajo.com/empleos-en-tacna',
    'bumeran': 'https://www.bumeran.com.pe/en-tacna/empleos.html',
    'indeed': 'https://pe.indeed.com/jobs?q=&l=Tacna%2C+Tacna',
    'trabajos_pe': 'https://www.trabajos.pe/trabajo-tacna'
}

# Modificar palabras clave de búsqueda
TACNA_KEYWORDS = ['tacna', 'tacneño', 'tacneña']
```

## 👥 Fase de Desarrollo

### Perfiles de Usuario

#### 1. Administrador del Sistema
- **Descripción**: Personal de la Oficina de RSU responsable de la gestión del sistema
- **Responsabilidades**:
  - Configurar y ejecutar extracciones automáticas
  - Gestionar usuarios del sistema
  - Monitorear el funcionamiento del sistema
  - Generar reportes y estadísticas
- **Acceso**: Completo a todas las funcionalidades
- **Casos de Uso**: Login, Dashboard, Extracción, Gestión de Ofertas, Estadísticas

#### 2. Usuario Final
- **Descripción**: Estudiantes, egresados y profesionales que buscan oportunidades laborales
- **Responsabilidades**:
  - Consultar ofertas laborales disponibles
  - Buscar ofertas por criterios específicos
  - Acceder a información detallada de ofertas
- **Acceso**: Solo lectura de ofertas
- **Casos de Uso**: Login, Búsqueda de Ofertas, Visualización de Detalles

### Modelo Conceptual

**Entidades Principales:**
- **Usuario**: Información de usuarios del sistema
- **Oferta Laboral**: Datos de las ofertas extraídas
- **Portal**: Fuentes de extracción de ofertas
- **Sesión**: Control de acceso al sistema

**Relaciones:**
- Usuario → Oferta Laboral (consulta)
- Portal → Oferta Laboral (origen)
- Usuario → Sesión (autenticación)

### Diagrama de Paquetes

```
Sistema Ofertas Laborales
├── Presentación
│   ├── Templates HTML
│   ├── CSS/JS
│   └── Rutas Flask
├── Lógica de Negocio
│   ├── Extractor de Ofertas
│   ├── Gestión de Usuarios
│   └── Validaciones
├── Acceso a Datos
│   ├── Database Manager
│   ├── Modelos de Datos
│   └── Consultas SQL
└── Configuración
    ├── Config.py
    ├── Requirements.txt
    └── Scripts de Inicialización
```

### Diagrama de Casos de Uso

```
[Usuario] → [Login] → [Dashboard]
    ↓
[Buscar Ofertas] → [Ver Detalles] → [Filtrar Resultados]
    ↓
[Administrador] → [Extraer Ofertas] → [Gestionar Sistema]
    ↓
[Generar Reportes] → [Ver Estadísticas]
```

### Escenarios de Caso de Uso (Narrativa)

#### CU-001: Autenticación de Usuario
**Actor**: Usuario/Administrador  
**Precondición**: Sistema en funcionamiento  
**Flujo Principal**:
1. Usuario accede al sistema
2. Sistema muestra formulario de login
3. Usuario ingresa credenciales
4. Sistema valida credenciales
5. Sistema redirige al dashboard
**Postcondición**: Usuario autenticado en el sistema

#### CU-002: Extracción de Ofertas
**Actor**: Administrador  
**Precondición**: Usuario autenticado como administrador  
**Flujo Principal**:
1. Administrador accede al dashboard
2. Administrador inicia proceso de extracción
3. Sistema extrae ofertas de portales web
4. Sistema valida y almacena ofertas
5. Sistema muestra resultados de extracción
**Postcondición**: Nuevas ofertas disponibles en el sistema

#### CU-003: Búsqueda de Ofertas
**Actor**: Usuario  
**Precondición**: Usuario autenticado  
**Flujo Principal**:
1. Usuario accede a lista de ofertas
2. Usuario aplica filtros de búsqueda
3. Sistema muestra ofertas filtradas
4. Usuario selecciona oferta de interés
5. Sistema muestra detalles completos
**Postcondición**: Usuario visualiza información de oferta

## 🎯 Uso del Sistema

### 1. Dashboard Principal
- Vista general de estadísticas
- Gráficos de distribución por fuente y nivel académico
- Lista de ofertas recientes
- Botón para extraer nuevas ofertas

### 2. Gestión de Ofertas
- Lista completa de ofertas con filtros
- Búsqueda por título, empresa, nivel académico
- Vista de tabla o tarjetas
- Enlaces a ofertas originales

### 3. Detalles de Oferta
- Información completa de cada oferta
- Datos de contacto y postulación
- Enlaces a documentos y formularios
- Opciones de compartir e imprimir

### 4. Estadísticas
- Gráficos interactivos
- Distribución por nivel académico y modalidad
- Top empresas con más ofertas
- Análisis temporal

## 🔍 Extracción de Ofertas

### Portales Soportados

1. **Computrabajo**: Portal principal de empleos en Perú
2. **Indeed**: Motor de búsqueda internacional
3. **Bumeran**: Portal especializado en Latinoamérica
4. **Trabajos.pe**: Portal de empleos peruanos

### Proceso de Extracción

1. El sistema accede a cada portal web
2. Busca ofertas que mencionen "Tacna" en la ubicación
3. Extrae y normaliza la información según los campos requeridos
4. Valida y limpia los datos
5. Almacena en la base de datos SQL Server
6. Elimina duplicados por URL
7. Si no encuentra ofertas reales, crea ofertas de ejemplo para Tacna

### Ofertas de Ejemplo

El sistema incluye ofertas de ejemplo realistas para Tacna cuando los portales no están disponibles:

- **Asistente Administrativo** - Empresa Local Tacna
- **Vendedor** - Comercial Tacna S.A.C.
- **Contador** - Estudio Contable Tacna
- **Técnico en Enfermería** - Clínica Tacna
- **Operario de Producción** - Industria Tacna S.A.C.

## 🛡️ Seguridad

- Autenticación con hash de contraseñas
- Sesiones seguras con Flask
- Validación de entrada de datos
- Conexión encriptada a SQL Server

## 🗄️ Modelo Lógico

### Análisis de Objetos

**Clases Principales:**

#### 1. Usuario
- **Atributos**: id, username, password_hash, email, role, created_at, updated_at
- **Métodos**: authenticate(), has_permission(), to_dict()

#### 2. OfertaLaboral
- **Atributos**: id, titulo_oferta, empresa, nivel_academico, puesto, experiencia_minima_anios, conocimientos_clave, responsabilidades_breve, modalidad, ubicacion, jornada, salario, fecha_publicacion, fecha_cierre, como_postular, url_oferta, documentos_requeridos, contacto, etiquetas, fuente, fecha_estimacion, created_at, updated_at
- **Métodos**: validate(), normalize_data(), to_dict()

#### 3. DatabaseManager
- **Atributos**: connection, cursor
- **Métodos**: connect(), create_tables(), insert_oferta(), get_ofertas(), update_oferta(), delete_oferta()

#### 4. SimpleOfertaExtractor
- **Atributos**: session, logger
- **Métodos**: extract_all_ofertas(), extract_from_computrabajo(), extract_from_indeed(), extract_from_bumeran(), extract_from_trabajos_pe()

### Diagrama de Entidad-Relación (Análisis)

```
┌─────────────────┐    ┌──────────────────┐
│     USUARIO     │    │  OFERTA_LABORAL  │
├─────────────────┤    ├──────────────────┤
│ id (PK)         │    │ id (PK)          │
│ username        │    │ titulo_oferta    │
│ password_hash   │    │ empresa          │
│ email           │    │ nivel_academico  │
│ role            │    │ puesto           │
│ created_at      │    │ experiencia_min  │
│ updated_at      │    │ conocimientos    │
└─────────────────┘    │ responsabilidades│
                       │ modalidad        │
                       │ ubicacion        │
                       │ jornada          │
                       │ salario          │
                       │ fecha_publicacion│
                       │ fecha_cierre     │
                       │ como_postular    │
                       │ url_oferta       │
                       │ documentos_req   │
                       │ contacto         │
                       │ etiquetas        │
                       │ fuente           │
                       │ fecha_estimacion │
                       │ created_at       │
                       │ updated_at       │
                       └──────────────────┘
```

### Diagrama de Secuencia

#### Secuencia: Extracción de Ofertas

```
[Administrador] → [Sistema] → [Extractor] → [Portal Web] → [Base de Datos]
       │              │            │             │              │
       │ 1. Iniciar   │            │             │              │
       ├─────────────→│            │             │              │
       │              │ 2. Ejecutar│             │              │
       │              ├───────────→│             │              │
       │              │            │ 3. Consultar│              │
       │              │            ├────────────→│              │
       │              │            │ 4. Respuesta│              │
       │              │            │←────────────┤              │
       │              │            │ 5. Procesar │              │
       │              │            │ 6. Validar  │              │
       │              │            │ 7. Almacenar│              │
       │              │            ├─────────────┼─────────────→│
       │              │            │ 8. Confirmar│              │
       │              │            │←────────────┼──────────────┤
       │              │ 9. Resultado│             │              │
       │              │←───────────┤             │              │
       │ 10. Mostrar  │            │             │              │
       │←─────────────┤            │             │              │
```

### Diagrama de Clases

```
┌─────────────────────────────────────────────────────────────┐
│                    Sistema Ofertas Laborales                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │     Usuario     │    │  OfertaLaboral   │               │
│  ├─────────────────┤    ├──────────────────┤               │
│  │ - id: int       │    │ - id: str        │               │
│  │ - username: str │    │ - titulo: str    │               │
│  │ - password: str │    │ - empresa: str   │               │
│  │ - email: str    │    │ - ubicacion: str │               │
│  │ - role: str     │    │ - salario: str   │               │
│  ├─────────────────┤    │ - fuente: str    │               │
│  │ + authenticate()│    ├──────────────────┤               │
│  │ + has_permission│    │ + validate()     │               │
│  │ + to_dict()     │    │ + normalize()    │               │
│  └─────────────────┘    │ + to_dict()      │               │
│                         └──────────────────┘               │
│                                                             │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │ DatabaseManager │    │SimpleOfertaExtr. │               │
│  ├─────────────────┤    ├──────────────────┤               │
│  │ - connection    │    │ - session        │               │
│  │ - cursor        │    │ - logger         │               │
│  ├─────────────────┤    ├──────────────────┤               │
│  │ + connect()     │    │ + extract_all()  │               │
│  │ + create_tables │    │ + extract_comp.  │               │
│  │ + insert_oferta │    │ + extract_indeed │               │
│  │ + get_ofertas() │    │ + extract_bumer. │               │
│  │ + update_oferta │    │ + extract_trab.  │               │
│  │ + delete_oferta │    │ + validate_data  │               │
│  └─────────────────┘    └──────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Base de Datos

### Tablas Principales

- **usuarios**: Gestión de usuarios del sistema
- **ofertas_laborales**: Almacenamiento de ofertas extraídas
- **logs_extraccion**: Registro de actividades de extracción

### Índices y Optimizaciones

- Índices en campos de búsqueda frecuente
- Particionado por fecha de publicación
- Limpieza automática de datos antiguos

## 🚀 Despliegue en Producción

### Configuración de Producción

1. **Variables de Entorno**
   ```bash
   export SECRET_KEY="tu-clave-secreta-muy-segura"
   export FLASK_ENV="production"
   ```

2. **Servidor Web**
   - Usar Gunicorn o uWSGI
   - Configurar Nginx como proxy reverso
   - Habilitar HTTPS con certificado SSL

3. **Base de Datos**
   - Configurar respaldos automáticos
   - Monitorear rendimiento
   - Implementar replicación si es necesario

## 🧪 Pruebas

### Ejecutar Pruebas del Extractor
```bash
python test_extractor_simple.py
```

### Ejecutar Pruebas de la Aplicación
```bash
python test_app_completa.py
```

### Ejecutar Aplicación con Pruebas
```bash
python run_test.py
```

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Enviar Pull Request con descripción detallada

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.

## 🆘 Soporte

Para soporte técnico o reportar problemas:

- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar la documentación técnica

## 🔄 Actualizaciones Futuras

- [ ] Integración con más portales de empleo
- [ ] API REST para integración externa
- [ ] Notificaciones por email
- [ ] Aplicación móvil
- [ ] Sistema de alertas personalizadas
- [ ] Mejoras en los selectores de scraping

## ✨ Ventajas del Sistema Actual

- **Sin dependencia de IA**: No requiere APIs externas
- **Más rápido**: Extracción directa sin procesamiento de IA
- **Más confiable**: No depende de la disponibilidad de APIs externas
- **Enfoque en Tacna**: Específicamente diseñado para ofertas de Tacna
- **Fallback robusto**: Ofertas de ejemplo cuando los portales no están disponibles
- **Fácil mantenimiento**: Código más simple y directo

## 🎓 Aporte Técnico-Académico

### Contribución como Practicante Pre-Profesional

Este proyecto representa una contribución significativa en el marco de las prácticas pre-profesionales realizadas en la Oficina de Responsabilidad Social Universitaria (RSU) de la Universidad Privada de Tacna (UPT).

### Objetivos Académicos Cumplidos

1. **Aplicación de Conocimientos Técnicos**:
   - Desarrollo web con Flask y Python
   - Gestión de bases de datos SQL Server
   - Técnicas de web scraping con BeautifulSoup
   - Arquitectura de software y patrones de diseño

2. **Desarrollo de Competencias Profesionales**:
   - Análisis de requisitos y especificación de software
   - Diseño de sistemas y modelado de datos
   - Implementación de soluciones tecnológicas
   - Documentación técnica y de usuario

3. **Impacto Social y Universitario**:
   - Optimización de procesos administrativos
   - Mejora en la gestión de oportunidades laborales
   - Contribución al desarrollo regional de Tacna
   - Fortalecimiento de la vinculación universidad-sociedad

### Metodología de Desarrollo

**Fase 1: Análisis y Planificación**
- Levantamiento de requisitos con la Oficina de RSU
- Análisis del proceso actual de gestión de ofertas
- Definición de objetivos y alcance del proyecto
- Diseño de la arquitectura del sistema

**Fase 2: Diseño y Modelado**
- Especificación de requerimientos funcionales y no funcionales
- Diseño de la base de datos y modelo de datos
- Creación de diagramas UML (casos de uso, clases, secuencia)
- Definición de la interfaz de usuario

**Fase 3: Implementación**
- Desarrollo del extractor de ofertas laborales
- Implementación de la aplicación web Flask
- Integración con base de datos SQL Server
- Desarrollo de la interfaz de usuario

**Fase 4: Pruebas y Validación**
- Pruebas unitarias del extractor
- Pruebas de integración del sistema completo
- Validación con usuarios finales
- Corrección de errores y optimización

**Fase 5: Documentación y Entrega**
- Documentación técnica completa
- Manual de usuario
- Documentación de instalación y configuración
- Capacitación al personal de la Oficina de RSU

### Tecnologías y Herramientas Utilizadas

**Backend:**
- Python 3.8+
- Flask 2.3.3 (Framework web)
- BeautifulSoup4 4.12.2 (Web scraping)
- pyodbc 4.0.39 (Conexión a SQL Server)
- requests 2.31.0 (HTTP requests)

**Base de Datos:**
- Microsoft SQL Server
- Diseño relacional optimizado
- Índices para consultas eficientes

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap para diseño responsivo
- Chart.js para gráficos y estadísticas

**Herramientas de Desarrollo:**
- Git para control de versiones
- Visual Studio Code como IDE
- SQL Server Management Studio
- Navegadores web para pruebas

### Resultados y Logros

**Técnicos:**
- Sistema funcional y estable
- Extracción automática de 4 portales laborales
- Interfaz intuitiva y responsiva
- Base de datos optimizada y escalable
- Código limpio y documentado

**Académicos:**
- Aplicación práctica de conocimientos de ingeniería de sistemas
- Desarrollo de competencias en análisis y diseño de software
- Experiencia en gestión de proyectos de software
- Contribución a la investigación aplicada

**Sociales:**
- Mejora en la eficiencia de procesos administrativos
- Facilitación del acceso a oportunidades laborales
- Contribución al desarrollo regional de Tacna
- Fortalecimiento de la responsabilidad social universitaria

### Lecciones Aprendidas

1. **Gestión de Proyectos**: Importancia de la planificación y seguimiento
2. **Análisis de Requisitos**: Necesidad de comunicación efectiva con usuarios
3. **Desarrollo de Software**: Valor del código limpio y documentado
4. **Integración de Sistemas**: Desafíos de la interoperabilidad
5. **Responsabilidad Social**: Impacto de la tecnología en la sociedad

### Recomendaciones Futuras

1. **Expansión del Sistema**:
   - Integración con más portales laborales
   - Desarrollo de aplicación móvil
   - Sistema de notificaciones automáticas

2. **Mejoras Técnicas**:
   - Implementación de caché para mejor rendimiento
   - Sistema de respaldos automáticos
   - Monitoreo y logging avanzado

3. **Impacto Social**:
   - Capacitación a más usuarios
   - Integración con otras oficinas de la universidad
   - Colaboración con instituciones locales

### Conclusiones

Este proyecto de prácticas pre-profesionales ha permitido aplicar conocimientos teóricos en un contexto real, contribuyendo significativamente a la optimización de procesos en la Oficina de RSU de la UPT. La experiencia ha sido enriquecedora tanto desde el punto de vista técnico como académico, demostrando la importancia de la vinculación universidad-sociedad en el desarrollo de soluciones tecnológicas innovadoras.

El sistema desarrollado no solo cumple con los objetivos planteados, sino que establece las bases para futuras mejoras y expansiones, contribuyendo al desarrollo sostenible de la región de Tacna a través de la tecnología.

---

**Desarrollado para la ciudad de Tacna, Perú** 🇵🇪  
**Universidad Privada de Tacna (UPT)** 🎓  
**Oficina de Responsabilidad Social Universitaria (RSU)** 🤝