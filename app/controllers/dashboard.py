"""
Controlador del dashboard y estadísticas
"""
from flask import Blueprint, render_template
from app.services.database_service import MongoDBManager
from app.controllers.auth import login_required
from config.settings import Config

dashboard_bp = Blueprint('dashboard', __name__)


def get_db_manager():
    """Obtiene la instancia del gestor de base de datos"""
    return MongoDBManager(Config.MONGODB_URI)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal con estadísticas"""
    db_manager = get_db_manager()
    
    # Obtener estadísticas usando agregaciones de MongoDB
    ofertas = db_manager.get_ofertas(limit=10)
    stats = db_manager.get_estadisticas()
    
    total_ofertas = stats.get('total_ofertas', 0)
    fuentes = stats.get('por_fuente', {})
    
    return render_template('dashboard.html', 
                         ofertas=ofertas, 
                         total_ofertas=total_ofertas,
                         fuentes=fuentes)


@dashboard_bp.route('/estadisticas')
@login_required
def estadisticas():
    """Página de estadísticas usando agregaciones de MongoDB"""
    db_manager = get_db_manager()
    
    # Obtener estadísticas usando agregaciones eficientes de MongoDB
    stats = db_manager.get_estadisticas()
    
    niveles = stats.get('por_nivel', {})
    modalidades = stats.get('por_modalidad', {})
    fuentes = stats.get('por_fuente', {})
    total_ofertas = stats.get('total_ofertas', 0)
    top_empresas = stats.get('top_empresas', {})
    
    return render_template('estadisticas.html', 
                         niveles=niveles,
                         modalidades=modalidades,
                         fuentes=fuentes,
                         total_ofertas=total_ofertas,
                         top_empresas=top_empresas)

