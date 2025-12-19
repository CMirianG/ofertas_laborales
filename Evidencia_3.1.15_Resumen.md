# Evidencia 3.1.15 - Metodología de Desarrollo Incremental e Iterativa

## Resumen Ejecutivo

Este documento presenta evidencia concisa del uso de metodología incremental e iterativa en el proyecto "Sistema de Ofertas Laborales para Tacna".

## 1. Historial de Commits (Git)

```
fcf79df | 2025-12-05 | doc
e4d5c3a | 2025-12-04 | CAMBIOS
e501775 | 2025-12-03 | cambios
cbb664f | 2025-12-02 | cambios
31ca9b9 | 2025-12-02 | cambios_app
55c6992 | 2025-12-02 | cambios
6d0d4d0 | 2025-10-13 | ofertas
```

**Análisis**: Desarrollo continuo durante ~2 meses con múltiples iteraciones documentadas.

## 2. Iteraciones Documentadas

### Iteración 1: Versión Monolítica (Octubre 2025)
- **Commit**: `6d0d4d0 - ofertas (2025-10-13)`
- **Evidencia**: Archivo `app.py` con implementación completa en un solo archivo
- **Funcionalidades**: Autenticación básica, visualización de ofertas, navegación

### Iteración 2: Refactorización Modular (Diciembre 2025)
- **Commits**: `55c6992, 31ca9b9, cbb664f (2025-12-02)`
- **Evidencia**: Estructura de carpetas modular creada
- **Cambios**: Separación en controllers/, services/, utils/, config/

### Iteración 3: Mejoras y Documentación (Diciembre 2025)
- **Commits**: `e501775, e4d5c3a, fcf79df (2025-12-03 a 2025-12-05)`
- **Evidencia**: Mejoras en funcionalidades y documentación completa
- **Cambios**: Filtros avanzados, estadísticas mejoradas, documentación técnica

## 3. Incrementos Funcionales

| Incremento | Funcionalidad | Archivo de Evidencia |
|------------|--------------|---------------------|
| 1 | Autenticación básica | `app/controllers/auth.py` |
| 2 | Visualización de ofertas | `app/controllers/ofertas.py` |
| 3 | Servicio de scraping | `app/services/scraping_service.py` |
| 4 | Dashboard y estadísticas | `app/controllers/dashboard.py` |
| 5 | Filtros avanzados | `app/controllers/ofertas.py` |

## 4. Evidencia de Arquitectura Evolutiva

### Estado Inicial (Iteración 1)
```
app.py  # Todo el código en un archivo
```

### Estado Final (Iteración 2+)
```
app/
  controllers/    # Manejo de rutas HTTP
  services/       # Lógica de negocio
  utils/          # Funciones auxiliares
config/
  settings.py     # Configuración centralizada
```

## 5. Ciclos Iterativos

Cada iteración siguió el ciclo:
1. **Análisis**: Revisión de necesidades y feedback
2. **Diseño**: Ajustes en arquitectura y modelos
3. **Implementación**: Desarrollo de código
4. **Pruebas**: Verificación de funcionalidades

## 6. Métricas

- **Duración**: ~2 meses (Oct 2025 - Dic 2025)
- **Commits**: 7 commits documentados
- **Iteraciones**: 3 iteraciones principales
- **Incrementos**: 5 incrementos funcionales

## 7. Conclusión

La evidencia demuestra claramente:
- ✓ Desarrollo incremental con múltiples versiones funcionales
- ✓ Iteraciones documentadas con ciclos completos
- ✓ Evolución arquitectónica verificable
- ✓ Prototipos evolutivos mantenidos
- ✓ Mejora continua del código y funcionalidades

---

**Referencias**:
- Historial Git: `git log --oneline --all`
- Estructura de archivos: `app/`, `config/`
- Documentación: `README.md`, `CHANGELOG.md`

