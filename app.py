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
        if usuarios_coll:
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
    ofertas_coll, _ = get_collections()
    
    if not ofertas_coll:
        return render_template('dashboard.html', 
                             ofertas=[], 
                             total_ofertas=0, 
                             fuentes={})
    
    # Obtener ofertas recientes
    ofertas = list(ofertas_coll.find().sort('created_at', DESCENDING).limit(10))
    
    # Convertir ObjectId a string y agregar campo id
    for oferta in ofertas:
        oferta['_id'] = str(oferta['_id'])
        if 'id' not in oferta:
            oferta['id'] = oferta.get('id', oferta['_id'])
    
    # Estadísticas simples
    total_ofertas = ofertas_coll.count_documents({})
    
    # Fuentes
    pipeline = [
        {'$group': {'_id': '$fuente', 'count': {'$sum': 1}}}
    ]
    fuentes_list = list(ofertas_coll.aggregate(pipeline))
    fuentes = {item['_id'] or 'Desconocido': item['count'] for item in fuentes_list}
    
    return render_template('dashboard.html', 
                         ofertas=ofertas, 
                         total_ofertas=total_ofertas, 
                         fuentes=fuentes)


@app.route('/ofertas')
@login_required
def listar_ofertas():
    """Lista de ofertas con filtros"""
    ofertas_coll, _ = get_collections()
    
    if not ofertas_coll:
        return render_template('ofertas.html', ofertas=[], filtros={}, page=1)
    
    # Filtros
    filtros = {}
    query = {}
    
    if request.args.get('busqueda'):
        busqueda = request.args.get('busqueda')
        filtros['busqueda'] = busqueda
        query['$or'] = [
            {'titulo_oferta': {'$regex': busqueda, '$options': 'i'}},
            {'empresa': {'$regex': busqueda, '$options': 'i'}},
            {'puesto': {'$regex': busqueda, '$options': 'i'}}
        ]
    
    if request.args.get('empresa'):
        empresa = request.args.get('empresa')
        filtros['empresa'] = empresa
        query['empresa'] = {'$regex': empresa, '$options': 'i'}
    
    if request.args.get('nivel_academico'):
        nivel = request.args.get('nivel_academico')
        filtros['nivel_academico'] = nivel
        query['nivel_academico'] = nivel
    
    if request.args.get('modalidad'):
        modalidad = request.args.get('modalidad')
        filtros['modalidad'] = modalidad
        query['modalidad'] = modalidad
    
    # Paginación
    page = int(request.args.get('page', 1))
    limit = 20
    skip = (page - 1) * limit
    
    # Obtener ofertas
    ofertas = list(ofertas_coll.find(query).sort('created_at', DESCENDING).skip(skip).limit(limit))
    
    # Convertir ObjectId y agregar campo id
    for oferta in ofertas:
        oferta['_id'] = str(oferta['_id'])
        if 'id' not in oferta:
            oferta['id'] = oferta.get('id', oferta['_id'])
    
    return render_template('ofertas.html', ofertas=ofertas, filtros=filtros, page=page)


@app.route('/ofertas/<oferta_id>')
@login_required
def ver_oferta(oferta_id):
    """Ver detalle de una oferta"""
    ofertas_coll, _ = get_collections()
    
    if not ofertas_coll:
        flash('Base de datos no disponible', 'error')
        return redirect(url_for('listar_ofertas'))
    
    oferta = ofertas_coll.find_one({'id': oferta_id})
    
    if not oferta:
        oferta = ofertas_coll.find_one({'_id': oferta_id})
    
    if not oferta:
        flash('Oferta no encontrada', 'error')
        return redirect(url_for('listar_ofertas'))
    
    oferta['_id'] = str(oferta['_id'])
    if 'id' not in oferta:
        oferta['id'] = oferta.get('id', oferta['_id'])
    
    return render_template('ver_oferta.html', oferta=oferta)


@app.route('/estadisticas')
@login_required
def estadisticas():
    """Página de estadísticas"""
    ofertas_coll, _ = get_collections()
    
    if not ofertas_coll:
        return render_template('estadisticas.html',
                             total_ofertas=0,
                             por_nivel={},
                             por_modalidad={},
                             por_fuente={},
                             top_empresas={})
    
    total_ofertas = ofertas_coll.count_documents({})
    
    # Agregaciones
    niveles = list(ofertas_coll.aggregate([
        {'$group': {'_id': '$nivel_academico', 'count': {'$sum': 1}}}
    ]))
    
    modalidades = list(ofertas_coll.aggregate([
        {'$group': {'_id': '$modalidad', 'count': {'$sum': 1}}}
    ]))
    
    fuentes = list(ofertas_coll.aggregate([
        {'$group': {'_id': '$fuente', 'count': {'$sum': 1}}}
    ]))
    
    empresas = list(ofertas_coll.aggregate([
        {'$group': {'_id': '$empresa', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]))
    
    return render_template('estadisticas.html',
                         total_ofertas=total_ofertas,
                         por_nivel={item['_id'] or 'N/A': item['count'] for item in niveles},
                         por_modalidad={item['_id'] or 'N/A': item['count'] for item in modalidades},
                         por_fuente={item['_id'] or 'N/A': item['count'] for item in fuentes},
                         top_empresas={item['_id'] or 'N/A': item['count'] for item in empresas})


@app.route('/extraer', methods=['POST'])
@login_required
def extraer_ofertas():
    """Extraer ofertas - versión simplificada y robusta"""
    if not mongo_connected:
        return jsonify({
            'success': False, 
            'error': 'MongoDB no está disponible. Por favor, inicia MongoDB primero.',
            'mensaje': 'Para extraer ofertas, MongoDB debe estar corriendo.'
        }), 500
    
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

