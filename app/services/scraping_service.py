#!/usr/bin/env python3
"""
Servicio de Scraping Independiente
Extrae ofertas laborales de múltiples portales usando contenedores
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
from app.services.database_service import MongoDBManager

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
                    'Upgrade-Insecure-Requests': '1',
                    'Referer': 'https://www.google.com/'
                })
                
                self.logger.info(f"Realizando request a: {url} (Intento {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=20, allow_redirects=True)
                response.raise_for_status()
                
                # Verificar que sea HTML
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    self.logger.warning(f"Respuesta no es HTML: {response.headers.get('Content-Type')}")
                    continue
                
                self.logger.info(f"✓ Request exitoso a {url} ({len(response.content)} bytes)")
                return BeautifulSoup(response.content, 'html.parser')
                
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"Error HTTP {e.response.status_code}: {url}")
                if e.response.status_code == 403:
                    self.logger.warning("Acceso denegado (403). Esperando antes de reintentar...")
                    time.sleep(random.uniform(15, 25))
                elif e.response.status_code == 429:
                    self.logger.warning("Rate limit (429). Esperando más tiempo...")
                    time.sleep(random.uniform(30, 60))
                    
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
        content = f"{base_url}_{titulo}".encode('utf-8')
        return hashlib.md5(content).hexdigest()[:16]
    
    def _is_tacna_location(self, text: str) -> bool:
        """Verifica si la ubicación menciona Tacna"""
        if not text:
            return False
        
        text_lower = text.lower()
        tacna_patterns = [
            r'\btacna\b', r'\btacneñ[oa]s?\b', 
            r'provincia de tacna', r'departamento de tacna',
            r'región tacna', r'tacna,', r', tacna', r'tacna\s*perú'
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
        
        keywords_list = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'php', 'ruby',
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'database',
            'html', 'css', 'bootstrap', 'jquery', 'ajax', 'json', 'xml', 'rest', 'api',
            'git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'cloud', 'devops',
            'linux', 'windows', 'unix', 'bash', 'powershell',
            'excel', 'word', 'powerpoint', 'office', 'google workspace', 'microsoft office',
            'sap', 'erp', 'crm', 'salesforce',
            'marketing digital', 'seo', 'sem', 'redes sociales', 'content marketing',
            'ventas', 'negociación', 'atención al cliente', 'comercial',
            'comunicación', 'liderazgo', 'trabajo en equipo', 'gestión de proyectos',
            'agile', 'scrum', 'planificación', 'organización',
            'administración', 'contabilidad', 'finanzas', 'auditoría', 'tributación',
            'recursos humanos', 'rrhh', 'selección', 'capacitación',
            'logística', 'cadena de suministro', 'almacén', 'inventario',
            'ingeniería', 'mantenimiento', 'producción', 'calidad',
            'enfermería', 'salud', 'medicina', 'farmacia',
            'diseño gráfico', 'autocad', 'solidworks', 'photoshop', 'illustrator',
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
    
    def _extract_modalidad(self, text: str) -> str:
        """Extrae la modalidad de trabajo"""
        if not text:
            return "Presencial"
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['remoto', 'remote', 'home office', 'teletrabajo']):
            return "Remoto"
        elif any(word in text_lower for word in ['híbrido', 'hybrid', 'mixto']):
            return "Híbrido"
        elif any(word in text_lower for word in ['presencial', 'oficina', 'on-site']):
            return "Presencial"
        
        return "Presencial"
    
    def _extract_jornada(self, text: str) -> str:
        """Extrae el tipo de jornada"""
        if not text:
            return "Tiempo completo"
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['tiempo completo', 'full time', 'jornada completa']):
            return "Tiempo completo"
        elif any(word in text_lower for word in ['medio tiempo', 'part time', 'parcial']):
            return "Medio tiempo"
        elif any(word in text_lower for word in ['por horas', 'freelance', 'temporal']):
            return "Por horas"
        
        return "Tiempo completo"
    
    def _extract_from_container(self, container, portal_name: str, base_url: str) -> Optional[Dict]:
        """
        Extrae datos de una oferta desde un contenedor
        Args:
            container: BeautifulSoup element del contenedor
            portal_name: Nombre del portal
            base_url: URL base del portal
        Returns:
            Diccionario con datos de la oferta o None si no es válida
        """
        try:
            # Extraer título y URL - múltiples estrategias
            titulo = None
            url_oferta = None
            
            # Estrategia 1: Buscar enlaces con título
            title_selectors = [
                'h2 a', 'h3 a', 'h4 a',  # Títulos con enlaces
                'a[title]',  # Enlaces con atributo title
                'a[data-jk]',  # Indeed
                'a.job-title', 'a.title',  # Clases comunes
                '.title a', '.job-title a',  # Contenedores con clase title
            ]
            
            for selector in title_selectors:
                title_elem = container.select_one(selector)
                if title_elem:
                    titulo = title_elem.get('title', '').strip() or title_elem.get_text(strip=True)
                    url_oferta = title_elem.get('href', '')
                    if titulo and url_oferta:
                        break
            
            # Estrategia 2: Si no hay enlace, buscar título directo
            if not titulo:
                for tag in ['h2', 'h3', 'h4', 'h5']:
                    title_tag = container.find(tag)
                    if title_tag:
                        titulo = title_tag.get_text(strip=True)
                        # Buscar enlace cercano
                        link = container.find('a', href=True)
                        if link:
                            url_oferta = link.get('href', '')
                        break
            
            if not titulo:
                self.logger.debug("No se encontró título en el contenedor")
                return None
            
            # Normalizar URL
            if url_oferta:
                if not url_oferta.startswith('http'):
                    url_oferta = urljoin(base_url, url_oferta)
            else:
                # Si no hay URL, generar una basada en el título
                url_oferta = f"{base_url}#{hashlib.md5(titulo.encode()).hexdigest()[:8]}"
            
            # Extraer empresa - múltiples estrategias
            empresa = "No especificado"
            empresa_selectors = [
                '.company-name', '.empresa', '.company', '[class*="company"]',
                '[class*="empresa"]', '.employer', '[data-company]',
                'span.company', 'div.company', 'a.company'
            ]
            
            for selector in empresa_selectors:
                emp_elem = container.select_one(selector)
                if emp_elem:
                    empresa = emp_elem.get_text(strip=True)
                    if empresa and empresa != "No especificado":
                        break
            
            # Si no se encuentra, buscar en atributos data
            if empresa == "No especificado":
                emp_attr = container.get('data-company') or container.find(attrs={'data-company': True})
                if emp_attr:
                    empresa = emp_attr if isinstance(emp_attr, str) else emp_attr.get('data-company', '')
            
            # Extraer ubicación - múltiples estrategias
            ubicacion = ""
            location_selectors = [
                '.location', '.ubicacion', '[class*="location"]', '[class*="ubicacion"]',
                '.city', '.ciudad', '[data-location]', 'span.location', 'div.location'
            ]
            
            for selector in location_selectors:
                loc_elem = container.select_one(selector)
                if loc_elem:
                    ubicacion = loc_elem.get_text(strip=True)
                    if ubicacion:
                        break
            
            # Validar que sea de Tacna
            if not self._is_tacna_location(ubicacion):
                self.logger.debug(f"Oferta descartada - no es de Tacna: {ubicacion}")
                return None
            
            # Extraer descripción/snippet
            descripcion = ""
            desc_selectors = [
                '.description', '.snippet', '.summary', '[class*="description"]',
                '[class*="snippet"]', 'p.description', 'div.description'
            ]
            
            for selector in desc_selectors:
                desc_elem = container.select_one(selector)
                if desc_elem:
                    descripcion = desc_elem.get_text(strip=True)
                    if descripcion:
                        break
            
            # Si no hay descripción, usar todo el texto del contenedor (limitado)
            if not descripcion:
                descripcion = container.get_text(separator=' ', strip=True)[:300]
            
            # Extraer salario
            salario = "No especificado"
            salary_selectors = [
                '.salary', '.salario', '[class*="salary"]', '[class*="salario"]',
                '[data-salary]', 'span.salary', 'div.salary'
            ]
            
            for selector in salary_selectors:
                sal_elem = container.select_one(selector)
                if sal_elem:
                    salario_text = sal_elem.get_text(strip=True)
                    salario = self._extract_salary(salario_text)
                    if salario != "No especificado":
                        break
            
            # Si no se encuentra salario, buscar en el texto completo
            if salario == "No especificado":
                full_text = container.get_text()
                salario = self._extract_salary(full_text)
            
            # Crear oferta
            oferta = {
                'id': self._generate_id(url_oferta, titulo),
                'titulo_oferta': titulo[:80] if titulo else "Sin título",
                'empresa': empresa[:100] if empresa else "No especificado",
                'nivel_academico': self._normalize_academic_level(descripcion + " " + titulo),
                'puesto': titulo[:100] if titulo else "Sin especificar",
                'experiencia_minima_anios': self._extract_experience(descripcion + " " + titulo),
                'conocimientos_clave': self._extract_keywords(descripcion + " " + titulo),
                'responsabilidades_breve': descripcion[:200] if descripcion else "Ver detalles en la oferta",
                'modalidad': self._extract_modalidad(descripcion + " " + titulo),
                'ubicacion': f"Tacna — {ubicacion}" if ubicacion and ubicacion.lower() != 'tacna' else "Tacna",
                'jornada': self._extract_jornada(descripcion),
                'salario': salario,
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
            
            return oferta
            
        except Exception as e:
            self.logger.error(f"Error extrayendo datos del contenedor: {e}")
            return None
    
    def _extract_from_portal(self, portal_name: str, url: str, container_selectors: List[str]) -> List[Dict]:
        """
        Método genérico para extraer ofertas de un portal usando contenedores
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
        
        # Intentar con diferentes selectores de contenedores
        job_containers = []
        for selector in container_selectors:
            try:
                # Intentar como selector CSS
                containers = soup.select(selector)
                if containers:
                    job_containers = containers
                    self.logger.info(f"✓ Encontrados {len(containers)} contenedores en {portal_name} usando selector CSS: {selector}")
                    break
            except Exception as e:
                self.logger.debug(f"Selector CSS falló: {selector} - {e}")
            
            # Intentar como búsqueda por clase
            try:
                if '.' in selector:
                    class_name = selector.replace('.', '')
                    containers = soup.find_all(['div', 'article', 'li', 'section'], class_=re.compile(class_name, re.IGNORECASE))
                    if containers:
                        job_containers = containers
                        self.logger.info(f"✓ Encontrados {len(containers)} contenedores en {portal_name} usando clase: {class_name}")
                        break
            except Exception as e:
                self.logger.debug(f"Búsqueda por clase falló: {selector} - {e}")
            
            # Intentar como búsqueda por atributo
            try:
                if '[' in selector:
                    # Selector de atributo como [data-id]
                    containers = soup.find_all(attrs={'data-id': True}) or soup.find_all(attrs={'data-job': True})
                    if containers:
                        job_containers = containers
                        self.logger.info(f"✓ Encontrados {len(containers)} contenedores en {portal_name} usando atributos")
                        break
            except Exception as e:
                self.logger.debug(f"Búsqueda por atributo falló: {selector} - {e}")
        
        if not job_containers:
            self.logger.warning(f"No se encontraron contenedores en {portal_name} con ningún selector")
            # Intentar búsqueda genérica de contenedores comunes
            generic_containers = soup.find_all(['article', 'div'], class_=re.compile(r'job|oferta|vacante|card', re.IGNORECASE))
            if generic_containers:
                job_containers = generic_containers
                self.logger.info(f"✓ Encontrados {len(generic_containers)} contenedores genéricos en {portal_name}")
            else:
                return ofertas
        
        # Procesar cada contenedor
        for idx, container in enumerate(job_containers, 1):
            try:
                oferta = self._extract_from_container(container, portal_name, url)
                if oferta:
                    ofertas.append(oferta)
                    self.logger.debug(f"✓ Oferta {idx}/{len(job_containers)} extraída: {oferta['titulo_oferta'][:50]}")
                else:
                    self.logger.debug(f"✗ Contenedor {idx}/{len(job_containers)} descartado")
            except Exception as e:
                self.logger.error(f"Error procesando contenedor {idx} de {portal_name}: {e}")
                continue
            
            # Pequeña pausa entre ofertas
            if idx % 10 == 0:
                time.sleep(0.5)
        
        self.logger.info(f"✓ {portal_name}: {len(ofertas)} ofertas válidas extraídas de {len(job_containers)} contenedores")
        return ofertas
    
    def extract_computrabajo(self) -> List[Dict]:
        """Extrae ofertas de Computrabajo usando contenedores"""
        self.logger.info("=== Extrayendo de Computrabajo ===")
        return self._extract_from_portal(
            portal_name="Computrabajo",
            url="https://pe.computrabajo.com/empleos-en-tacna",
            container_selectors=[
                'article[data-id]',  # Artículos con data-id
                'div.box_border',  # Contenedores con clase box_border
                'div[class*="box_border"]',  # Variaciones
                'article.box_border',  # Artículos con box_border
                'div.o_oferta',  # Clase específica de ofertas
                'article.o_oferta'  # Artículos de ofertas
            ]
        )
    
    def extract_indeed(self) -> List[Dict]:
        """Extrae ofertas de Indeed usando contenedores"""
        self.logger.info("=== Extrayendo de Indeed ===")
        return self._extract_from_portal(
            portal_name="Indeed",
            url="https://pe.indeed.com/jobs?q=&l=Tacna%2C+Tacna",
            container_selectors=[
                'div[data-jk]',  # Contenedores con data-jk (Indeed)
                'div.job_seen_beacon',  # Clase específica de Indeed
                'div[class*="job_seen"]',  # Variaciones
                'div.resultWithShelf',  # Resultados con estante
                'div[class*="result"]',  # Resultados genéricos
                'div.jobsearch-SerpJobCard'  # Tarjeta de trabajo
            ]
        )
    
    def extract_bumeran(self) -> List[Dict]:
        """Extrae ofertas de Bumeran usando contenedores"""
        self.logger.info("=== Extrayendo de Bumeran ===")
        return self._extract_from_portal(
            portal_name="Bumeran",
            url="https://www.bumeran.com.pe/en-tacna/empleos.html",
            container_selectors=[
                'div[class*="sc-"]',  # Componentes styled-components
                'div.card-vacancy',  # Tarjetas de vacantes
                'div[class*="card"]',  # Cualquier tarjeta
                'li.list-group-item',  # Items de lista
                'div[class*="vacancy"]',  # Contenedores de vacantes
                'article[class*="job"]'  # Artículos de trabajo
            ]
        )
    
    def extract_trabajos_pe(self) -> List[Dict]:
        """Extrae ofertas de Trabajos.pe usando contenedores"""
        self.logger.info("=== Extrayendo de Trabajos.pe ===")
        return self._extract_from_portal(
            portal_name="Trabajos.pe",
            url="https://www.trabajos.pe/trabajo-tacna",
            container_selectors=[
                'div.content-jobs__item',  # Items de contenido de trabajos
                'div[class*="content-jobs"]',  # Contenedores de trabajos
                'div.job-card',  # Tarjetas de trabajo
                'div[class*="job-card"]',  # Variaciones
                'div.oferta-item',  # Items de ofertas
                'article[class*="oferta"]'  # Artículos de ofertas
            ]
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
        
        # Resetear estadísticas
        self.stats = {
            'total_encontradas': 0,
            'nuevas': 0,
            'actualizadas': 0,
            'errores': 0,
            'por_fuente': {}
        }
        
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
                if portal_name != portals[-1]:  # No pausar después del último
                    time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                self.logger.error(f"✗ Error en {portal_name}: {e}", exc_info=True)
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
        try:
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
        except Exception as e:
            self.logger.warning(f"No se pudo guardar log de extracción: {e}")
        
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
        logging.error(f"Error ejecutando el servicio: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
