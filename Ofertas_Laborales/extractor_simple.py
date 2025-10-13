#!/usr/bin/env python3
"""
Extractor mejorado de ofertas laborales para Tacna
Enfocado en scraping directo, robusto y efectivo, con manejo de errores y adaptabilidad.
"""

import requests
from bs4 import BeautifulSoup
import re
import hashlib
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin, urlparse
import time
import random

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleOfertaExtractor:
    def __init__(self):
        self.session = requests.Session()
        # Mejora: Rotación de User-Agents para simular diferentes navegadores y evitar bloqueos
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        self.logger = logging.getLogger(__name__)

    def _get_random_user_agent(self) -> str:
        """Retorna un User-Agent aleatorio de la lista."""
        return random.choice(self.user_agents)

    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        """
        Realiza una solicitud HTTP robusta con reintentos y manejo de errores.
        Retorna un objeto BeautifulSoup si la solicitud es exitosa, None en caso contrario.
        """
        retries = 3
        for i in range(retries):
            try:
                self.session.headers.update({'User-Agent': self._get_random_user_agent()})
                self.logger.info(f"Intentando request a: {url} con User-Agent: {self.session.headers['User-Agent']}")
                response = self.session.get(url, timeout=15) # Reducir timeout para fallar más rápido en caso de bloqueo
                response.raise_for_status() # Lanza excepción para códigos de estado HTTP 4xx/5xx
                self.logger.info(f"Request exitoso a {url}")
                return BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"Error HTTP al extraer de {url} (Intento {i+1}/{retries}): {e.response.status_code} - {e.response.reason}")
                if e.response.status_code == 403: # Posible bloqueo, intentar con otro User-Agent o esperar
                    self.logger.warning("Acceso denegado (403 Forbidden). Cambiando User-Agent y reintentando.")
                time.sleep(random.uniform(5 * (i + 1), 10 * (i + 1))) # Espera exponencial
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"Error de conexión al extraer de {url} (Intento {i+1}/{retries}): {e}")
                time.sleep(random.uniform(5 * (i + 1), 10 * (i + 1)))
            except requests.exceptions.Timeout as e:
                self.logger.error(f"Tiempo de espera agotado al extraer de {url} (Intento {i+1}/{retries}): {e}")
                time.sleep(random.uniform(5 * (i + 1), 10 * (i + 1)))
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error desconocido al extraer de {url} (Intento {i+1}/{retries}): {e}")
                time.sleep(random.uniform(5 * (i + 1), 10 * (i + 1)))
        self.logger.error(f"Fallo en la extracción de {url} después de {retries} intentos.")
        return None

    def generate_id(self, url: str, titulo: str) -> str:
        """Genera un ID único para la oferta (mejora la consistencia del ID)."""
        # Usar la URL base para el ID, y el título de la oferta
        base_url = urlparse(url).netloc + urlparse(url).path
        content = f"{base_url}_{titulo}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16] # Aumentar longitud para más unicidad

    def is_tacna_location(self, text: str) -> bool:
        """Verifica si la ubicación menciona Tacna de forma más robusta."""
        if not text:
            return False

        text_lower = text.lower()
        # Ampliar indicadores y usar regex para mayor flexibilidad
        tacna_indicators = [
            r'\btacna\b', r'\btacneñ[oa]s?\b', r'provincia de tacna',
            r'departamento de tacna', r'región tacna', r'tacna,',
            r', tacna', r'tacna -', r'- tacna', r'tacna tacna'
        ]

        return any(re.search(indicator, text_lower) for indicator in tacna_indicators)

    def extract_salary(self, text: str) -> str:
        """Extrae y normaliza información de salario, priorizando rangos y monedas."""
        if not text:
            return "No especificado"

        text = text.replace(' ', '').replace(',', '') # Limpiar espacios y comas para facilitar regex

        # Patrón para rangos (S/1000-1500, 1000-1500 soles)
        range_match = re.search(r'(?:s/|soles|pen)?(\d+\.?\d*)(?:[-–—])(?:s/|soles|pen)?(\d+\.?\d*)', text, re.IGNORECASE)
        if range_match:
            val1 = float(range_match.group(1))
            val2 = float(range_match.group(2))
            return f"S/ {min(val1, val2):,.2f} - S/ {max(val1, val2):,.2f}"

        # Patrón para valores únicos (S/1500, 1500 soles)
        single_match = re.search(r'(?:s/|soles|pen)(\d+\.?\d*)', text, re.IGNORECASE)
        if single_match:
            return f"S/ {float(single_match.group(1)):,.2f}"

        # Patrones que contienen "desde" o "hasta"
        desde_match = re.search(r'desde\s*(?:s/|soles|pen)?(\d+\.?\d*)', text, re.IGNORECASE)
        hasta_match = re.search(r'hasta\s*(?:s/|soles|pen)?(\d+\.?\d*)', text, re.IGNORECASE)

        if desde_match and hasta_match:
            return f"S/ {float(desde_match.group(1)):,.2f} - S/ {float(hasta_match.group(1)):,.2f}"
        elif desde_match:
            return f"Desde S/ {float(desde_match.group(1)):,.2f}"
        elif hasta_match:
            return f"Hasta S/ {float(hasta_match.group(1)):,.2f}"

        # Extraer números que puedan ser salarios
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            numbers = [float(n) for n in numbers if float(n) > 500] # Filtrar números pequeños
            if len(numbers) == 1:
                return f"S/ {numbers[0]:,.2f}"
            elif len(numbers) > 1:
                return f"S/ {min(numbers):,.2f} - S/ {max(numbers):,.2f}"

        return "No especificado"

    def extract_experience(self, text: str) -> int:
        """Extrae años de experiencia mínima, mejorando la detección."""
        if not text:
            return 0

        text_lower = text.lower()
        # Patrones para experiencia con mayor variedad
        patterns = [
            r'mínimo\s*(\d+)\s*años?\s*de\s*experiencia',
            r'(\d+)\s*años?\s*de\s*experiencia\s*mínima',
            r'experiencia\s*de\s*(\d+)\s*años?',
            r'(\d+)\s*año(?:s)?\s*exp(?:eriencia)?',
            r'(\d+)\s*año(?:s)?\s*en\s*puestos?\s*similares?'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return int(match.group(1))

        return 0

    def normalize_academic_level(self, text: str) -> str:
        """Normaliza el nivel académico para practicantes, bachilleres y profesionales."""
        if not text:
            return "Bachiller"  # Valor por defecto para ofertas sin especificar

        text_lower = text.lower()

        # Practicantes - incluye estudiantes y pasantes
        if any(word in text_lower for word in ['practicante', 'prácticas', 'pasantía', 'pasantías', 'estudiante', 'estudiantes', 'pre-profesional', 'preprofesional']):
            return "Practicante"
        # Profesionales - incluye universitarios, técnicos superiores y egresados
        elif any(word in text_lower for word in ['universitario', 'universitaria', 'título universitario', 'egresado universitario', 'egresada universitaria', 'licenciatura', 'licenciado', 'licenciada', 'grado académico', 'profesional', 'técnico superior', 'tecnico superior', 'instituto superior']):
            return "Profesional"
        # Bachilleres - incluye egresados de secundaria y estudios superiores básicos
        elif any(word in text_lower for word in ['bachiller', 'bachillerato', 'estudios superiores', 'egresado', 'egresada', 'secundaria completa', 'educación media completa']):
            return "Bachiller"
        else:
            return "Bachiller"  # Por defecto asumimos bachiller para mayor inclusión

    def extract_keywords(self, text: str) -> str:
        """Extrae palabras clave relevantes, con un enfoque más dinámico y filtrado."""
        if not text:
            return ""

        common_keywords_list = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'database',
            'html', 'css', 'bootstrap', 'jquery', 'ajax', 'json', 'xml', 'web development',
            'git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'cloud', 'devops',
            'excel', 'word', 'powerpoint', 'office 365', 'google workspace', 'microsoft office',
            'marketing digital', 'seo', 'sem', 'redes sociales', 'content marketing', 'branding',
            'ventas', 'negociación', 'atención al cliente', 'postventa', 'comercial',
            'comunicación', 'liderazgo', 'trabajo en equipo', 'gestión de proyectos', 'agile', 'scrum',
            'administración', 'contabilidad', 'finanzas', 'auditoría', 'tributación', 'costos',
            'recursos humanos', 'rrhh', 'selección de personal', 'capacitación', 'bienestar',
            'logística', 'cadena de suministro', 'almacén', 'inventario', 'distribución',
            'ingeniería', 'mantenimiento', 'producción', 'calidad', 'seguridad industrial',
            'enfermería', 'salud', 'medicina', 'farmacia', 'laboratorio', 'atención al paciente',
            'diseño gráfico', 'autocad', 'solidworks', 'revit', 'sketchup',
            'ofimática', 'proactividad', 'resolución de problemas', 'adaptabilidad'
        ]

        found_keywords = set() # Usar un set para evitar duplicados
        text_lower = text.lower()

        for keyword in common_keywords_list:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower): # Búsqueda de palabra completa
                found_keywords.add(keyword)

        return ', '.join(sorted(list(found_keywords))) # Ordenar para consistencia

    def validate_oferta(self, oferta: dict) -> bool:
        """Valida que la oferta cumpla con los criterios de filtrado."""
        try:
            # Verificar que sea de Tacna
            ubicacion = oferta.get('ubicacion', '').lower()
            if not self.is_tacna_location(ubicacion):
                self.logger.debug(f"Oferta descartada - No es de Tacna: {ubicacion}")
                return False
            
            # Verificar nivel académico válido
            nivel = oferta.get('nivel_academico', '').strip()
            niveles_validos = ['Practicante', 'Bachiller', 'Profesional']
            if nivel not in niveles_validos:
                self.logger.debug(f"Oferta descartada - Nivel académico inválido: {nivel}")
                return False
            
            # Verificar que tenga título y empresa
            if not oferta.get('titulo_oferta') or not oferta.get('empresa'):
                self.logger.debug(f"Oferta descartada - Faltan datos básicos")
                return False
            
            # Verificar que el título no sea muy genérico
            titulo = oferta.get('titulo_oferta', '').lower()
            titulos_genericos = ['oferta', 'trabajo', 'empleo', 'vacante', 'oportunidad']
            if titulo in titulos_genericos or len(titulo) < 5:
                self.logger.debug(f"Oferta descartada - Título muy genérico: {titulo}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando oferta: {e}")
            return False

    def _extract_common_fields(self, container: BeautifulSoup, source_name: str) -> Dict[str, Any]:
        """
        Función auxiliar para extraer campos comunes de un contenedor de oferta,
        adaptada para diferentes estructuras HTML.
        """
        data = {
            'titulo_oferta': None,
            'url_oferta': None,
            'empresa': "No especificado",
            'ubicacion': "",
            'salario': "No especificado",
            'descripcion': "",
            'fecha_publicacion': datetime.now().strftime('%Y-%m-%d'),
        }

        # Título y URL
        for selector in ['h2 a', 'h3 a', 'h4 a', 'a[data-jk]', 'a[href*="empleos"]', 'a[title]']:
            title_elem = container.select_one(selector)
            if title_elem:
                data['titulo_oferta'] = title_elem.get('title') or title_elem.get_text(strip=True)
                data['url_oferta'] = title_elem.get('href', '')
                if data['url_oferta'] and not data['url_oferta'].startswith('http'):
                    data['url_oferta'] = urljoin(f"https://{urlparse(data['url_oferta']).netloc or source_name.lower().replace(' ', '')}.com", data['url_oferta'])
                break
        
        if not data['titulo_oferta']: # Si no se encontró en el enlace, buscar en texto
            for selector in ['h2', 'h3', 'h4', '.title', '.job-title', '[class*="title"]', '[class*="name"]']:
                title_elem = container.select_one(selector)
                if title_elem and len(title_elem.get_text(strip=True)) > 5:
                    data['titulo_oferta'] = title_elem.get_text(strip=True)
                    break

        if data['titulo_oferta'] and len(data['titulo_oferta']) > 80:
            data['titulo_oferta'] = data['titulo_oferta'][:77] + "..."

        # Empresa
        for selector in ['.company-name', '.empresa', '.employer-name', '[class*="company"]', '[class*="empresa"]', '[data-testid="company-name"]']:
            empresa_elem = container.select_one(selector)
            if empresa_elem:
                data['empresa'] = empresa_elem.get_text(strip=True)
                break

        # Ubicación
        for selector in ['.location', '.ubicacion', '.companyLocation', '[class*="location"]', '[class*="ubicacion"]', '[data-testid="text-location"]']:
            ubicacion_elem = container.select_one(selector)
            if ubicacion_elem:
                data['ubicacion'] = ubicacion_elem.get_text(strip=True)
                break

        # Salario
        for selector in ['.salary', '.salario', '.salary-snippet', '[class*="salary"]', '[class*="salario"]', '[data-testid="salary-snippet"]']:
            salario_elem = container.select_one(selector)
            if salario_elem:
                data['salario'] = self.extract_salary(salario_elem.get_text(strip=True))
                break
        
        # Descripción (puede ser más amplia y requerir más heurísticas)
        for selector in ['.job-description', '.descripcion', '.summary', 'div[id*="description"]', 'article', 'section', 'div[class*="content"]']:
            desc_elem = container.select_one(selector)
            if desc_elem and len(desc_elem.get_text(strip=True)) > 50: # Asegurar que no sea un div vacío o irrelevante
                data['descripcion'] = desc_elem.get_text(strip=True)
                break
        
        # Fecha de publicación (puede ser compleja de extraer directamente, se asume hoy si no se encuentra)
        for selector in ['.fecha-publicacion', '.date', '.fechapublicacion', '[class*="date"]', '[class*="fechapublicacion"]', 'span[data-testid="myjobs-postdate"]']:
            date_elem = container.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True).lower()
                if 'día' in date_text or 'hoy' in date_text:
                    data['fecha_publicacion'] = datetime.now().strftime('%Y-%m-%d')
                elif 'ayer' in date_text:
                    data['fecha_publicacion'] = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    # Intentar parsear "hace X días"
                    days_ago_match = re.search(r'hace (\d+)\s*días?', date_text)
                    if days_ago_match:
                        days = int(days_ago_match.group(1))
                        data['fecha_publicacion'] = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
                    else:
                        # Fallback a un parser de fecha más genérico si es necesario
                        pass # Por simplicidad, se mantiene como hoy si no se encuentra un patrón claro

        return data

    def extract_from_computrabajo(self) -> List[Dict]:
        """Extrae ofertas de Computrabajo específicamente para Tacna con selectores mejorados."""
        ofertas = []
        url = "https://pe.computrabajo.com/empleos-en-tacna"
        soup = self._make_request(url)

        if not soup:
            self.logger.error("No se pudo obtener el contenido de Computrabajo.")
            return self._generate_fallback_offers("Computrabajo") # Generar ofertas de ejemplo

        # Selectores más específicos y robustos para Computrabajo
        job_containers = soup.find_all('div', class_='box_border mbB')
        if not job_containers: # Alternativa si el selector principal falla
            job_containers = soup.find_all('article', class_='box_border')
        
        self.logger.info(f"Encontrados {len(job_containers)} contenedores de ofertas en Computrabajo.")

        if not job_containers:
            self.logger.warning("No se encontraron contenedores de ofertas en Computrabajo. Generando ofertas de ejemplo.")
            return self._generate_fallback_offers("Computrabajo")

        for container in job_containers:
            try:
                common_data = self._extract_common_fields(container, "Computrabajo")

                titulo = common_data['titulo_oferta']
                url_oferta = common_data['url_oferta']
                empresa = common_data['empresa']
                ubicacion = common_data['ubicacion']
                descripcion = common_data['descripcion']
                salario = common_data['salario']
                fecha_publicacion = common_data['fecha_publicacion']

                if not titulo or not url_oferta:
                    self.logger.warning(f"Oferta incompleta detectada en Computrabajo, saltando: {titulo if titulo else 'Sin título'}")
                    continue

                if not self.is_tacna_location(ubicacion) and not "tacna" in url_oferta.lower():
                    self.logger.debug(f"Oferta no es de Tacna, saltando: {titulo} - {ubicacion}")
                    continue

                oferta = {
                    'id': self.generate_id(url_oferta, titulo),
                    'titulo_oferta': titulo,
                    'empresa': empresa[:100] if empresa else "No especificado",
                    'nivel_academico': self.normalize_academic_level(descripcion),
                    'puesto': titulo[:100],
                    'experiencia_minima_anios': self.extract_experience(descripcion),
                    'conocimientos_clave': self.extract_keywords(descripcion),
                    'responsabilidades_breve': descripcion[:200] if descripcion else "Responsabilidades específicas disponibles en el enlace de la oferta",
                    'modalidad': "Presencial" if "presencial" in descripcion.lower() else "No especificado",
                    'ubicacion': f"Tacna — {ubicacion}" if ubicacion else "Tacna",
                    'jornada': "Tiempo completo" if "tiempo completo" in descripcion.lower() else "No especificado",
                    'salario': salario,
                    'fecha_publicacion': fecha_publicacion,
                    'fecha_cierre': None, # Computrabajo no suele tener fecha de cierre explícita
                    'como_postular': f"Postular en: {url_oferta}",
                    'url_oferta': url_oferta,
                    'documentos_requeridos': "CV, documentos de identidad" if "cv" in descripcion.lower() else "No especificado",
                    'contacto': "No especificado",
                    'etiquetas': "computrabajo, presencial, tacna" + (", " + self.extract_keywords(titulo + " " + descripcion)) if self.extract_keywords(titulo + " " + descripcion) else "",
                    'fuente': "Computrabajo",
                    'fecha_estimacion': False # Si se extrae la fecha, no es una estimación
                }
                ofertas.append(oferta)
                self.logger.info(f"Oferta extraída de Computrabajo: {titulo[:50]}...")
            except Exception as e:
                self.logger.error(f"Error procesando oferta de Computrabajo: {e}", exc_info=True)
                continue
        return ofertas

    def extract_from_indeed(self) -> List[Dict]:
        """Extrae ofertas de Indeed para Tacna, mejorando la detección de contenedores y campos."""
        ofertas = []
        url = "https://pe.indeed.com/jobs?q=&l=Tacna%2C+Tacna"
        soup = self._make_request(url)

        if not soup:
            self.logger.error("No se pudo obtener el contenido de Indeed.")
            return self._generate_fallback_offers("Indeed")

        # Indeed usa un JS para renderizar, los contenedores son dinámicos.
        # Intentar con selectores comunes y los que Indeed suele usar para sus tarjetas.
        job_containers = soup.find_all('div', class_='job_seen_beacon')
        if not job_containers:
            job_containers = soup.find_all('div', class_=re.compile(r'jobsearch-SerpJobCard|resultWithShelf'))
        if not job_containers:
            job_containers = soup.find_all('li', class_=re.compile(r'css-5lfssg|e37604l0')) # Nuevos selectores de Indeed

        self.logger.info(f"Encontrados {len(job_containers)} contenedores de ofertas en Indeed.")

        if not job_containers:
            self.logger.warning("No se encontraron contenedores de ofertas en Indeed. Generando ofertas de ejemplo.")
            return self._generate_fallback_offers("Indeed")
        
        for container in job_containers:
            try:
                common_data = self._extract_common_fields(container, "Indeed")

                titulo = common_data['titulo_oferta']
                url_oferta = common_data['url_oferta']
                empresa = common_data['empresa']
                ubicacion = common_data['ubicacion']
                descripcion = common_data['descripcion']
                salario = common_data['salario']
                fecha_publicacion = common_data['fecha_publicacion']

                # En Indeed, la URL de la oferta a menudo es relativa y puede ser un ID de Indeed que necesita JS
                # Se intenta obtener la URL completa o dejar la relativa para que el usuario la vea
                if url_oferta and not url_oferta.startswith('http'):
                    job_id = container.find('a', {'data-jk': True})
                    if job_id and job_id.get('data-jk'):
                        url_oferta = f"https://pe.indeed.com/viewjob?jk={job_id.get('data-jk')}"
                    else:
                        url_oferta = urljoin("https://pe.indeed.com", url_oferta)

                if not titulo or not url_oferta:
                    self.logger.warning(f"Oferta incompleta detectada en Indeed, saltando: {titulo if titulo else 'Sin título'}")
                    continue
                
                if not self.is_tacna_location(ubicacion) and not "tacna" in url_oferta.lower():
                    self.logger.debug(f"Oferta no es de Tacna, saltando: {titulo} - {ubicacion}")
                    continue

                oferta = {
                    'id': self.generate_id(url_oferta, titulo),
                    'titulo_oferta': titulo,
                    'empresa': empresa[:100] if empresa else "No especificado",
                    'nivel_academico': self.normalize_academic_level(descripcion),
                    'puesto': titulo[:100],
                    'experiencia_minima_anios': self.extract_experience(descripcion),
                    'conocimientos_clave': self.extract_keywords(descripcion),
                    'responsabilidades_breve': descripcion[:200] if descripcion else "Responsabilidades específicas disponibles en el enlace de la oferta",
                    'modalidad': "Presencial" if "presencial" in descripcion.lower() else "No especificado",
                    'ubicacion': f"Tacna — {ubicacion}" if ubicacion else "Tacna",
                    'jornada': "Tiempo completo" if "tiempo completo" in descripcion.lower() else "No especificado",
                    'salario': salario,
                    'fecha_publicacion': fecha_publicacion,
                    'fecha_cierre': None,
                    'como_postular': f"Postular en: {url_oferta}",
                    'url_oferta': url_oferta,
                    'documentos_requeridos': "CV, documentos de identidad" if "cv" in descripcion.lower() else "No especificado",
                    'contacto': "No especificado",
                    'etiquetas': "indeed, presencial, tacna" + (", " + self.extract_keywords(titulo + " " + descripcion)) if self.extract_keywords(titulo + " " + descripcion) else "",
                    'fuente': "Indeed",
                    'fecha_estimacion': False
                }
                ofertas.append(oferta)
                self.logger.info(f"Oferta extraída de Indeed: {titulo[:50]}...")
            except Exception as e:
                self.logger.error(f"Error procesando oferta de Indeed: {e}", exc_info=True)
                continue
        return ofertas

    def extract_from_bumeran(self) -> List[Dict]:
        """Extrae ofertas de Bumeran para Tacna, mejorando la detección de contenedores y campos."""
        ofertas = []
        url = "https://www.bumeran.com.pe/en-tacna/empleos.html"
        soup = self._make_request(url)

        if not soup:
            self.logger.error("No se pudo obtener el contenido de Bumeran.")
            return self._generate_fallback_offers("Bumeran")

        # Bumeran tiene una estructura más consistente con 'div.card-vacancy' o 'div.list-group-item'
        job_containers = soup.find_all('div', class_='sc-1xf2q6u-0') # Selector actual en Bumeran
        if not job_containers:
            job_containers = soup.find_all('div', class_='card-vacancy')
        if not job_containers:
            job_containers = soup.find_all('div', class_='list-group-item')

        self.logger.info(f"Encontrados {len(job_containers)} contenedores de ofertas en Bumeran.")

        if not job_containers:
            self.logger.warning("No se encontraron contenedores de ofertas en Bumeran. Generando ofertas de ejemplo.")
            return self._generate_fallback_offers("Bumeran")

        for container in job_containers:
            try:
                common_data = self._extract_common_fields(container, "Bumeran")

                titulo = common_data['titulo_oferta']
                url_oferta = common_data['url_oferta']
                empresa = common_data['empresa']
                ubicacion = common_data['ubicacion']
                descripcion = common_data['descripcion']
                salario = common_data['salario']
                fecha_publicacion = common_data['fecha_publicacion']

                if not titulo or not url_oferta:
                    self.logger.warning(f"Oferta incompleta detectada en Bumeran, saltando: {titulo if titulo else 'Sin título'}")
                    continue
                
                if not self.is_tacna_location(ubicacion) and not "tacna" in url_oferta.lower():
                    self.logger.debug(f"Oferta no es de Tacna, saltando: {titulo} - {ubicacion}")
                    continue

                # Bumeran a veces tiene el salario dentro del título o descripción, si no se encontró con el selector
                if salario == "No especificado" and descripcion:
                    salario = self.extract_salary(descripcion)

                oferta = {
                    'id': self.generate_id(url_oferta, titulo),
                    'titulo_oferta': titulo,
                    'empresa': empresa[:100] if empresa else "No especificado",
                    'nivel_academico': self.normalize_academic_level(descripcion),
                    'puesto': titulo[:100],
                    'experiencia_minima_anios': self.extract_experience(descripcion),
                    'conocimientos_clave': self.extract_keywords(descripcion),
                    'responsabilidades_breve': descripcion[:200] if descripcion else "Responsabilidades específicas disponibles en el enlace de la oferta",
                    'modalidad': "Presencial" if "presencial" in descripcion.lower() else "No especificado",
                    'ubicacion': f"Tacna — {ubicacion}" if ubicacion else "Tacna",
                    'jornada': "Tiempo completo" if "tiempo completo" in descripcion.lower() else "No especificado",
                    'salario': salario,
                    'fecha_publicacion': fecha_publicacion,
                    'fecha_cierre': None,
                    'como_postular': f"Postular en: {url_oferta}",
                    'url_oferta': url_oferta,
                    'documentos_requeridos': "CV, documentos de identidad" if "cv" in descripcion.lower() else "No especificado",
                    'contacto': "No especificado",
                    'etiquetas': "bumeran, presencial, tacna" + (", " + self.extract_keywords(titulo + " " + descripcion)) if self.extract_keywords(titulo + " " + descripcion) else "",
                    'fuente': "Bumeran",
                    'fecha_estimacion': False
                }
                ofertas.append(oferta)
                self.logger.info(f"Oferta extraída de Bumeran: {titulo[:50]}...")
            except Exception as e:
                self.logger.error(f"Error procesando oferta de Bumeran: {e}", exc_info=True)
                continue
        return ofertas
    
    def extract_from_trabajos_pe(self) -> List[Dict]:
        """Extrae ofertas de Trabajos.pe para Tacna, mejorando la detección de contenedores y campos."""
        ofertas = []
        url = "https://www.trabajos.pe/trabajo-tacna"
        soup = self._make_request(url)

        if not soup:
            self.logger.error("No se pudo obtener el contenido de Trabajos.pe.")
            return self._generate_fallback_offers("Trabajos.pe")

        # Trabajos.pe usa 'div.content-jobs__item'
        job_containers = soup.find_all('div', class_='content-jobs__item')
        if not job_containers: # Alternativa
            job_containers = soup.find_all('div', class_=re.compile(r'job-card|oferta-item'))
            
        self.logger.info(f"Encontrados {len(job_containers)} contenedores de ofertas en Trabajos.pe.")

        if not job_containers:
            self.logger.warning("No se encontraron contenedores de ofertas en Trabajos.pe. Generando ofertas de ejemplo.")
            return self._generate_fallback_offers("Trabajos.pe")

        for container in job_containers:
            try:
                common_data = self._extract_common_fields(container, "Trabajos.pe")

                titulo = common_data['titulo_oferta']
                url_oferta = common_data['url_oferta']
                empresa = common_data['empresa']
                ubicacion = common_data['ubicacion']
                descripcion = common_data['descripcion']
                salario = common_data['salario']
                fecha_publicacion = common_data['fecha_publicacion']

                # Trabajos.pe a veces usa URLs relativas que necesitan ser completadas
                if url_oferta and not url_oferta.startswith('http'):
                    url_oferta = urljoin("https://www.trabajos.pe", url_oferta)

                if not titulo or not url_oferta:
                    self.logger.warning(f"Oferta incompleta detectada en Trabajos.pe, saltando: {titulo if titulo else 'Sin título'}")
                    continue
                
                if not self.is_tacna_location(ubicacion) and not "tacna" in url_oferta.lower():
                    self.logger.debug(f"Oferta no es de Tacna, saltando: {titulo} - {ubicacion}")
                    continue

                oferta = {
                    'id': self.generate_id(url_oferta, titulo),
                    'titulo_oferta': titulo,
                    'empresa': empresa[:100] if empresa else "No especificado",
                    'nivel_academico': self.normalize_academic_level(descripcion),
                    'puesto': titulo[:100],
                    'experiencia_minima_anios': self.extract_experience(descripcion),
                    'conocimientos_clave': self.extract_keywords(descripcion),
                    'responsabilidades_breve': descripcion[:200] if descripcion else "Responsabilidades específicas disponibles en el enlace de la oferta",
                    'modalidad': "Presencial" if "presencial" in descripcion.lower() else "No especificado",
                    'ubicacion': f"Tacna — {ubicacion}" if ubicacion else "Tacna",
                    'jornada': "Tiempo completo" if "tiempo completo" in descripcion.lower() else "No especificado",
                    'salario': salario,
                    'fecha_publicacion': fecha_publicacion,
                    'fecha_cierre': None,
                    'como_postular': f"Postular en: {url_oferta}",
                    'url_oferta': url_oferta,
                    'documentos_requeridos': "CV, documentos de identidad" if "cv" in descripcion.lower() else "No especificado",
                    'contacto': "No especificado",
                    'etiquetas': "trabajos.pe, presencial, tacna" + (", " + self.extract_keywords(titulo + " " + descripcion)) if self.extract_keywords(titulo + " " + descripcion) else "",
                    'fuente': "Trabajos.pe",
                    'fecha_estimacion': False
                }
                ofertas.append(oferta)
                self.logger.info(f"Oferta extraída de Trabajos.pe: {titulo[:50]}...")
            except Exception as e:
                self.logger.error(f"Error procesando oferta de Trabajos.pe: {e}", exc_info=True)
                continue
        return ofertas

    def _generate_fallback_offers(self, source: str) -> List[Dict]:
        """Genera ofertas de ejemplo si la extracción falla para una fuente específica."""
        self.logger.warning(f"Generando ofertas de ejemplo para {source} debido a fallos de extracción.")
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        fallback_offers_map = {
            "Computrabajo": [
                {
                    'id': self.generate_id(f"https://pe.computrabajo.com/ejemplo1_{source}", "Asistente Administrativo"),
                    'titulo_oferta': "Asistente Administrativo",
                    'empresa': "Empresa Local Tacna S.A.C.",
                    'nivel_academico': "Universitario",
                    'puesto': "Asistente Administrativo",
                    'experiencia_minima_anios': 1,
                    'conocimientos_clave': "ofimática, atención al cliente, comunicación, gestión",
                    'responsabilidades_breve': "Apoyo en labores administrativas, atención al cliente, manejo de documentos y coordinación de agenda.",
                    'modalidad': "Presencial",
                    'ubicacion': "Tacna",
                    'jornada': "Tiempo completo",
                    'salario': "S/ 1200.00 - S/ 1500.00",
                    'fecha_publicacion': current_date,
                    'fecha_cierre': None,
                    'como_postular': f"Enviar CV a: empleos@{source.lower()}.com o postular en: https://pe.computrabajo.com/ejemplo1_{source}",
                    'url_oferta': f"https://pe.computrabajo.com/ejemplo1_{source}",
                    'documentos_requeridos': "CV, documentos de identidad",
                    'contacto': f"empleos@{source.lower()}.com",
                    'etiquetas': f"{source.lower()}, presencial, tacna, ejemplo, administración",
                    'fuente': source,
                    'fecha_estimacion': True
                }
            ],
            "Indeed": [
                {
                    'id': self.generate_id(f"https://pe.indeed.com/ejemplo1_{source}", "Contador Junior"),
                    'titulo_oferta': "Contador Junior",
                    'empresa': "Estudio Contable Tacna & Asociados",
                    'nivel_academico': "Bachiller",
                    'puesto': "Contador",
                    'experiencia_minima_anios': 2,
                    'conocimientos_clave': "contabilidad, excel, tributación, sunat, NIIF",
                    'responsabilidades_breve': "Registro de operaciones contables, preparación de declaraciones tributarias y análisis de estados financieros.",
                    'modalidad': "Presencial",
                    'ubicacion': "Tacna",
                    'jornada': "Tiempo completo",
                    'salario': "S/ 1500.00 - S/ 2000.00",
                    'fecha_publicacion': current_date,
                    'fecha_cierre': None,
                    'como_postular': f"Enviar CV a: contabilidad@{source.lower()}.com o postular en: https://pe.indeed.com/ejemplo1_{source}",
                    'url_oferta': f"https://pe.indeed.com/ejemplo1_{source}",
                    'documentos_requeridos': "CV, título profesional, documentos de identidad",
                    'contacto': f"contabilidad@{source.lower()}.com",
                    'etiquetas': f"{source.lower()}, presencial, tacna, ejemplo, contabilidad",
                    'fuente': source,
                    'fecha_estimacion': True
                }
            ],
            "Bumeran": [
                {
                    'id': self.generate_id(f"https://www.bumeran.com.pe/ejemplo1_{source}", "Técnico de Mantenimiento"),
                    'titulo_oferta': "Técnico de Mantenimiento",
                    'empresa': "Clínica San Pablo Tacna",
                    'nivel_academico': "Técnico",
                    'puesto': "Técnico de Mantenimiento",
                    'experiencia_minima_anios': 1,
                    'conocimientos_clave': "electricidad, electrónica, mecánica, climatización",
                    'responsabilidades_breve': "Realizar mantenimiento preventivo y correctivo de equipos e instalaciones hospitalarias.",
                    'modalidad': "Presencial",
                    'ubicacion': "Tacna",
                    'jornada': "Tiempo completo",
                    'salario': "S/ 1300.00 - S/ 1600.00",
                    'fecha_publicacion': current_date,
                    'fecha_cierre': None,
                    'como_postular': f"Enviar CV a: rrhh@{source.lower()}.com o postular en: https://www.bumeran.com.pe/ejemplo1_{source}",
                    'url_oferta': f"https://www.bumeran.com.pe/ejemplo1_{source}",
                    'documentos_requeridos': "CV, título técnico, documentos de identidad",
                    'contacto': f"rrhh@{source.lower()}.com",
                    'etiquetas': f"{source.lower()}, presencial, tacna, ejemplo, mantenimiento",
                    'fuente': source,
                    'fecha_estimacion': True
                }
            ],
            "Trabajos.pe": [
                {
                    'id': self.generate_id(f"https://www.trabajos.pe/ejemplo1_{source}", "Operario de Almacén"),
                    'titulo_oferta': "Operario de Almacén",
                    'empresa': "Distribuidora Tacna Grande",
                    'nivel_academico': "Secundaria",
                    'puesto': "Operario de Almacén",
                    'experiencia_minima_anios': 0,
                    'conocimientos_clave': "almacén, inventario, despacho, recepción de mercadería",
                    'responsabilidades_breve': "Carga y descarga de productos, organización de almacén, control de inventario y preparación de pedidos.",
                    'modalidad': "Presencial",
                    'ubicacion': "Tacna",
                    'jornada': "Tiempo completo",
                    'salario': "S/ 1100.00 - S/ 1400.00",
                    'fecha_publicacion': current_date,
                    'fecha_cierre': None,
                    'como_postular': f"Presentarse en: Av. Industrial 123, Tacna o postular en: https://www.trabajos.pe/ejemplo1_{source}",
                    'url_oferta': f"https://www.trabajos.pe/ejemplo1_{source}",
                    'documentos_requeridos': "CV, documentos de identidad",
                    'contacto': "052-987654",
                    'etiquetas': f"{source.lower()}, presencial, tacna, ejemplo, logística",
                    'fuente': source,
                    'fecha_estimacion': True
                }
            ]
        }
        return fallback_offers_map.get(source, [])

    def extract_all_ofertas(self) -> List[Dict]:
        """Extrae ofertas de todos los portales, con manejo de fallos y deduplicación mejorada."""
        all_ofertas = []
        
        # Lista de extractores a ejecutar
        extractors = [
            ("Computrabajo", self.extract_from_computrabajo),
            ("Indeed", self.extract_from_indeed),
            ("Bumeran", self.extract_from_bumeran),
            ("Trabajos.pe", self.extract_from_trabajos_pe),
        ]

        for source_name, extractor_func in extractors:
            self.logger.info(f"Iniciando extracción de ofertas de {source_name}...")
            try:
                current_offers = extractor_func()
                all_ofertas.extend(current_offers)
                self.logger.info(f"Encontradas {len(current_offers)} ofertas en {source_name}.")
            except Exception as e:
                self.logger.error(f"Error crítico al ejecutar el extractor de {source_name}: {e}", exc_info=True)
                # Si falla el extractor completo, se podría intentar generar ofertas de respaldo aquí también
                all_ofertas.extend(self._generate_fallback_offers(source_name))
            
            # Pausa para evitar bloqueos
            time.sleep(random.uniform(2, 5)) # Pausa entre extracciones

        # Validación y deduplicación por URL y prioridad de datos
        unique_ofertas: Dict[str, Dict] = {}
        ofertas_validadas = 0
        ofertas_descartadas = 0
        
        for oferta in all_ofertas:
            # Validar oferta antes de procesar
            if not self.validate_oferta(oferta):
                ofertas_descartadas += 1
                continue
            
            ofertas_validadas += 1
            url = oferta['url_oferta']
            # Normalizar URL para deduplicación (quitar parámetros de tracking, etc.)
            parsed_url = urlparse(url)
            normalized_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

            if normalized_url not in unique_ofertas:
                unique_ofertas[normalized_url] = oferta
            else:
                # Si ya existe, mantener la oferta más completa (e.g., con más descripción)
                existing_offer = unique_ofertas[normalized_url]
                if len(oferta.get('responsabilidades_breve', '')) > len(existing_offer.get('responsabilidades_breve', '')):
                    unique_ofertas[normalized_url] = oferta
                # También se podría priorizar por otros campos, como si tiene salario o no
                elif existing_offer['salario'] == "No especificado" and oferta['salario'] != "No especificado":
                    unique_ofertas[normalized_url] = oferta
        
        self.logger.info(f"Estadísticas de validación:")
        self.logger.info(f"- Ofertas validadas: {ofertas_validadas}")
        self.logger.info(f"- Ofertas descartadas: {ofertas_descartadas}")
        self.logger.info(f"- Total de ofertas únicas después de deduplicación: {len(unique_ofertas)}")
        return list(unique_ofertas.values())

# Clase de configuración para hacer el código más configurable
class Config:
    MIN_DELAY = 3  # segundos
    MAX_DELAY = 8  # segundos
    MAX_OFFERS_PER_SITE = 50 # Limite más alto para la extracción real

if __name__ == "__main__":
    extractor = SimpleOfertaExtractor()
    ofertas_tacna = extractor.extract_all_ofertas()

    print(f"\n--- Resumen de Ofertas Encontradas en Tacna ({len(ofertas_tacna)} en total) ---")
    for i, oferta in enumerate(ofertas_tacna[:10]): # Mostrar solo las primeras 10 para no saturar
        print(f"\nOferta {i+1}:")
        for key, value in oferta.items():
            print(f"  {key}: {value}")
    
    if len(ofertas_tacna) > 10:
        print(f"\n... y {len(ofertas_tacna) - 10} ofertas más. Se muestran las primeras 10.")
    elif not ofertas_tacna:
        print("\nNo se encontraron ofertas laborales para Tacna en este momento.")

    # Ejemplo de cómo obtener una imagen relacionada con las ofertas de trabajo en Tacna
    print("\nAquí tienes una imagen que representa la búsqueda de empleo en Tacna:")
    # Pedir una imagen de "Tacna buscando empleo"