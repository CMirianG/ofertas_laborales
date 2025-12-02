"""
Validadores para datos del sistema
"""
from typing import Dict, Optional
import re


def validate_oferta_data(data: Dict) -> tuple[bool, Optional[str]]:
    """
    Valida los datos de una oferta laboral
    Args:
        data: Diccionario con los datos de la oferta
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    required_fields = ['titulo_oferta', 'empresa', 'nivel_academico', 'ubicacion']
    
    for field in required_fields:
        if not data.get(field):
            return False, f"Campo requerido faltante: {field}"
    
    # Validar nivel académico
    valid_levels = ['Practicante', 'Bachiller', 'Profesional']
    if data.get('nivel_academico') not in valid_levels:
        return False, f"Nivel académico inválido. Debe ser uno de: {', '.join(valid_levels)}"
    
    # Validar que la ubicación contenga "Tacna"
    ubicacion = data.get('ubicacion', '').lower()
    if 'tacna' not in ubicacion:
        return False, "La oferta debe ser para Tacna"
    
    # Validar URL si existe
    url = data.get('url_oferta', '')
    if url and not re.match(r'^https?://', url):
        return False, "URL inválida"
    
    return True, None


def validate_user_data(data: Dict) -> tuple[bool, Optional[str]]:
    """
    Valida los datos de un usuario
    Args:
        data: Diccionario con los datos del usuario
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not data.get('username'):
        return False, "El nombre de usuario es requerido"
    
    if len(data.get('username', '')) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if not data.get('password_hash'):
        return False, "La contraseña es requerida"
    
    # Validar email si existe
    email = data.get('email', '')
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "Email inválido"
    
    return True, None

