"""
Aplicación Flask simplificada para Sistema de Ofertas Laborales - Tacna
Versión simplificada y funcional
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os
import logging

# Configuración
app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = 'ofertas_laborales'

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conexión a MongoDB
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    ofertas_collection = db['ofertas']
    usuarios_collection = db['usuarios']
    logger.info("✓ Conexión a MongoDB exitosa")
    mongo_connected = True
except Exception as e:
    logger.error(f"✗ Error conectando a MongoDB: {e}")
    mongo_connected = False
    db = None
    ofertas_collection = None
    usuarios_collection = None

# Crear índices
if mongo_connected:
    try:
        ofertas_collection.create_index("id", unique=True)
        ofertas_collection.create_index([("created_at", DESCENDING)])
        usuarios_collection.create_index("username", unique=True)
    except:
        pass

# Inicializar usuario admin
if mongo_connected:
    try:
        if not usuarios_collection.find_one({'username': 'admin'}):
            usuarios_collection.insert_one({
                'username': 'admin',
                'password_hash': generate_password_hash('admin123'),
                'email': 'admin@ofertas.com',
                'created_at': datetime.now()
            })
            logger.info("✓ Usuario admin creado (admin/admin123)")
    except:
        pass


# Helper para verificar conexión
def get_collections():
    """Retorna las colecciones o None si no hay conexión"""
    if not mongo_connected:
        return None, None
    return ofertas_collection, usuarios_collection


# Decorador para requerir login
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ========== RUTAS ==========

@app.route('/')
def index():
    """Página principal"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Modo sin conexión
        if not mongo_connected:
            if username == 'admin' and password == 'admin123':
                session['user_id'] = 'offline-admin'
                session['username'] = 'admin'
                flash('Inicio de sesión en modo sin conexión', 'warning')
                return redirect(url_for('dashboard'))
            flash('MongoDB no disponible. Solo admin/admin123 funciona', 'error')
            return render_template('login.html')
        
        # Modo normal
        ofertas_coll, usuarios_coll = get_collections()
        if usuarios_coll is not None:
            user = usuarios_coll.find_one({'username': username})
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    # Usar MongoDBManager que incluye soporte para datos mock
    from app.services.database_service import MongoDBManager
    from config.settings import Config
    
    db_manager = MongoDBManager(Config.MONGODB_URI)
    
    # Obtener ofertas y estadísticas (usará datos mock si la BD está vacía)
    ofertas = db_manager.get_ofertas(limit=10)
    stats = db_manager.get_estadisticas()
    
    total_ofertas = stats.get('total_ofertas', 0)
    fuentes = stats.get('por_fuente', {})
    
    return render_template('dashboard.html', 
                         ofertas=ofertas, 
                         total_ofertas=total_ofertas, 
                         fuentes=fuentes)


@app.route('/ofertas')
@login_required
def listar_ofertas():
    """Lista de ofertas con filtros"""
    from app.services.database_service import MongoDBManager
    from config.settings import Config
    
    db_manager = MongoDBManager(Config.MONGODB_URI)
    
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
    limit = 20
    offset = (page - 1) * limit
    
    # Obtener ofertas usando MongoDBManager (incluye datos de simulación)
    ofertas = db_manager.get_ofertas(filtros=filtros, limit=limit, offset=offset)
    
    # Asegurar que todas las ofertas tengan un campo 'id'
    for oferta in ofertas:
        if 'id' not in oferta:
            oferta['id'] = oferta.get('_id', str(oferta.get('id', '')))
    
    return render_template('ofertas.html', ofertas=ofertas, filtros=filtros, page=page)


@app.route('/ofertas/<oferta_id>')
@login_required
def ver_oferta(oferta_id):
    """Ver detalle de una oferta"""
    from app.services.database_service import MongoDBManager
    from config.settings import Config
    
    db_manager = MongoDBManager(Config.MONGODB_URI)
    
    # Intentar obtener la oferta por ID
    oferta = db_manager.get_oferta_by_id(oferta_id)
    
    # Si no se encuentra, buscar en datos de simulación
    if not oferta:
        mock_ofertas = db_manager.get_ofertas(limit=1000, offset=0)
        for mock_oferta in mock_ofertas:
            if str(mock_oferta.get('id', '')) == str(oferta_id) or str(mock_oferta.get('_id', '')) == str(oferta_id):
                oferta = mock_oferta
                break
    
    if not oferta:
        flash('Oferta no encontrada', 'error')
        return redirect(url_for('listar_ofertas'))
    
    # Asegurar que tenga _id como string
    if '_id' in oferta:
        oferta['_id'] = str(oferta['_id'])
    if 'id' not in oferta:
        oferta['id'] = oferta.get('_id', oferta_id)
    if 'id' not in oferta:
        oferta['id'] = oferta.get('id', oferta['_id'])
    
    return render_template('ver_oferta.html', oferta=oferta)


