"""
Módulo principal de procesamiento para el consolidador de archivos.
Maneja la lógica de consolidación y procesamiento de múltiples archivos.
"""

import pandas as pd
from typing import List, Dict, Any, Tuple
import logging
from .utils import FileProcessor, FileManager, DataAnalyzer

logger = logging.getLogger(__name__)


class Consolidator:
    """Clase principal para consolidar archivos CSV y Excel."""
    
    def __init__(self):
        self.file_processor = FileProcessor()
        self.file_manager = FileManager()
        self.data_analyzer = DataAnalyzer()
        
        # Configuración por defecto
        self.columna_1_nombre = "Archivo_Origen"
        self.columna_2_nombre = "Fecha_Procesamiento"
        self.eliminar_duplicados = False
        self.columnas_a_ignorar = []
    
    def configurar(self, 
                   columna_1_nombre: str = "Archivo_Origen",
                   columna_2_nombre: str = "Fecha_Procesamiento",
                   columnas_a_ignorar: List[str] = None,
                   eliminar_duplicados: bool = False):
        """
        Configura los parámetros del consolidador.
        
        Args:
            columna_1_nombre: Nombre de la primera columna a agregar
            columna_2_nombre: Nombre de la segunda columna a agregar
            columnas_a_ignorar: Lista de columnas a ignorar
            eliminar_duplicados: Si eliminar duplicados del resultado final
        """
        self.columna_1_nombre = columna_1_nombre
        self.columna_2_nombre = columna_2_nombre
        self.columnas_a_ignorar = columnas_a_ignorar or []
        self.eliminar_duplicados = eliminar_duplicados
        
        logger.info(f"Configuración actualizada: {self.__dict__}")
    
    def procesar_archivos(self, archivos: List[str]) -> Dict[str, Any]:
        """
        Procesa múltiples archivos y los consolida.
        
        Args:
            archivos: Lista de rutas de archivos a procesar
            
        Returns:
            Diccionario con el resultado del procesamiento
        """
        logger.info(f"Iniciando procesamiento de {len(archivos)} archivos")
        
        # Validar archivos
        validacion = self.file_manager.validar_archivos(archivos)
        
        if validacion['total_validos'] == 0:
            return {
                'exito': False,
                'error': 'No hay archivos válidos para procesar',
                'archivos_invalidos': validacion['invalidos']
            }
        
        if validacion['total_invalidos'] > 0:
            logger.warning(f"Archivos inválidos encontrados: {validacion['invalidos']}")
        
        # Procesar archivos válidos
        dataframes = []
        archivos_procesados = []
        errores = []
        columnas_eliminadas_por_archivo = {}
        
        for archivo in validacion['validos']:
            try:
                logger.info(f"Procesando archivo: {archivo}")
                
                # Leer archivo
                df = self.file_processor.leer_archivo(archivo)
                
                # Procesar DataFrame
                df_procesado, columnas_eliminadas = self.file_processor.procesar_dataframe(
                    df=df,
                    nombre_archivo=archivo,
                    columnas_a_ignorar=self.columnas_a_ignorar,
                    columna_1_nombre=self.columna_1_nombre,
                    columna_2_nombre=self.columna_2_nombre
                )
                
                dataframes.append(df_procesado)
                archivos_procesados.append(archivo)
                columnas_eliminadas_por_archivo[os.path.basename(archivo)] = columnas_eliminadas
                
                logger.info(f"Archivo {archivo} procesado exitosamente: {len(df_procesado)} registros")
                
            except Exception as e:
                error_msg = f"Error procesando {archivo}: {str(e)}"
                logger.error(error_msg)
                errores.append(error_msg)
                continue
        
        if not dataframes:
            return {
                'exito': False,
                'error': 'No se pudo procesar ningún archivo válido',
                'errores': errores
            }
        
        # Consolidar DataFrames
        logger.info("Consolidando DataFrames...")
        df_consolidado = pd.concat(dataframes, ignore_index=True)
        
        # Eliminar duplicados si se solicita
        duplicados_eliminados = 0
        if self.eliminar_duplicados:
            antes = len(df_consolidado)
            df_consolidado = df_consolidado.drop_duplicates().reset_index(drop=True)
            duplicados_eliminados = antes - len(df_consolidado)
            logger.info(f"Duplicados eliminados: {duplicados_eliminados}")
        
        # Generar resumen
        resumen = self.data_analyzer.generar_resumen(df_consolidado, archivos_procesados)
        info_duplicados = self.data_analyzer.detectar_duplicados(df_consolidado)
        
        resultado = {
            'exito': True,
            'dataframe': df_consolidado,
            'archivos_procesados': archivos_procesados,
            'archivos_con_errores': errores,
            'archivos_invalidos': validacion['invalidos'],
            'columnas_eliminadas_por_archivo': columnas_eliminadas_por_archivo,
            'duplicados_eliminados': duplicados_eliminados,
            'resumen': resumen,
            'info_duplicados': info_duplicados
        }
        
        logger.info(f"Procesamiento completado: {resumen['total_registros']} registros, {resumen['total_columnas']} columnas")
        return resultado
    
    def guardar_consolidado(self, 
                           df: pd.DataFrame, 
                           formato: str = 'csv',
                           nombre_personalizado: str = None) -> Dict[str, Any]:
        """
        Guarda el DataFrame consolidado en el formato especificado.
        
        Args:
            df: DataFrame consolidado
            formato: Formato de salida ('csv' o 'xlsx')
            nombre_personalizado: Nombre personalizado para el archivo (opcional)
            
        Returns:
            Diccionario con el resultado del guardado
        """
        try:
            # Determinar nombre del archivo
            if nombre_personalizado:
                nombre_archivo = f"{nombre_personalizado}.{formato.lower()}"
            else:
                nombre_archivo = self.file_manager.crear_nombre_archivo_salida(formato)
            
            # Obtener ruta de salida
            ruta_generados = self.file_manager.obtener_ruta_generados()
            ruta_completa = os.path.join(ruta_generados, nombre_archivo)
            
            # Guardar archivo
            exito = self.file_processor.guardar_archivo(df, ruta_completa, formato)
            
            if exito:
                return {
                    'exito': True,
                    'ruta_archivo': ruta_completa,
                    'nombre_archivo': nombre_archivo,
                    'formato': formato,
                    'registros': len(df),
                    'columnas': len(df.columns)
                }
            else:
                return {
                    'exito': False,
                    'error': 'Error al guardar el archivo'
                }
                
        except Exception as e:
            logger.error(f"Error al guardar consolidado: {str(e)}")
            return {
                'exito': False,
                'error': f'Error al guardar el archivo: {str(e)}'
            }
    
    def procesar_y_guardar(self, 
                          archivos: List[str], 
                          formato: str = 'csv',
                          nombre_personalizado: str = None) -> Dict[str, Any]:
        """
        Procesa archivos y guarda el resultado consolidado.
        
        Args:
            archivos: Lista de archivos a procesar
            formato: Formato de salida ('csv' o 'xlsx')
            nombre_personalizado: Nombre personalizado para el archivo (opcional)
            
        Returns:
            Diccionario con el resultado completo
        """
        # Procesar archivos
        resultado_procesamiento = self.procesar_archivos(archivos)
        
        if not resultado_procesamiento['exito']:
            return resultado_procesamiento
        
        # Guardar resultado
        resultado_guardado = self.guardar_consolidado(
            df=resultado_procesamiento['dataframe'],
            formato=formato,
            nombre_personalizado=nombre_personalizado
        )
        
        # Combinar resultados
        resultado_final = {
            **resultado_procesamiento,
            'guardado': resultado_guardado
        }
        
        return resultado_final


# Importar os para uso en el módulo
import os
