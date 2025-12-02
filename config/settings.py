"""
Configuración del sistema de ofertas laborales
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración principal de la aplicación"""
    
    # ========================================
    # CONFIGURACIÓN DE FLASK
    # ========================================
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # ========================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ========================================
    
    # MongoDB Configuration (Base de datos principal)
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    MONGODB_DATABASE = 'ofertas_laborales'
    
    # ========================================
    # CONFIGURACIÓN DE WEB SCRAPING
    # ========================================
    USER_AGENT = os.environ.get('USER_AGENT') or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))
    MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
    
    # ========================================
    # CONFIGURACIÓN DE BÚSQUEDA
    # ========================================
    TACNA_KEYWORDS = ['tacna', 'tacneño', 'tacneña']
    JOB_LEVELS = ['practicante', 'bachiller', 'profesional', 'egresado', 'universitario', 'estudiante']
    VALID_ACADEMIC_LEVELS = ['Practicante', 'Bachiller', 'Profesional']
    
    # ========================================
    # CONFIGURACIÓN DE PORTALES
    # ========================================
    PORTALS = {
        'computrabajo': 'https://pe.computrabajo.com/empleos-en-tacna',
        'bumeran': 'https://www.bumeran.com.pe/en-tacna/empleos.html',
        'indeed': 'https://pe.indeed.com/jobs?q=&l=Tacna%2C+Tacna',
        'trabajos_pe': 'https://www.trabajos.pe/trabajo-tacna'
    }
    
    # ========================================
    # CONFIGURACIÓN DE PAGINACIÓN
    # ========================================
    OFERTAS_PER_PAGE = int(os.environ.get('OFERTAS_PER_PAGE', 20))
    MAX_RESULTS = int(os.environ.get('MAX_RESULTS', 1000))
    
    # ========================================
    # CONFIGURACIÓN DE LOGGING
    # ========================================
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')