@app.route('/estadisticas')
@login_required
def estadisticas():
    """Página de estadísticas"""
    # Usar MongoDBManager que incluye soporte para datos mock
    from app.services.database_service import MongoDBManager
    from config.settings import Config
    
    db_manager = MongoDBManager(Config.MONGODB_URI)
    
    # Obtener estadísticas (usará datos mock si la BD está vacía)
    stats = db_manager.get_estadisticas()
    
    # Extraer las estadísticas con los nombres que el template espera
    total_ofertas = stats.get('total_ofertas', 0)
    niveles = stats.get('por_nivel', {})
    modalidades = stats.get('por_modalidad', {})
    fuentes = stats.get('por_fuente', {})
    top_empresas = stats.get('top_empresas', {})
    
    return render_template('estadisticas.html',
                         total_ofertas=total_ofertas,
                         niveles=niveles,
                         modalidades=modalidades,
                         fuentes=fuentes,
                         top_empresas=top_empresas)


@app.route('/extraer', methods=['POST'])
@login_required
def extraer_ofertas():
    """Extraer ofertas - versión simplificada y robusta"""
    if not mongo_connected:
        return jsonify({
            'success': False, 
            'error': 'MongoDB no está disponible',
            'mensaje': 'MongoDB no está instalado o no está corriendo.\n\n' +
                      'Para extraer ofertas necesitas instalar MongoDB.\n\n' +
                      'Opciones:\n' +
                      '1. Instalar MongoDB localmente (ver INSTALAR_MONGODB.md)\n' +
                      '2. Usar MongoDB Atlas (gratis en la nube)\n\n' +
                      'Sin MongoDB puedes usar la aplicación en modo lectura.'
        }), 400
    
    try:
        import traceback
        from app.services.scraping_service import ScrapingService
        from app.services.database_service import MongoDBManager
        
        logger.info("Iniciando extracción de ofertas...")
        
        # Crear instancia de MongoDBManager
        try:
            db_manager = MongoDBManager(MONGODB_URI)
            if not db_manager._connected:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo conectar a MongoDB',
                    'mensaje': 'Verifica que MongoDB esté corriendo en localhost:27017'
                }), 500
        except Exception as db_error:
            logger.error(f"Error creando MongoDBManager: {db_error}")
            return jsonify({
                'success': False,
                'error': f'Error de conexión a MongoDB: {str(db_error)}',
                'mensaje': 'Verifica tu configuración de MongoDB'
            }), 500
        
        # Crear servicio de scraping
        try:
            scraping_service = ScrapingService(db_manager)
        except Exception as scraping_init_error:
            logger.error(f"Error inicializando ScrapingService: {scraping_init_error}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': f'Error inicializando servicio de scraping: {str(scraping_init_error)}'
            }), 500
        
        # Ejecutar scraping
        try:
            logger.info("Ejecutando scraping...")
            stats = scraping_service.run_scraping()
            logger.info(f"Scraping completado. Stats: {stats}")
        except Exception as scraping_error:
            logger.error(f"Error durante el scraping: {scraping_error}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': f'Error durante la extracción: {str(scraping_error)}',
                'traceback': traceback.format_exc() if app.config['DEBUG'] else None
            }), 500
        
        # Retornar resultados
        return jsonify({
            'success': True,
            'nuevas_ofertas': stats.get('nuevas', 0),
            'actualizadas': stats.get('actualizadas', 0),
            'errores': stats.get('errores', 0),
            'total_procesadas': stats.get('total_encontradas', 0),
            'por_fuente': stats.get('por_fuente', {}),
            'mensaje': f'Extracción completada: {stats.get("nuevas", 0)} nuevas ofertas'
        })
        
    except ImportError as import_error:
        logger.error(f"Error de importación: {import_error}")
        return jsonify({
            'success': False,
            'error': f'Módulo no encontrado: {str(import_error)}',
            'mensaje': 'Verifica que todos los archivos del servicio estén presentes'
        }), 500
    except Exception as e:
        logger.error(f"Error inesperado en extracción: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error inesperado: {str(e)}',
            'traceback': traceback.format_exc() if app.config['DEBUG'] else None
        }), 500


# Manejador de errores global para asegurar respuestas JSON
@app.errorhandler(500)
def handle_500_error(e):
    """Maneja errores 500 y retorna JSON"""
    logger.error(f"Error 500: {e}")
    import traceback
    logger.error(traceback.format_exc())
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor',
        'mensaje': 'Ha ocurrido un error inesperado. Por favor, revisa los logs del servidor.',
        'detalles': str(e) if app.config['DEBUG'] else None
    }), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Maneja excepciones no capturadas"""
    logger.error(f"Excepción no capturada: {e}")
    import traceback
    logger.error(traceback.format_exc())
    return jsonify({
        'success': False,
        'error': 'Error inesperado',
        'mensaje': f'Ocurrió un error: {str(e)}',
        'detalles': traceback.format_exc() if app.config['DEBUG'] else None
    }), 500


@app.route('/favicon.ico')
def favicon():
    """Maneja la solicitud de favicon para evitar errores 404"""
    from flask import abort
    import os
    favicon_path = os.path.join(app.root_path, 'app', 'static', 'favicon.ico')
    if os.path.exists(favicon_path):
        from flask import send_from_directory
        return send_from_directory(os.path.join(app.root_path, 'app', 'static'),
                                  'favicon.ico', mimetype='image/vnd.microsoft.icon')
    else:
        # Retornar 204 No Content si no existe el favicon
        return '', 204


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

