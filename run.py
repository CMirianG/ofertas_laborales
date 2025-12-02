#!/usr/bin/env python3
"""
Punto de entrada principal de la aplicación
"""
import os
from app import create_app
from config.settings import Config

# Crear la aplicación usando el factory pattern
app = create_app(Config)

if __name__ == '__main__':
    # Crear directorios necesarios si no existen
    os.makedirs('app/templates', exist_ok=True)
    os.makedirs('app/static/css', exist_ok=True)
    os.makedirs('app/static/js', exist_ok=True)
    
    # Ejecutar la aplicación
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )

