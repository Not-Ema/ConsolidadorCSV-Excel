"""
Paquete Consolidador Pro - Consolidador de archivos CSV y Excel.

Este paquete proporciona funcionalidades para consolidar múltiples archivos
CSV y Excel en un solo archivo con opciones avanzadas de configuración.

Módulos:
- utils: Utilidades para procesamiento de archivos y análisis de datos
- processor: Lógica principal de consolidación
- ui: Interfaz gráfica de usuario
"""

from .utils import FileProcessor, FileManager, DataAnalyzer
from .processor import Consolidator
from .ui import ConsolidadorUI

__version__ = "2.0.0"
__author__ = "Consolidador Pro Team"

__all__ = [
    'FileProcessor',
    'FileManager', 
    'DataAnalyzer',
    'Consolidator',
    'ConsolidadorUI'
]
