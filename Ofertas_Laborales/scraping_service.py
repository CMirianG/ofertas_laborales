#!/usr/bin/env python3
"""
Servicio de Scraping Independiente
Extrae ofertas laborales de múltiples portales y las almacena en MongoDB
Puede ejecutarse de forma independiente del backend Flask
"""

import requests
from bs4 import BeautifulSoup
import re
import hashlib
import logging
import time
import random
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from mongodb_database import MongoDBManager

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

class ScrapingService:
    """Servicio independiente de scraping de ofertas laborales"""
    
    def __init__(self, db_manager: MongoDBManager = None):
        """
        Inicializa el servicio de scraping
        Args:
            db_manager: Instancia de MongoDBManager (opcional)
        """
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager or MongoDBManager()
        
        # Estadísticas de extracción
        self.stats = {
            'total_encontradas': 0,
            'nuevas': 0,
            'actualizadas': 0,
            'errores': 0,
            'por_fuente': {}
        }
    
    def _get_random_user_agent(self) -> str:
        """Retorna un User-Agent aleatorio"""
        return random.choice(self.user_agents)
    
    def _make_request(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """
        Realiza una solicitud HTTP con reintentos
        Args:
            url: URL a consultar
            retries: Número de reintentos
        Returns:
            BeautifulSoup object o None si falla
        """
        for attempt in range(retries):
            try:
                self.session.headers.update({
                    'User-Agent': self._get_random_user_agent(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                })
                
                self.logger.info(f"Realizando request a: {url} (Intento {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                self.logger.info(f"✓ Request exitoso a {url}")
                return BeautifulSoup(response.content, 'html.parser')
                
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"Error HTTP {e.response.status_code}: {url}")
                if e.response.status_code == 403:
                    self.logger.warning("Acceso denegado (403). Esperando antes de reintentar...")
                    time.sleep(random.uniform(10, 20))
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error de conexión: {e}")
                
            # Espera entre reintentos
            if attempt < retries - 1:
                wait_time = random.uniform(5 * (attempt + 1), 10 * (attempt + 1))
                self.logger.info(f"Esperando {wait_time:.1f}s antes del siguiente intento...")
                time.sleep(wait_time)
        
        self.logger.error(f"✗ Falló la extracción de {url} después de {retries} intentos")
        return None
    
    def _generate_id(self, url: str, titulo: str) -> str:
        """Genera un ID único para la oferta"""
        base_url = urlparse(url).netloc + urlparse(url).path
        content = f"{base_url}_{titulo}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    
    def _is_tacna_location(self, text: str) -> bool:
        """Verifica si la ubicación menciona Tacna"""
        if not text:
            return False
        
        text_lower = text.lower()
        tacna_patterns = [
            r'\btacna\b', r'\btacneñ[oa]s?\b', 
            r'provincia de tacna', r'departamento de tacna',
            r'región tacna', r'tacna,', r', tacna'
        ]
        
        return any(re.search(pattern, text_lower) for pattern in tacna_patterns)
    
    def _extract_salary(self, text: str) -> str:
        """Extrae información de salario del texto"""
        if not text:
            return "No especificado"
        
        text_clean = text.replace(' ', '').replace(',', '')
        
        # Buscar rangos (1000-1500, S/1000-1500)
        range_match = re.search(r'(?:s/|soles?|pen)?(\d+\.?\d*)(?:[-–—])(?:s/|soles?|pen)?(\d+\.?\d*)', text_clean, re.IGNORECASE)
        if range_match:
            val1 = float(range_match.group(1))
            val2 = float(range_match.group(2))
            return f"S/ {min(val1, val2):,.2f} - S/ {max(val1, val2):,.2f}"
        
        # Buscar valor único
        single_match = re.search(r'(?:s/|soles?|pen)(\d+\.?\d*)', text_clean, re.IGNORECASE)
        if single_match:
            return f"S/ {float(single_match.group(1)):,.2f}"
        
        # Buscar "desde" o "hasta"
        desde_match = re.search(r'desde\s*(?:s/|soles?|pen)?(\d+\.?\d*)', text, re.IGNORECASE)
        hasta_match = re.search(r'hasta\s*(?:s/|soles?|pen)?(\d+\.?\d*)', text, re.IGNORECASE)
        
        if desde_match and hasta_match:
            return f"S/ {float(desde_match.group(1)):,.2f} - S/ {float(hasta_match.group(1)):,.2f}"
        elif desde_match:
            return f"Desde S/ {float(desde_match.group(1)):,.2f}"
        elif hasta_match:
            return f"Hasta S/ {float(hasta_match.group(1)):,.2f}"
        
        return "No especificado"
    
    def _extract_experience(self, text: str) -> int:
        """Extrae años de experiencia requeridos"""
        if not text:
            return 0
        
        patterns = [
            r'(\d+)\s*(?:a[ñn]os?|years?)\s*(?:de\s*)?(?:experiencia|exp)',
            r'experiencia\s*(?:de\s*)?(\d+)\s*(?:a[ñn]os?|years?)',
            r'mínimo\s*(\d+)\s*(?:a[ñn]os?|years?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0
    
    def _normalize_academic_level(self, text: str) -> str:
        """Normaliza el nivel académico"""
        if not text:
            return "Bachiller"
        
        text_lower = text.lower()
        
        # Practicantes
        if any(word in text_lower for word in ['practicante', 'prácticas', 'pasantía', 'estudiante', 'pre-profesional']):
            return "Practicante"
        
        # Profesionales
        elif any(word in text_lower for word in ['universitario', 'título', 'licenciado', 'profesional', 'técnico superior', 'egresado universitario']):
            return "Profesional"
        
        # Bachilleres
        elif any(word in text_lower for word in ['bachiller', 'bachillerato', 'secundaria completa', 'egresado']):
            return "Bachiller"
        
        return "Bachiller"
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> str:
        """Extrae palabras clave técnicas y relevantes"""
        if not text:
            return ""
        
        # Palabras clave técnicas y de habilidades
        keywords_list = [
            # Tecnología
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'php', 'ruby',
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'database',
            'html', 'css', 'bootstrap', 'jquery', 'ajax', 'json', 'xml', 'rest', 'api',
            'git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'cloud', 'devops',
            'linux', 'windows', 'unix', 'bash', 'powershell',
            
            # Office y herramientas
            'excel', 'word', 'powerpoint', 'office', 'google workspace', 'microsoft office',
            'sap', 'erp', 'crm', 'salesforce',
            
            # Marketing y ventas
            'marketing digital', 'seo', 'sem', 'redes sociales', 'content marketing',
            'ventas', 'negociación', 'atención al cliente', 'comercial',
            
            # Soft skills
            'comunicación', 'liderazgo', 'trabajo en equipo', 'gestión de proyectos',
            'agile', 'scrum', 'planificación', 'organización',
            
            # Áreas profesionales
            'administración', 'contabilidad', 'finanzas', 'auditoría', 'tributación',
            'recursos humanos', 'rrhh', 'selección', 'capacitación',
            'logística', 'cadena de suministro', 'almacén', 'inventario',
            'ingeniería', 'mantenimiento', 'producción', 'calidad',
            'enfermería', 'salud', 'medicina', 'farmacia',
            'diseño gráfico', 'autocad', 'solidworks', 'photoshop', 'illustrator',
            
            # Idiomas
            'inglés', 'english', 'portugués', 'francés'
        ]
        
        found_keywords = set()
        text_lower = text.lower()
        
        for keyword in keywords_list:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                found_keywords.add(keyword)
                if len(found_keywords) >= max_keywords:
                    break
        
        return ', '.join(sorted(list(found_keywords)))
    
    def _extract_detailed_info(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extrae información detallada de la página de la oferta
        Args:
            soup: BeautifulSoup object de la página
            url: URL de la oferta
        Returns:
            Diccionario con información adicional
        """
        info = {
            'descripcion_completa': '',
            'requisitos': [],
            'beneficios': [],
            'horario': '',
            'tipo_contrato': ''
        }
        
        try:
            # Buscar descripción completa
            desc_selectors = [
                '.job-description', '.descripcion', '.description',
                '#jobDescriptionText', '[id*="description"]',
                'article', 'section[class*="description"]'
            ]
            
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem and len(desc_elem.get_text(strip=True)) > 100:
                    info['descripcion_completa'] = desc_elem.get_text(strip=True)[:1000]
                    break
            
            # Extraer requisitos (buscar listas o secciones de requisitos)
            requisitos_keywords = ['requisito', 'requirement', 'requerir', 'necesit']
            for keyword in requisitos_keywords:
                req_section = soup.find(text=re.compile(keyword, re.IGNORECASE))
                if req_section:
                    parent = req_section.find_parent(['div', 'section', 'article'])
                    if parent:
                        bullets = parent.find_all(['li', 'p'])
                        info['requisitos'] = [b.get_text(strip=True) for b in bullets[:5] if len(b.get_text(strip=True)) > 10]
                        break
            
            # Extraer beneficios
            beneficios_keywords = ['beneficio', 'benefit', 'ofrece']
            for keyword in beneficios_keywords:
                ben_section = soup.find(text=re.compile(keyword, re.IGNORECASE))
                if ben_section:
                    parent = ben_section.find_parent(['div', 'section', 'article'])
                    if parent:
                        bullets = parent.find_all(['li', 'p'])
                        info['beneficios'] = [b.get_text(strip=True) for b in bullets[:5] if len(b.get_text(strip=True)) > 10]
                        break
            
            # Extraer horario y tipo de contrato del texto
            text = soup.get_text()
            horario_match = re.search(r'(?:horario|schedule):?\s*([^\n.]+)', text, re.IGNORECASE)
            if horario_match:
                info['horario'] = horario_match.group(1).strip()[:100]
            
            contrato_match = re.search(r'(?:contrato|tipo de contrato|contract type):?\s*([^\n.]+)', text, re.IGNORECASE)
            if contrato_match:
                info['tipo_contrato'] = contrato_match.group(1).strip()[:100]
                
        except Exception as e:
            self.logger.error(f"Error extrayendo información detallada: {e}")
        
        return info
    
    def _extract_from_portal(self, portal_name: str, url: str, container_selectors: List[str]) -> List[Dict]:
        """
        Método genérico para extraer ofertas de un portal
        Args:
            portal_name: Nombre del portal
            url: URL del portal
            container_selectors: Lista de selectores CSS para contenedores de ofertas
        Returns:
            Lista de ofertas extraídas
        """
        ofertas = []
        soup = self._make_request(url)
        
        if not soup:
            self.logger.error(f"No se pudo obtener contenido de {portal_name}")
            return ofertas
        
        # Intentar con diferentes selectores
        job_containers = []
        for selector in container_selectors:
            if ',' in selector:
                # Selector CSS con múltiples opciones
                job_containers = soup.select(selector)
            else:
                # Selector de clase simple
                job_containers = soup.find_all('div', class_=re.compile(selector))
            
            if job_containers:
                self.logger.info(f"✓ Encontrados {len(job_containers)} contenedores en {portal_name} usando selector: {selector}")
                break
        
        if not job_containers:
            self.logger.warning(f"No se encontraron contenedores en {portal_name}")
            return ofertas
        
        for container in job_containers:
            try:
                # Extraer título y URL
                titulo = None
                url_oferta = None
                
                for title_sel in ['h2 a', 'h3 a', 'a[title]', 'a[data-jk]']:
                    title_elem = container.select_one(title_sel)
                    if title_elem:
                        titulo = title_elem.get('title') or title_elem.get_text(strip=True)
                        url_oferta = title_elem.get('href', '')
                        break
                
                if not titulo or not url_oferta:
                    continue
                
                # Normalizar URL
                if not url_oferta.startswith('http'):
                    url_oferta = urljoin(url, url_oferta)
                
                # Extraer otros campos
                empresa = "No especificado"
                ubicacion = ""
                descripcion = ""
                
                # Empresa
                for emp_sel in ['.company-name', '.empresa', '[class*="company"]']:
                    emp_elem = container.select_one(emp_sel)
                    if emp_elem:
                        empresa = emp_elem.get_text(strip=True)
                        break
                
                # Ubicación
                for loc_sel in ['.location', '.ubicacion', '[class*="location"]']:
                    loc_elem = container.select_one(loc_sel)
                    if loc_elem:
                        ubicacion = loc_elem.get_text(strip=True)
                        break
                
                # Descripción
                desc_elem = container.find(['p', 'div'], class_=re.compile('description|snippet|summary'))
                if desc_elem:
                    descripcion = desc_elem.get_text(strip=True)
                
                # Validar que sea de Tacna
                if not self._is_tacna_location(ubicacion):
                    continue
                
                # Crear oferta
                oferta = {
                    'id': self._generate_id(url_oferta, titulo),
                    'titulo_oferta': titulo[:80],
                    'empresa': empresa[:100],
                    'nivel_academico': self._normalize_academic_level(descripcion),
                    'puesto': titulo[:100],
                    'experiencia_minima_anios': self._extract_experience(descripcion),
                    'conocimientos_clave': self._extract_keywords(descripcion + " " + titulo),
                    'responsabilidades_breve': descripcion[:200] if descripcion else "Ver detalles en la oferta",
                    'modalidad': self._extract_modalidad(descripcion),
                    'ubicacion': f"Tacna — {ubicacion}" if ubicacion else "Tacna",
                    'jornada': self._extract_jornada(descripcion),
                    'salario': self._extract_salary(descripcion),
                    'fecha_publicacion': datetime.now().strftime('%Y-%m-%d'),
                    'fecha_cierre': None,
                    'como_postular': f"Postular en: {url_oferta}",
                    'url_oferta': url_oferta,
                    'documentos_requeridos': "CV actualizado",
                    'contacto': "Ver en la oferta",
                    'etiquetas': f"{portal_name.lower()}, tacna",
                    'fuente': portal_name,
                    'fecha_estimacion': False
                }
                
                ofertas.append(oferta)
                self.logger.info(f"✓ Oferta extraída: {titulo[:50]}")
                
            except Exception as e:
                self.logger.error(f"Error procesando oferta de {portal_name}: {e}")
                continue
        
        return ofertas
    
    def _extract_modalidad(self, text: str) -> str:
        """Extrae la modalidad de trabajo"""
        if not text:
            return "No especificado"
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['remoto', 'remote', 'home office', 'teletrabajo']):
            return "Remoto"
        elif any(word in text_lower for word in ['híbrido', 'hybrid', 'mixto']):
            return "Híbrido"
        elif any(word in text_lower for word in ['presencial', 'oficina', 'on-site']):
            return "Presencial"
        
        return "Presencial"  # Por defecto
    
    def _extract_jornada(self, text: str) -> str:
        """Extrae el tipo de jornada"""
        if not text:
            return "No especificado"
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['tiempo completo', 'full time', 'jornada completa']):
            return "Tiempo completo"
        elif any(word in text_lower for word in ['medio tiempo', 'part time', 'parcial']):
            return "Medio tiempo"
        elif any(word in text_lower for word in ['por horas', 'freelance', 'temporal']):
            return "Por horas"
        
        return "Tiempo completo"  # Por defecto
    
    def extract_computrabajo(self) -> List[Dict]:
        """Extrae ofertas de Computrabajo"""
        self.logger.info("=== Extrayendo de Computrabajo ===")
        return self._extract_from_portal(
            portal_name="Computrabajo",
            url="https://pe.computrabajo.com/empleos-en-tacna",
            container_selectors=['box_border mbB', 'box_border', 'article']
        )
    
    def extract_indeed(self) -> List[Dict]:
        """Extrae ofertas de Indeed"""
        self.logger.info("=== Extrayendo de Indeed ===")
        return self._extract_from_portal(
            portal_name="Indeed",
            url="https://pe.indeed.com/jobs?q=&l=Tacna%2C+Tacna",
            container_selectors=['job_seen_beacon', 'jobsearch-SerpJobCard', 'resultWithShelf']
        )
    
    def extract_bumeran(self) -> List[Dict]:
        """Extrae ofertas de Bumeran"""
        self.logger.info("=== Extrayendo de Bumeran ===")
        return self._extract_from_portal(
            portal_name="Bumeran",
            url="https://www.bumeran.com.pe/en-tacna/empleos.html",
            container_selectors=['sc-1xf2q6u-0', 'card-vacancy', 'list-group-item']
        )
    
    def extract_trabajos_pe(self) -> List[Dict]:
        """Extrae ofertas de Trabajos.pe"""
        self.logger.info("=== Extrayendo de Trabajos.pe ===")
        return self._extract_from_portal(
            portal_name="Trabajos.pe",
            url="https://www.trabajos.pe/trabajo-tacna",
            container_selectors=['content-jobs__item', 'job-card', 'oferta-item']
        )
    
    def run_scraping(self, portals: List[str] = None) -> Dict:
        """
        Ejecuta el scraping de todos los portales especificados
        Args:
            portals: Lista de portales a extraer. Si es None, extrae de todos
        Returns:
            Diccionario con estadísticas de extracción
        """
        start_time = time.time()
        
        # Portales disponibles
        available_portals = {
            'computrabajo': self.extract_computrabajo,
            'indeed': self.extract_indeed,
            'bumeran': self.extract_bumeran,
            'trabajos': self.extract_trabajos_pe
        }
        
        # Si no se especifican portales, extraer de todos
        if not portals:
            portals = list(available_portals.keys())
        
        all_ofertas = []
        
        for portal_name in portals:
            if portal_name.lower() not in available_portals:
                self.logger.warning(f"Portal no reconocido: {portal_name}")
                continue
            
            try:
                extractor_func = available_portals[portal_name.lower()]
                ofertas = extractor_func()
                all_ofertas.extend(ofertas)
                
                self.stats['por_fuente'][portal_name] = len(ofertas)
                self.stats['total_encontradas'] += len(ofertas)
                
                self.logger.info(f"✓ {portal_name}: {len(ofertas)} ofertas extraídas")
                
                # Pausa entre portales
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                self.logger.error(f"✗ Error en {portal_name}: {e}")
                self.stats['errores'] += 1
        
        # Guardar en base de datos
        self.logger.info(f"\n=== Guardando {len(all_ofertas)} ofertas en MongoDB ===")
        
        for oferta in all_ofertas:
            try:
                if self.db_manager.insert_oferta(oferta):
                    self.stats['nuevas'] += 1
                else:
                    self.stats['actualizadas'] += 1
            except Exception as e:
                self.logger.error(f"Error guardando oferta: {e}")
                self.stats['errores'] += 1
        
        duration = time.time() - start_time
        
        # Registrar log de extracción
        log_data = {
            'fuente': ', '.join(portals),
            'ofertas_encontradas': self.stats['total_encontradas'],
            'ofertas_nuevas': self.stats['nuevas'],
            'ofertas_actualizadas': self.stats['actualizadas'],
            'errores': self.stats['errores'],
            'duracion_segundos': int(duration),
            'detalles': str(self.stats)
        }
        
        self.db_manager.insert_log_extraccion(log_data)
        
        # Resumen
        self.logger.info("\n" + "="*60)
        self.logger.info("RESUMEN DE EXTRACCIÓN")
        self.logger.info("="*60)
        self.logger.info(f"Total encontradas: {self.stats['total_encontradas']}")
        self.logger.info(f"Nuevas: {self.stats['nuevas']}")
        self.logger.info(f"Actualizadas: {self.stats['actualizadas']}")
        self.logger.info(f"Errores: {self.stats['errores']}")
        self.logger.info(f"Duración: {duration:.2f} segundos")
        self.logger.info(f"\nPor fuente:")
        for fuente, count in self.stats['por_fuente'].items():
            self.logger.info(f"  - {fuente}: {count}")
        self.logger.info("="*60)
        
        return self.stats


def main():
    """Función principal para ejecutar el servicio"""
    parser = argparse.ArgumentParser(description='Servicio de Scraping de Ofertas Laborales')
    parser.add_argument(
        '--portals',
        nargs='+',
        choices=['computrabajo', 'indeed', 'bumeran', 'trabajos', 'all'],
        default=['all'],
        help='Portales a extraer (por defecto: all)'
    )
    parser.add_argument(
        '--mongodb-uri',
        type=str,
        default='mongodb://localhost:27017/',
        help='URI de conexión a MongoDB'
    )
    
    args = parser.parse_args()
    
    # Inicializar servicio
    try:
        db_manager = MongoDBManager(args.mongodb_uri)
        service = ScrapingService(db_manager)
        
        portals = None if 'all' in args.portals else args.portals
        
        # Ejecutar scraping
        service.run_scraping(portals)
        
    except Exception as e:
        logging.error(f"Error ejecutando el servicio: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

