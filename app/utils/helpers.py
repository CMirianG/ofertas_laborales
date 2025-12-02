"""
Funciones auxiliares
"""
from datetime import datetime
import hashlib
from typing import Optional


def format_date(date_value) -> Optional[str]:
    """
    Formatea una fecha a string ISO
    Args:
        date_value: Fecha (datetime, string o None)
    Returns:
        String con la fecha en formato ISO o None
    """
    if date_value is None:
        return None
    
    if isinstance(date_value, datetime):
        return date_value.isoformat()
    
    if isinstance(date_value, str):
        return date_value
    
    return None


def generate_oferta_id(url: str, titulo: str = None) -> str:
    """
    Genera un ID único para una oferta basado en su URL y título
    Args:
        url: URL de la oferta
        titulo: Título de la oferta (opcional)
    Returns:
        String con el ID único
    """
    if titulo:
        data = f"{url}_{titulo}"
    else:
        data = url
    
    return hashlib.md5(data.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Trunca un texto a una longitud máxima
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
    Returns:
        Texto truncado con "..." si es necesario
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

