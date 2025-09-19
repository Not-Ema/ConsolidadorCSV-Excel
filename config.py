"""
Archivo de configuración para Consolidador Pro.
Contiene configuraciones por defecto y constantes del programa.
"""

import os
from pathlib import Path

# Información del programa
PROGRAM_NAME = "Consolidador Pro"
VERSION = "2.0.0"
AUTHOR = "Consolidador Pro Team"
DESCRIPTION = "Consolidador avanzado de archivos CSV y Excel"

# Directorios
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / 'src'
GENERADOS_DIR = BASE_DIR / 'generados'
LOGS_DIR = BASE_DIR / 'logs'
EXAMPLES_DIR = BASE_DIR / 'examples'
TESTS_DIR = BASE_DIR / 'tests'

# Configuración por defecto
DEFAULT_CONFIG = {
    # Nombres de columnas por defecto
    'columna_1_nombre': 'Archivo_Origen',
    'columna_2_nombre': 'Fecha_Procesamiento',
    
    # Opciones de procesamiento
    'eliminar_duplicados': False,
    'formato_salida': 'csv',
    
    # Configuración de archivos
    'encodings_csv': ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1'],
    'formatos_soportados': ['.csv', '.xlsx', '.xls'],
    
    # Configuración de interfaz
    'ventana_ancho': 900,
    'ventana_alto': 700,
    'ventana_titulo': f"{PROGRAM_NAME} v{VERSION}",
    
    # Configuración de logging
    'nivel_log': 'INFO',
    'max_size_log': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,
    
    # Límites
    'max_archivos': 100,
    'max_columnas_ignorar': 50,
    'max_registros_muestra': 1000,
}

# Mensajes de la interfaz
MESSAGES = {
    'archivo_guardado_exito': "Archivo consolidado creado exitosamente",
    'error_procesamiento': "Error durante el procesamiento",
    'sin_archivos_seleccionados': "No hay archivos seleccionados",
    'archivos_invalidos': "Archivos inválidos encontrados",
    'confirmar_limpiar': "¿Estás seguro de que quieres limpiar todo?",
    'dependencias_faltantes': "Dependencias faltantes",
    'error_importacion': "Error al importar módulos",
}

# Configuración de la interfaz gráfica
UI_CONFIG = {
    'colores': {
        'principal': '#2E86AB',
        'secundario': '#A23B72',
        'exito': '#28A745',
        'error': '#DC3545',
        'advertencia': '#FFC107',
        'info': '#17A2B8',
    },
    'fuentes': {
        'titulo': ('Arial', 16, 'bold'),
        'subtitulo': ('Arial', 12, 'bold'),
        'normal': ('Arial', 10),
        'pequena': ('Arial', 9),
    },
    'estilos': {
        'frame_principal': 'TFrame',
        'frame_secundario': 'TLabelFrame',
        'boton_principal': 'Accent.TButton',
        'boton_secundario': 'TButton',
    }
}

# Configuración de validación
VALIDATION_RULES = {
    'nombres_columnas': {
        'min_length': 1,
        'max_length': 50,
        'allowed_chars': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_',
    },
    'archivos': {
        'max_size_mb': 100,
        'min_size_bytes': 1,
    },
    'procesamiento': {
        'timeout_segundos': 300,  # 5 minutos
        'max_memory_mb': 1024,    # 1 GB
    }
}

# Configuración de exportación
EXPORT_CONFIG = {
    'csv': {
        'encoding': 'utf-8-sig',
        'separator': ',',
        'quotechar': '"',
        'lineterminator': '\n',
    },
    'excel': {
        'engine': 'openpyxl',
        'sheet_name': 'Consolidado',
        'index': False,
    }
}

def get_config(key: str, default=None):
    """Obtiene una configuración específica."""
    return DEFAULT_CONFIG.get(key, default)

def get_ui_config(category: str, key: str, default=None):
    """Obtiene una configuración específica de la UI."""
    return UI_CONFIG.get(category, {}).get(key, default)

def get_message(key: str, default=None):
    """Obtiene un mensaje específico."""
    return MESSAGES.get(key, default)

def get_validation_rule(category: str, key: str, default=None):
    """Obtiene una regla de validación específica."""
    return VALIDATION_RULES.get(category, {}).get(key, default)

def get_export_config(format_type: str, key: str, default=None):
    """Obtiene una configuración específica de exportación."""
    return EXPORT_CONFIG.get(format_type, {}).get(key, default)
