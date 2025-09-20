#!/usr/bin/env python3
"""
Consolidador Pro - Consolidador de archivos CSV y Excel
Versión 2.0.0

Programa principal para consolidar múltiples archivos CSV y Excel
en un solo archivo con opciones avanzadas de configuración.

Características:
- Soporte para archivos CSV y Excel (.xlsx, .xls)
- Múltiples columnas a ignorar
- Exportación a CSV y Excel
- Interfaz gráfica moderna
- Procesamiento en hilos separados
- Logging detallado
- Archivos de salida en carpeta separada

Autor: Sebastian Abdala Asencio
Versión: 2.0.0
"""

import sys
import os
import logging
from pathlib import Path

# Agregar el directorio src al path para importaciones
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

try:
    from src.ui import ConsolidadorUI
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de que todas las dependencias estén instaladas.")
    print("Ejecuta: pip install pandas openpyxl")
    sys.exit(1)


def configurar_logging():
    """Configura el sistema de logging."""
    # Crear directorio de logs si no existe
    log_dir = current_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'consolidador.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Consolidador Pro iniciado - Versión 2.0.0")


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas."""
    dependencias = ['pandas', 'openpyxl']
    faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltantes.append(dep)
    
    if faltantes:
        print("❌ Dependencias faltantes:")
        for dep in faltantes:
            print(f"   • {dep}")
        print("\nPara instalar las dependencias, ejecuta:")
        print("pip install pandas openpyxl")
        return False
    
    return True


def crear_estructura_directorios():
    """Crea la estructura de directorios necesaria."""
    directorios = [
        current_dir / 'generados',
        current_dir / 'logs',
        current_dir / 'examples'
    ]
    
    for directorio in directorios:
        directorio.mkdir(exist_ok=True)


def main():
    """Función principal del programa."""
    print("🚀 Iniciando Consolidador Pro v2.0.0")
    print("=" * 50)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ No se puede continuar sin las dependencias necesarias.")
        input("Presiona Enter para salir...")
        sys.exit(1)
    
    # Crear estructura de directorios
    crear_estructura_directorios()
    
    # Configurar logging
    configurar_logging()
    
    try:
        print("✅ Dependencias verificadas")
        print("✅ Estructura de directorios creada")
        print("✅ Sistema de logging configurado")
        print("\n🎯 Iniciando interfaz gráfica...")
        
        # Crear y ejecutar la aplicación
        app = ConsolidadorUI()
        app.ejecutar()
        
    except Exception as e:
        logging.error(f"Error fatal en la aplicación: {str(e)}")
        print(f"\n❌ Error fatal: {str(e)}")
        print("Revisa el archivo de log para más detalles.")
        input("Presiona Enter para salir...")
        sys.exit(1)
    
    print("\n👋 ¡Gracias por usar Consolidador Pro!")


if __name__ == "__main__":
    main()
