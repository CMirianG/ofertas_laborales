-- =====================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Ofertas Laborales - Tacna
-- =====================================================

-- Crear la base de datos si no existe

CREATE DATABASE OfertasLaborales;
    
-- Usar la base de datos
USE OfertasLaborales;
GO

-- =====================================================
-- CREACIÓN DE TABLAS
-- =====================================================

-- Tabla usuarios
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='usuarios' AND xtype='U')
BEGIN
    CREATE TABLE usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50) UNIQUE NOT NULL,
        password_hash NVARCHAR(255) NOT NULL,
        email NVARCHAR(100),
        created_at DATETIME2 DEFAULT GETDATE(),
        is_active BIT DEFAULT 1
    );
END
GO

-- Tabla ofertas_laborales
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ofertas_laborales' AND xtype='U')
BEGIN
    CREATE TABLE ofertas_laborales (
        id NVARCHAR(50) PRIMARY KEY,
        titulo_oferta NVARCHAR(80) NOT NULL,
        empresa NVARCHAR(100) NOT NULL,
        nivel_academico NVARCHAR(20) NOT NULL,
        puesto NVARCHAR(100) NOT NULL,
        experiencia_minima_anios INT DEFAULT 0,
        conocimientos_clave NVARCHAR(500),
        responsabilidades_breve NVARCHAR(200),
        modalidad NVARCHAR(20) NOT NULL,
        ubicacion NVARCHAR(100) NOT NULL,
        jornada NVARCHAR(30),
        salario NVARCHAR(50),
        fecha_publicacion DATE,
        fecha_cierre DATE,
        como_postular NVARCHAR(500),
        url_oferta NVARCHAR(500) NOT NULL,
        documentos_requeridos NVARCHAR(300),
        contacto NVARCHAR(100),
        etiquetas NVARCHAR(200),
        fuente NVARCHAR(50) NOT NULL,
        fecha_estimacion BIT DEFAULT 0,
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE()
    );
END
GO

-- Tabla logs_extraccion
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='logs_extraccion' AND xtype='U')
BEGIN
    CREATE TABLE logs_extraccion (
        id INT IDENTITY(1,1) PRIMARY KEY,
        fuente NVARCHAR(50) NOT NULL,
        ofertas_encontradas INT DEFAULT 0,
        ofertas_nuevas INT DEFAULT 0,
        ofertas_actualizadas INT DEFAULT 0,
        errores INT DEFAULT 0,
        fecha_ejecucion DATETIME2 DEFAULT GETDATE(),
        duracion_segundos INT,
        detalles NVARCHAR(MAX)
    );
END
GO

-- =====================================================
-- CREACIÓN DE ÍNDICES
-- =====================================================

-- Índice en empresa
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ofertas_empresa')
    CREATE INDEX IX_ofertas_empresa ON ofertas_laborales(empresa);
GO

-- Índice en nivel académico
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ofertas_nivel')
    CREATE INDEX IX_ofertas_nivel ON ofertas_laborales(nivel_academico);
GO

-- Índice en modalidad
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ofertas_modalidad')
    CREATE INDEX IX_ofertas_modalidad ON ofertas_laborales(modalidad);
GO

-- Índice en fuente
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ofertas_fuente')
    CREATE INDEX IX_ofertas_fuente ON ofertas_laborales(fuente);
GO

-- Índice en fecha de creación
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ofertas_created_at')
    CREATE INDEX IX_ofertas_created_at ON ofertas_laborales(created_at);
GO

-- Índice combinado de texto (no fulltext)
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ofertas_texto')
    CREATE INDEX IX_ofertas_texto ON ofertas_laborales(titulo_oferta, puesto, conocimientos_clave);
GO

PRINT 'Script de creación de base de datos y tablas completado exitosamente';

INSERT INTO usuarios (username, password_hash, email, is_active)
VALUES 
('admin', 'hash_prueba_123', 'admin@ofertas.com', 1);