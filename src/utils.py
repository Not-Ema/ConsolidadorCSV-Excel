"""
Módulo de utilidades para el consolidador de archivos CSV y Excel.
Contiene funciones auxiliares para manejo de archivos y procesamiento de datos.
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileProcessor:
    """Clase para procesar archivos CSV y Excel."""
    
    @staticmethod
    def leer_archivo(ruta_archivo: str) -> pd.DataFrame:
        """
        Lee un archivo CSV o Excel y retorna un DataFrame.
        
        Args:
            ruta_archivo: Ruta del archivo a leer
            
        Returns:
            DataFrame con los datos del archivo
            
        Raises:
            Exception: Si no se puede leer el archivo
        """
        try:
            nombre_archivo = os.path.basename(ruta_archivo).lower()
            logger.info(f"Leyendo archivo: {nombre_archivo}")
            
            if nombre_archivo.endswith('.xlsx'):
                df = pd.read_excel(ruta_archivo, engine='openpyxl')
            elif nombre_archivo.endswith('.xls'):
                df = pd.read_excel(ruta_archivo, engine='xlrd')
            elif nombre_archivo.endswith('.csv'):
                # Intentar diferentes encodings para CSV
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encodings:
                    try:
                        df = pd.read_csv(ruta_archivo, encoding=encoding)
                        logger.info(f"Archivo CSV leído con encoding: {encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    # Si ninguno funciona, usar el último encoding
                    df = pd.read_csv(ruta_archivo, encoding='utf-8', errors='ignore')
                    logger.warning(f"Usando encoding UTF-8 con errores ignorados para {nombre_archivo}")
            else:
                raise ValueError(f"Tipo de archivo no soportado: {nombre_archivo}")
            
            logger.info(f"Archivo {nombre_archivo} leído exitosamente: {len(df)} registros, {len(df.columns)} columnas")
            return df
            
        except Exception as e:
            logger.error(f"Error al leer {ruta_archivo}: {str(e)}")
            raise Exception(f"Error al leer {ruta_archivo}: {str(e)}")
    
    @staticmethod
    def procesar_dataframe(df: pd.DataFrame, 
                          nombre_archivo: str,
                          columnas_a_ignorar: List[str],
                          columna_1_nombre: str = "Archivo_Origen",
                          columna_2_nombre: str = "Fecha_Procesamiento") -> pd.DataFrame:
        """
        Procesa un DataFrame agregando columnas y eliminando las especificadas.
        
        Args:
            df: DataFrame a procesar
            nombre_archivo: Nombre del archivo original
            columnas_a_ignorar: Lista de nombres de columnas a eliminar
            columna_1_nombre: Nombre de la primera columna a agregar
            columna_2_nombre: Nombre de la segunda columna a agregar
            
        Returns:
            DataFrame procesado
        """
        df_procesado = df.copy()
        
        # Agregar las dos columnas al inicio
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_procesado.insert(0, columna_1_nombre, os.path.basename(nombre_archivo))
        df_procesado.insert(1, columna_2_nombre, fecha_actual)
        
        # Eliminar columnas especificadas
        columnas_eliminadas = []
        for columna in columnas_a_ignorar:
            if columna in df_procesado.columns:
                df_procesado = df_procesado.drop(columns=[columna])
                columnas_eliminadas.append(columna)
                logger.info(f"Columna '{columna}' eliminada de {nombre_archivo}")
            else:
                logger.warning(f"Columna '{columna}' no encontrada en {nombre_archivo}")
        
        return df_procesado, columnas_eliminadas
    
    @staticmethod
    def guardar_archivo(df: pd.DataFrame, 
                       ruta_salida: str, 
                       formato: str = 'csv') -> bool:
        """
        Guarda un DataFrame en el formato especificado.
        
        Args:
            df: DataFrame a guardar
            ruta_salida: Ruta donde guardar el archivo
            formato: Formato de salida ('csv' o 'xlsx')
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
            
            if formato.lower() == 'csv':
                df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
                logger.info(f"Archivo CSV guardado: {ruta_salida}")
            elif formato.lower() == 'xlsx':
                df.to_excel(ruta_salida, index=False, engine='openpyxl')
                logger.info(f"Archivo Excel guardado: {ruta_salida}")
            else:
                raise ValueError(f"Formato no soportado: {formato}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar archivo {ruta_salida}: {str(e)}")
            return False


class FileManager:
    """Clase para manejar archivos y directorios."""
    
    @staticmethod
    def crear_nombre_archivo_salida(formato: str = 'csv') -> str:
        """
        Crea un nombre único para el archivo de salida.
        
        Args:
            formato: Formato del archivo ('csv' o 'xlsx')
            
        Returns:
            Nombre del archivo con timestamp
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        extension = 'csv' if formato.lower() == 'csv' else 'xlsx'
        return f"consolidado_{timestamp}.{extension}"
    
    @staticmethod
    def obtener_ruta_generados() -> str:
        """
        Obtiene la ruta del directorio de archivos generados.
        
        Returns:
            Ruta absoluta del directorio generados
        """
        # Obtener directorio actual del proyecto
        directorio_actual = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_generados = os.path.join(directorio_actual, 'generados')
        
        # Crear directorio si no existe
        os.makedirs(ruta_generados, exist_ok=True)
        
        return ruta_generados
    
    @staticmethod
    def validar_archivos(archivos: List[str]) -> Dict[str, Any]:
        """
        Valida una lista de archivos.
        
        Args:
            archivos: Lista de rutas de archivos
            
        Returns:
            Diccionario con archivos válidos e inválidos
        """
        archivos_validos = []
        archivos_invalidos = []
        
        for archivo in archivos:
            if os.path.exists(archivo) and os.path.isfile(archivo):
                nombre = os.path.basename(archivo).lower()
                if nombre.endswith(('.csv', '.xlsx', '.xls')):
                    archivos_validos.append(archivo)
                else:
                    archivos_invalidos.append(f"{archivo} (formato no soportado)")
            else:
                archivos_invalidos.append(f"{archivo} (archivo no encontrado)")
        
        return {
            'validos': archivos_validos,
            'invalidos': archivos_invalidos,
            'total_validos': len(archivos_validos),
            'total_invalidos': len(archivos_invalidos)
        }


class DataAnalyzer:
    """Clase para analizar datos del consolidado."""
    
    @staticmethod
    def generar_resumen(df: pd.DataFrame, archivos_procesados: List[str]) -> Dict[str, Any]:
        """
        Genera un resumen de los datos consolidados.
        
        Args:
            df: DataFrame consolidado
            archivos_procesados: Lista de archivos procesados
            
        Returns:
            Diccionario con el resumen
        """
        return {
            'total_registros': len(df),
            'total_columnas': len(df.columns),
            'archivos_procesados': len(archivos_procesados),
            'nombres_archivos': [os.path.basename(archivo) for archivo in archivos_procesados],
            'columnas': list(df.columns),
            'tipos_datos': df.dtypes.to_dict()
        }
    
    @staticmethod
    def detectar_duplicados(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detecta duplicados en el DataFrame.
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Diccionario con información de duplicados
        """
        duplicados = df.duplicated()
        total_duplicados = duplicados.sum()
        
        return {
            'tiene_duplicados': total_duplicados > 0,
            'total_duplicados': int(total_duplicados),
            'indices_duplicados': df[duplicados].index.tolist() if total_duplicados > 0 else []
        }
