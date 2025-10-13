import os
from dotenv import load_dotenv  

load_dotenv()

class Config:
    # ========================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ========================================
    
    # MongoDB Configuration (Base de datos NO RELACIONAL - NUEVA)
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    MONGODB_DATABASE = 'ofertas_laborales'
    
    # SQL Server Configuration (DEPRECADO - mantener para migración)
    SQL_SERVER_HOST = "161.132.50.113"
    SQL_SERVER_USER = "sa"
    SQL_SERVER_PASSWORD = "Upt2025ii"
    SQL_SERVER_DATABASE = "OfertasLaborales"
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Web Scraping Configuration
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    # Search Configuration
    TACNA_KEYWORDS = ['tacna', 'tacneño', 'tacneña']
    JOB_LEVELS = ['practicante', 'bachiller', 'profesional', 'egresado', 'universitario', 'estudiante']
    VALID_ACADEMIC_LEVELS = ['Practicante', 'Bachiller', 'Profesional']
    
    # Portal URLs
    PORTALS = {
        'computrabajo': 'https://pe.computrabajo.com/empleos-en-tacna',
        'bumeran': 'https://www.bumeran.com.pe/en-tacna/empleos.html',
        'indeed': 'https://pe.indeed.com/jobs?q=&l=Tacna%2C+Tacna',
        'trabajos_pe': 'https://www.trabajos.pe/trabajo-tacna'
    }
