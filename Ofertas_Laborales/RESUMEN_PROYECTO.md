# 📋 Resumen del Proyecto - Sistema de Ofertas Laborales para Tacna

## 🎯 Información General

**Institución:** Universidad Privada de Tacna (UPT)  
**Oficina:** Responsabilidad Social Universitaria (RSU)  
**Tipo:** Prácticas Pre-Profesionales  
**Área:** Ingeniería de Sistemas  
**Objetivo:** Optimización de procesos mediante soluciones tecnológicas innovadoras

---

## 📁 Estructura de Archivos del Proyecto

```
Ofertas_Laborales/
├── 📁 Archivos Principales
│   ├── app.py (8,547 bytes) - Aplicación Flask principal
│   ├── config.py (1,156 bytes) - Configuración del sistema
│   ├── database.py (12,873 bytes) - Gestión de base de datos SQL Server
│   └── extractor_simple.py (46,653 bytes) - Extractor de ofertas laborales
│
├── 📁 Base de Datos
│   └── 01_create_database.sql (4,016 bytes) - Script de creación de BD
│
├── 📁 Documentación
│   ├── README.md (33,486 bytes) - Documentación completa del proyecto
│   └── DOCUMENTO_ARQUITECTURA_SOLUCION.md (30,034 bytes) - Arquitectura técnica
│
├── 📁 Configuración
│   └── requirements.txt (124 bytes) - Dependencias Python
│
├── 📁 Frontend - Templates HTML
│   ├── base.html (4,060 bytes) - Plantilla base con navbar y footer
│   ├── login.html (4,792 bytes) - Formulario de autenticación
│   ├── dashboard.html (11,055 bytes) - Panel principal con estadísticas
│   ├── ofertas.html (14,775 bytes) - Lista de ofertas con filtros
│   ├── ver_oferta.html (9,424 bytes) - Vista detallada de oferta
│   └── estadisticas.html (11,595 bytes) - Página de estadísticas y gráficos
│
├── 📁 Frontend - Archivos Estáticos
│   ├── css/style.css (6,150 bytes) - Estilos personalizados
│   └── js/main.js (10,915 bytes) - JavaScript con funciones utilitarias
│
└── 📁 Cache Python
    └── __pycache__/ - Archivos compilados de Python (6 archivos)
```

---

## 📊 Estadísticas del Proyecto

| **Categoría** | **Archivos** | **Tamaño Total** | **Descripción** |
|---------------|--------------|------------------|-----------------|
| **Backend Python** | 4 archivos | 68,229 bytes | Lógica de negocio y extracción |
| **Frontend HTML** | 6 archivos | 55,701 bytes | Interfaz de usuario |
| **Frontend CSS/JS** | 2 archivos | 17,065 bytes | Estilos y funcionalidad |
| **Base de Datos** | 1 archivo | 4,016 bytes | Scripts SQL |
| **Documentación** | 2 archivos | 63,520 bytes | Documentación técnica |
| **Configuración** | 1 archivo | 124 bytes | Dependencias |
| **Cache Python** | 6 archivos | 127,794 bytes | Archivos compilados |

**📈 Total del Proyecto: 336,449 bytes (328 KB)**

---

## 🎯 Descripción Detallada de Archivos

### 🔧 Backend (Python)

#### **`app.py` (8,547 bytes)**
- **Aplicación Flask principal**
- Rutas: login, dashboard, ofertas, extracción, API
- Manejo de sesiones y autenticación
- Lógica de negocio del sistema

#### **`extractor_simple.py` (46,653 bytes)**
- **Extractor de ofertas laborales**
- Extrae de 4 portales: Computrabajo, Indeed, Bumeran, Trabajos.pe
- Filtros: solo Tacna, niveles válidos (Practicante, Bachiller, Profesional)
- Sistema de fallback con ofertas de ejemplo
- Validación robusta de datos

#### **`database.py` (12,873 bytes)**
- **Gestión de base de datos SQL Server**
- Conexión y operaciones CRUD
- Creación automática de tablas
- Consultas con filtros y paginación

