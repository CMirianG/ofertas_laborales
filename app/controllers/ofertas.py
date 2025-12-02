"""
Controlador de ofertas laborales
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services.database_service import MongoDBManager
from app.controllers.auth import login_required
from config.settings import Config

ofertas_bp = Blueprint('ofertas', __name__)


def get_db_manager():
    """Obtiene la instancia del gestor de base de datos"""
    return MongoDBManager(Config.MONGODB_URI)


@ofertas_bp.route('/ofertas')
@login_required
def listar_ofertas():
    """Lista de ofertas laborales"""
    db_manager = get_db_manager()
    
    # Filtros
    filtros = {}
    if request.args.get('busqueda'):
        filtros['busqueda'] = request.args.get('busqueda')
    if request.args.get('empresa'):
        filtros['empresa'] = request.args.get('empresa')
    if request.args.get('nivel_academico'):
        filtros['nivel_academico'] = request.args.get('nivel_academico')
    if request.args.get('modalidad'):
        filtros['modalidad'] = request.args.get('modalidad')
    
    # Paginación
    page = int(request.args.get('page', 1))
    limit = Config.OFERTAS_PER_PAGE
    offset = (page - 1) * limit
    
    ofertas = db_manager.get_ofertas(filtros, limit, offset)
    
    return render_template('ofertas.html', ofertas=ofertas, filtros=filtros, page=page)


@ofertas_bp.route('/ofertas/<oferta_id>')
@login_required
def ver_oferta(oferta_id):
    """Ver detalles de una oferta específica"""
    db_manager = get_db_manager()
    oferta = db_manager.get_oferta_by_id(oferta_id)
    
    if not oferta:
        flash('Oferta no encontrada', 'error')
        return redirect(url_for('ofertas.listar_ofertas'))
    
    return render_template('ver_oferta.html', oferta=oferta)


@ofertas_bp.route('/api/ofertas')
@login_required
def api_ofertas():
    """API para obtener ofertas (para AJAX)"""
    db_manager = get_db_manager()
    
    filtros = {}
    if request.args.get('busqueda'):
        filtros['busqueda'] = request.args.get('busqueda')
    if request.args.get('empresa'):
        filtros['empresa'] = request.args.get('empresa')
    if request.args.get('nivel_academico'):
        filtros['nivel_academico'] = request.args.get('nivel_academico')
    if request.args.get('modalidad'):
        filtros['modalidad'] = request.args.get('modalidad')
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', Config.OFERTAS_PER_PAGE))
    offset = (page - 1) * limit
    
    ofertas = db_manager.get_ofertas(filtros, limit, offset)
    
    return jsonify({
        'ofertas': ofertas,
        'page': page,
        'limit': limit
    })


@ofertas_bp.route('/extraer', methods=['POST'])
@login_required
def extraer_ofertas():
    """Extraer nuevas ofertas laborales usando el servicio de scraping"""
    from app.services.scraping_service import ScrapingService
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Iniciando extracción de ofertas para Tacna con servicio de scraping...")
        
        db_manager = get_db_manager()
        scraping_service = ScrapingService(db_manager)
        
        # Obtener portales a extraer (opcional)
        portals = request.json.get('portals', None) if request.is_json else None
        
        # Ejecutar servicio de scraping
        stats = scraping_service.run_scraping(portals)
        
        logger.info(f"Extracción completada: {stats}")
        
        return jsonify({
            'success': True,
            'nuevas_ofertas': stats.get('nuevas', 0),
            'actualizadas': stats.get('actualizadas', 0),
            'errores': stats.get('errores', 0),
            'total_procesadas': stats.get('total_encontradas', 0),
            'por_fuente': stats.get('por_fuente', {}),
            'servicio_separado': True
        })
        
    except Exception as e:
        logger.error(f"Error en extracción: {e}")
        import traceback
        logger.error(f"Traceback completo: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

