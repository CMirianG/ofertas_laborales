"""
Factory pattern para la aplicación Flask
"""
from flask import Flask, redirect, url_for
from werkzeug.security import generate_password_hash
import logging
from config.settings import Config
from app.services.database_service import MongoDBManager
from app.controllers.auth import auth_bp
from app.controllers.ofertas import ofertas_bp
from app.controllers.dashboard import dashboard_bp


def create_app(config_class=Config):
    """
    Factory function para crear la aplicación Flask
    Args:
        config_class: Clase de configuración a usar
    Returns:
        Instancia de la aplicación Flask
    """
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuración
    app.config.from_object(config_class)
    app.secret_key = config_class.SECRET_KEY
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, config_class.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(ofertas_bp)
    app.register_blueprint(dashboard_bp)
    
    # Ruta raíz
    @app.route('/')
    def index():
        """Página principal - redirige al login o dashboard"""
        from flask import session
        if 'user_id' in session:
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('auth.login'))
    
    # Inicializar base de datos
    with app.app_context():
        initialize_database(config_class, logger)
    
    return app


def initialize_database(config_class, logger):
    """
    Inicializa la base de datos MongoDB al arrancar la aplicación
    Args:
        config_class: Clase de configuración
        logger: Logger para mensajes
    """
    try:
        db_manager = MongoDBManager(config_class.MONGODB_URI)

        # Verificar conexión real antes de continuar
        if not getattr(db_manager, "_connected", True):
            logger.warning(
                "MongoDB no está disponible al iniciar la app. "
                "El sistema funcionará en modo limitado (sin persistencia)."
            )
            return

        logger.info("Conectado a MongoDB exitosamente")

        # Crear usuario admin por defecto si no existe
        admin_user = db_manager.get_user_by_username('admin')
        if not admin_user:
            password_hash = generate_password_hash('admin123')
            db_manager.create_user('admin', password_hash, 'admin@ofertas.com')
            logger.info("Usuario admin creado: admin/admin123")
        else:
            logger.info("Usuario admin ya existe")

    except Exception as e:
        logger.error(f"Error inicializando MongoDB: {e}")