#### **`config.py` (1,156 bytes)**
- **Configuración del sistema**
- URLs de portales laborales
- Credenciales de base de datos
- Parámetros de scraping

### 🎨 Frontend (HTML/CSS/JS)

#### **Templates HTML:**
- **`base.html`** - Estructura común con navbar, footer
- **`login.html`** - Formulario de autenticación
- **`dashboard.html`** - Panel principal con gráficos y estadísticas
- **`ofertas.html`** - Lista de ofertas con filtros avanzados
- **`ver_oferta.html`** - Vista detallada de cada oferta
- **`estadisticas.html`** - Gráficos y análisis estadístico

#### **Archivos Estáticos:**
- **`style.css`** - Estilos modernos con gradientes y animaciones
- **`main.js`** - Funciones JavaScript para UX mejorada

### 📚 Documentación

#### **`README.md` (33,486 bytes)**
- Documentación completa del proyecto
- Instrucciones de instalación y uso
- Especificación de requerimientos
- Guía de usuario

#### **`DOCUMENTO_ARQUITECTURA_SOLUCION.md` (30,034 bytes)**
- Documento técnico de arquitectura
- Diagramas UML y casos de uso
- Metodología de desarrollo
- Especificaciones técnicas

### 🗄️ Base de Datos

#### **`01_create_database.sql` (4,016 bytes)**
- Script de creación de base de datos
- Tablas: usuarios, ofertas_laborales, logs_extraccion
- Índices optimizados para consultas
- Usuario admin por defecto

### ⚙️ Configuración

#### **`requirements.txt` (124 bytes)**
- Dependencias Python necesarias
- Flask, requests, BeautifulSoup, pyodbc, etc.

---

## 🚀 Características Principales del Sistema

### ✅ Funcionalidades Implementadas:
1. **Extracción Automática** - 4 portales laborales
2. **Filtros Específicos** - Solo Tacna, 3 niveles académicos
3. **Validación Robusta** - Datos completos y válidos
4. **Interfaz Moderna** - Bootstrap 5, responsive design
5. **Autenticación Segura** - Login con hash de contraseñas
6. **Estadísticas** - Gráficos interactivos con Chart.js
7. **Base de Datos** - SQL Server con estructura optimizada

### 🎯 Niveles Académicos Soportados:
- **🔵 Practicante** - Estudiantes, pasantes, pre-profesionales
- **🟡 Bachiller** - Egresados de secundaria
- **🟢 Profesional** - Universitarios, técnicos superiores

### 📍 Ubicación Específica:
- **Solo Tacna, Perú** - Filtrado geográfico estricto
- Detección de variaciones: "Tacna, Tacna", "Tacneño", etc.

---

## 🛠️ Tecnologías Utilizadas

### Backend:
- **Python 3.13** - Lenguaje principal
- **Flask 2.3.3** - Framework web
- **BeautifulSoup 4.12.2** - Web scraping
- **pyodbc 5.2.0** - Conexión SQL Server
- **requests 2.31.0** - HTTP requests

### Frontend:
- **HTML5** - Estructura
- **CSS3** - Estilos personalizados
- **JavaScript** - Funcionalidad
- **Bootstrap 5** - Framework CSS
- **Chart.js** - Gráficos interactivos

### Base de Datos:
- **Microsoft SQL Server** - Base de datos principal
- **Índices optimizados** - Consultas eficientes

---

## 📈 Estado del Proyecto

**✅ COMPLETADO Y FUNCIONANDO:**
- ✅ Servidor ejecutándose en http://127.0.0.1:5000
- ✅ Base de datos creada y conectada
- ✅ Filtros implementados y probados
- ✅ Interfaz web funcional
- ✅ Extracción automática operativa
- ✅ Documentación completa

---

## 🎓 Contexto Académico

**Proyecto de Prácticas Pre-Profesionales:**
- **Institución:** Universidad Privada de Tacna (UPT)
- **Oficina:** Responsabilidad Social Universitaria (RSU)
- **Área:** Ingeniería de Sistemas
- **Objetivo:** Optimización de procesos mediante tecnología
- **Impacto:** Mejora en la gestión de oportunidades laborales para Tacna

---

## 🔧 Instalación y Uso

