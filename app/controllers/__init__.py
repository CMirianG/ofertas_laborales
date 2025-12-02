"""
Módulo de controladores - Blueprints de Flask
"""
from .auth import auth_bp
from .ofertas import ofertas_bp
from .dashboard import dashboard_bp

__all__ = ['auth_bp', 'ofertas_bp', 'dashboard_bp']

