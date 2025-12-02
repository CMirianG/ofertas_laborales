// JavaScript principal para el sistema de ofertas laborales

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Animación de entrada para las cards
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(function() {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var iconClass = type === 'success' ? 'fa-check-circle' : 
                   type === 'error' ? 'fa-exclamation-circle' : 
                   type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    
    var notification = document.createElement('div');
    notification.className = 'alert ' + alertClass + ' alert-dismissible fade show position-fixed';
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas ${iconClass} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove después de 5 segundos
    setTimeout(function() {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Función para confirmar acciones
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Función para formatear fechas
function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// Función para formatear números
function formatNumber(number) {
    return new Intl.NumberFormat('es-ES').format(number);
}

// Función para copiar al portapapeles
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copiado al portapapeles', 'success');
    }).catch(function() {
        showNotification('Error al copiar', 'error');
    });
}

// Función para compartir oferta
function shareOffer(title, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).catch(function(error) {
            console.log('Error sharing:', error);
        });
    } else {
        copyToClipboard(url);
    }
}

// Función para filtrar tabla
function filterTable(inputId, tableId) {
    var input = document.getElementById(inputId);
    var table = document.getElementById(tableId);
    var filter = input.value.toLowerCase();
    var rows = table.getElementsByTagName('tr');
    
    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        var cells = row.getElementsByTagName('td');
        var found = false;
        
        for (var j = 0; j < cells.length; j++) {
            var cell = cells[j];
            if (cell.innerHTML.toLowerCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        row.style.display = found ? '' : 'none';
    }
}

// Función para ordenar tabla
function sortTable(tableId, columnIndex) {
    var table = document.getElementById(tableId);
    var rows = Array.from(table.getElementsByTagName('tr'));
    var header = rows[0];
    var dataRows = rows.slice(1);
    
    dataRows.sort(function(a, b) {
        var aText = a.getElementsByTagName('td')[columnIndex].textContent;
        var bText = b.getElementsByTagName('td')[columnIndex].textContent;
        
        // Intentar comparar como números
        var aNum = parseFloat(aText);
        var bNum = parseFloat(bText);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // Comparar como texto
        return aText.localeCompare(bText);
    });
    
    // Reconstruir tabla
    table.innerHTML = '';
    table.appendChild(header);
    dataRows.forEach(function(row) {
        table.appendChild(row);
    });
}

// Función para exportar datos
function exportToCSV(tableId, filename) {
    var table = document.getElementById(tableId);
    var rows = table.getElementsByTagName('tr');
    var csv = [];
    
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var cells = row.getElementsByTagName('td');
        var rowData = [];
        
        for (var j = 0; j < cells.length; j++) {
            var cell = cells[j];
            var text = cell.textContent.replace(/"/g, '""');
            rowData.push('"' + text + '"');
        }
        
        csv.push(rowData.join(','));
    }
    
    var csvContent = csv.join('\n');
    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    
    if (link.download !== undefined) {
        var url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Función para imprimir página
function printPage() {
    window.print();
}

// Función para refrescar datos
function refreshData() {
    location.reload();
}

// Función para mostrar/ocultar secciones
function toggleSection(sectionId) {
    var section = document.getElementById(sectionId);
    if (section.style.display === 'none') {
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
    }
}

// Función para validar formularios
function validateForm(formId) {
    var form = document.getElementById(formId);
    var inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    var isValid = true;
    
    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Función para limpiar formularios
function clearForm(formId) {
    var form = document.getElementById(formId);
    form.reset();
    
    var inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(function(input) {
        input.classList.remove('is-valid', 'is-invalid');
    });
}

// Función para mostrar loading
function showLoading(elementId) {
    var element = document.getElementById(elementId);
    if (element) {
        element.classList.add('loading');
        element.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
    }
}

// Función para ocultar loading
function hideLoading(elementId, originalContent) {
    var element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('loading');
        element.innerHTML = originalContent;
    }
}

// Función para hacer peticiones AJAX
function makeRequest(url, options = {}) {
    var defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    var finalOptions = Object.assign(defaultOptions, options);
    
    return fetch(url, finalOptions)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(function(error) {
            console.error('Error:', error);
            showNotification('Error en la petición: ' + error.message, 'error');
            throw error;
        });
}

// Función para debounce
function debounce(func, wait) {
    var timeout;
    return function executedFunction() {
        var later = function() {
            clearTimeout(timeout);
            func();
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Función para throttle
function throttle(func, limit) {
    var inThrottle;
    return function() {
        var args = arguments;
        var context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(function() {
                inThrottle = false;
            }, limit);
        }
    };
}

// Inicializar funcionalidades específicas de la página
function initPageFeatures() {
    // Auto-completar para campos de búsqueda
    var searchInputs = document.querySelectorAll('input[type="search"], input[name="busqueda"]');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', debounce(function() {
            // Implementar búsqueda en tiempo real si es necesario
        }, 300));
    });
    
    // Mejorar accesibilidad de tablas
    var tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        table.setAttribute('role', 'table');
        var headers = table.querySelectorAll('th');
        headers.forEach(function(header, index) {
            header.setAttribute('scope', 'col');
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table.id, index);
            });
        });
    });
}

// Ejecutar inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initPageFeatures);
