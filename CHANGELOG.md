# Changelog - Sistema de Ofertas Laborales para Tacna

Este documento registra los cambios significativos del proyecto, evidenciando el desarrollo incremental e iterativo.

## [Iteración 3] - 2025-12-05

### Agregado
- Documentación completa del sistema
- Evidencia de metodología de desarrollo

### Cambios
- Mejoras en documentación técnica
- Refinamiento de funcionalidades existentes

## [Iteración 3] - 2025-12-04

### Cambios
- Mejoras en la interfaz de usuario
- Optimizaciones en el rendimiento del sistema

## [Iteración 3] - 2025-12-03

### Cambios
- Refinamiento de filtros de búsqueda
- Mejoras en la visualización de estadísticas

## [Iteración 2] - 2025-12-02

### Refactorizado
- **Cambio arquitectónico mayor**: Migración de código monolítico a arquitectura modular
- Separación de responsabilidades en capas:
  - Controladores (`app/controllers/`)
  - Servicios (`app/services/`)
  - Utilidades (`app/utils/`)
  - Configuración (`config/`)

### Agregado
- Estructura de carpetas modular
- Servicios de base de datos (`database_service.py`)
- Servicios de scraping (`scraping_service.py`)
- Controladores especializados (auth, dashboard, ofertas)
- Sistema de configuración centralizado

### Mejorado
- Mantenibilidad del código
- Escalabilidad del sistema
- Separación de concerns

## [Iteración 1] - 2025-10-13

### Agregado
- **Versión inicial funcional** del sistema
- Implementación monolítica en `app.py`
- Funcionalidades básicas:
  - Sistema de autenticación
  - Visualización de ofertas laborales
  - Navegación entre vistas
  - Integración básica con MongoDB

### Notas
- Esta versión permitió validar rápidamente los requisitos fundamentales del sistema
- Sirvió como prototipo evolutivo para las iteraciones posteriores

---

## Metodología de Desarrollo

Este proyecto sigue una **metodología incremental e iterativa** con las siguientes características:

- **Incremental**: Cada versión agrega nuevas funcionalidades sobre la base de la anterior
- **Iterativo**: Cada ciclo incluye análisis, diseño, implementación y pruebas
- **Evolutivo**: Los prototipos se refinan y mejoran en cada iteración

### Principios Aplicados

1. **Entrega temprana de valor**: Versión funcional desde la primera iteración
2. **Mejora continua**: Refactorización y optimización en cada ciclo
3. **Adaptabilidad**: Capacidad de ajustar el alcance según feedback
4. **Calidad progresiva**: Mejora de arquitectura y código en cada iteración

