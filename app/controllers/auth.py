"""
Controlador de autenticación
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.services.database_service import MongoDBManager
from config.settings import Config

auth_bp = Blueprint('auth', __name__)


def get_db_manager():
    """Obtiene la instancia del gestor de base de datos"""
    return MongoDBManager(Config.MONGODB_URI)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db_manager = get_db_manager()
        # Modo sin conexión: si no hay conexión a MongoDB, permitir login de emergencia
        if not getattr(db_manager, "_connected", True):
            if username == 'admin' and password == 'admin123':
                # Usuario de sesión en modo offline
                session['user_id'] = 'offline-admin'
                session['username'] = 'admin'
                flash('Inicio de sesión en modo sin conexión (MongoDB no disponible).', 'warning')
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('MongoDB no está disponible. Solo se permite admin/admin123 en modo sin conexión.', 'error')
                return render_template('login.html')

        # Modo normal (con MongoDB)
        user = db_manager.get_user_by_username(username)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))


def login_required(f):
    """Decorador para requerir autenticación"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

