from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from datetime import datetime
import os
from mongodb_database import MongoDBManager  # Cambio a MongoDB
from scraping_service import ScrapingService  # Servicio de scraping separado
from config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Inicializar componentes con MongoDB
db_manager = MongoDBManager(Config.MONGODB_URI)
scraping_service = ScrapingService(db_manager)

def initialize_database():
    """Inicializa la base de datos MongoDB al arrancar la aplicación"""
    try:
        # MongoDB no requiere creación explícita de base de datos
        # Se crea automáticamente al insertar el primer documento
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

# Inicializar base de datos al importar
initialize_database()

@app.route('/')
def index():
    """Página principal - redirige al login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db_manager.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Dashboard principal con estadísticas de MongoDB"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Obtener estadísticas usando agregaciones de MongoDB
    ofertas = db_manager.get_ofertas(limit=10)
    stats = db_manager.get_estadisticas()
    
    total_ofertas = stats.get('total_ofertas', 0)
    fuentes = stats.get('por_fuente', {})
    
    return render_template('dashboard.html', 
                         ofertas=ofertas, 
                         total_ofertas=total_ofertas,
                         fuentes=fuentes)

@app.route('/ofertas')
def ofertas():
    """Lista de ofertas laborales"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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
    
    ofertas = db_manager.get_ofertas(filtros, limit, offset)
    
    return render_template('ofertas.html', ofertas=ofertas, filtros=filtros, page=page)

@app.route('/ofertas/<oferta_id>')
def ver_oferta(oferta_id):
    """Ver detalles de una oferta específica"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    oferta = db_manager.get_oferta_by_id(oferta_id)
    if not oferta:
        flash('Oferta no encontrada', 'error')
        return redirect(url_for('ofertas'))
    
    return render_template('ver_oferta.html', oferta=oferta)

@app.route('/extraer', methods=['POST'])
def extraer_ofertas():
    """Extraer nuevas ofertas laborales usando el servicio de scraping separado"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        logger.info("Iniciando extracción de ofertas para Tacna con servicio de scraping...")
        
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

@app.route('/api/ofertas')
def api_ofertas():
    """API para obtener ofertas (para AJAX)"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
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
    limit = int(request.args.get('limit', 20))
    offset = (page - 1) * limit
    
    ofertas = db_manager.get_ofertas(filtros, limit, offset)
    
    return jsonify({
        'ofertas': ofertas,
        'page': page,
        'limit': limit
    })

@app.route('/estadisticas')
def estadisticas():
    """Página de estadísticas usando agregaciones de MongoDB"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