### Requisitos:
- Python 3.8 o superior
- SQL Server
- Navegador web moderno

### Instalación:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

### Acceso:
- **URL:** http://127.0.0.1:5000
- **Usuario:** admin
- **Contraseña:** admin123

---

## 📋 Campos de Ofertas Extraídas

Cada oferta incluye los siguientes campos normalizados:

- **ID** - Identificador único generado por el sistema
- **Título de Oferta** - Título de la oferta (máx. 80 caracteres)
- **Empresa** - Nombre de la empresa/organización
- **Nivel Académico** - Practicante, Bachiller o Profesional
- **Puesto** - Cargo o posición
- **Experiencia Mínima** - Años de experiencia requeridos
- **Conocimientos Clave** - 3-5 keywords relevantes
- **Responsabilidades** - Descripción breve (máx. 200 caracteres)
- **Modalidad** - Presencial, Remoto o Híbrido
- **Ubicación** - Tacna con distrito/localidad si está disponible
- **Jornada** - Tiempo completo, Medio tiempo, Por horas
- **Salario** - Monto en PEN o "No especificado"
- **Fechas** - Publicación y cierre (formato YYYY-MM-DD)
- **Cómo Postular** - Instrucciones para aplicar
- **URL Original** - Enlace a la oferta original
- **Documentos Requeridos** - Lista de documentos necesarios
- **Contacto** - Email o teléfono si está disponible
- **Etiquetas** - Tags adicionales (urgente, pasantía, etc.)
- **Fuente** - Portal donde se encontró la oferta

---

## 🌐 Fuentes de Datos

El sistema extrae ofertas laborales de los siguientes portales especializados:

### Portales Principales:
- **Computrabajo Perú** - Portal líder en empleos en Perú
- **Bumeran Perú** - Portal especializado en empleos profesionales
- **Indeed Perú** - Portal internacional con ofertas locales
- **Trabajos.pe** - Portal de empleos peruanos

### Características de Extracción:
- **Filtrado Geográfico** - Solo ofertas ubicadas en Tacna, Perú
- **Múltiples Estrategias** - Diferentes selectores CSS para mayor robustez
- **Deduplicación** - Elimina ofertas duplicadas entre portales
- **Validación de Datos** - Verifica la calidad y completitud de la información
- **Ofertas de Ejemplo** - Sistema de fallback con ofertas realistas para Tacna

---

## 🎯 Logros del Proyecto

### Técnicos:
- ✅ Sistema funcional y estable
- ✅ Extracción automática de 4 portales laborales
- ✅ Interfaz intuitiva y responsiva
- ✅ Base de datos optimizada y escalable
- ✅ Código limpio y documentado

### Académicos:
- ✅ Aplicación práctica de conocimientos de ingeniería de sistemas
- ✅ Desarrollo de competencias en análisis y diseño de software
- ✅ Experiencia en gestión de proyectos de software
- ✅ Contribución a la investigación aplicada

### Sociales:
- ✅ Mejora en la eficiencia de procesos administrativos
- ✅ Facilitación del acceso a oportunidades laborales
- ✅ Contribución al desarrollo regional de Tacna
- ✅ Fortalecimiento de la responsabilidad social universitaria

---

## 📝 Conclusión

Este proyecto de prácticas pre-profesionales ha permitido aplicar conocimientos teóricos en un contexto real, contribuyendo significativamente a la optimización de procesos en la Oficina de RSU de la UPT. La experiencia ha sido enriquecedora tanto desde el punto de vista técnico como académico, demostrando la importancia de la vinculación universidad-sociedad en el desarrollo de soluciones tecnológicas innovadoras.

El sistema desarrollado no solo cumple con los objetivos planteados, sino que establece las bases para futuras mejoras y expansiones, contribuyendo al desarrollo sostenible de la región de Tacna a través de la tecnología.

---

**Desarrollado para la ciudad de Tacna, Perú** 🇵🇪  
**Universidad Privada de Tacna (UPT)** 🎓  
**Oficina de Responsabilidad Social Universitaria (RSU)** 🤝

---

*Documento generado automáticamente - Diciembre 2024*
