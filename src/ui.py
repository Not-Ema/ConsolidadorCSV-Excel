"""
Módulo de interfaz de usuario para el consolidador de archivos.
Contiene la interfaz gráfica usando Tkinter con funcionalidades mejoradas.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Dict, Any
import threading
import logging
from .processor import Consolidator

logger = logging.getLogger(__name__)


class ConsolidadorUI:
    """Interfaz gráfica para el consolidador de archivos."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.consolidador = Consolidator()
        
        # Variables de la interfaz
        self.archivos_seleccionados = []
        self.columnas_a_ignorar = []
        
        # Configurar ventana principal
        self.configurar_ventana()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Variables de control
        self.procesando = False
    
    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.root.title("Consolidador Pro - CSV y Excel")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configurar el grid principal
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz."""
        # Frame principal con scrollbar
        self.crear_frame_principal()
        
        # Sección de selección de archivos
        self.crear_seccion_archivos()
        
        # Sección de configuración
        self.crear_seccion_configuracion()
        
        # Sección de columnas a ignorar
        self.crear_seccion_columnas_ignorar()
        
        # Sección de opciones avanzadas
        self.crear_seccion_opciones()
        
        # Sección de botones
        self.crear_seccion_botones()
        
        # Sección de resultados
        self.crear_seccion_resultados()
    
    def crear_frame_principal(self):
        """Crea el frame principal con scrollbar."""
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(0, weight=1)
        
        # Canvas y scrollbar para scroll vertical
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.main_frame.rowconfigure(0, weight=1)
        
        # Configurar scroll con mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Maneja el scroll del mouse."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def crear_seccion_archivos(self):
        """Crea la sección de selección de archivos."""
        # Frame para archivos
        frame_archivos = ttk.LabelFrame(self.scrollable_frame, text="📁 Archivos a Consolidar", padding="10")
        frame_archivos.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_archivos.columnconfigure(1, weight=1)
        
        # Botón de selección
        ttk.Button(frame_archivos, text="Seleccionar Archivos CSV/Excel", 
                  command=self.seleccionar_archivos).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Lista de archivos
        self.lista_archivos = tk.Listbox(frame_archivos, height=6, selectmode=tk.EXTENDED)
        self.lista_archivos.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Scrollbar para la lista
        scrollbar_lista = ttk.Scrollbar(frame_archivos, orient=tk.VERTICAL, command=self.lista_archivos.yview)
        scrollbar_lista.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.lista_archivos.configure(yscrollcommand=scrollbar_lista.set)
        
        # Botones de gestión de archivos
        frame_botones_archivos = ttk.Frame(frame_archivos)
        frame_botones_archivos.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Button(frame_botones_archivos, text="Eliminar Seleccionados", 
                  command=self.eliminar_archivos_seleccionados).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_archivos, text="Limpiar Lista", 
                  command=self.limpiar_lista_archivos).pack(side=tk.LEFT)
    
    def crear_seccion_configuracion(self):
        """Crea la sección de configuración de columnas."""
        frame_config = ttk.LabelFrame(self.scrollable_frame, text="⚙️ Configuración de Columnas", padding="10")
        frame_config.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_config.columnconfigure(1, weight=1)
        
        # Nombre columna 1
        ttk.Label(frame_config, text="Nombre Columna 1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_columna1 = ttk.Entry(frame_config, width=30)
        self.entry_columna1.insert(0, "Archivo_Origen")
        self.entry_columna1.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Nombre columna 2
        ttk.Label(frame_config, text="Nombre Columna 2:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_columna2 = ttk.Entry(frame_config, width=30)
        self.entry_columna2.insert(0, "Fecha_Procesamiento")
        self.entry_columna2.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Formato de salida
        ttk.Label(frame_config, text="Formato de salida:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.formato_salida = tk.StringVar(value="csv")
        frame_formato = ttk.Frame(frame_config)
        frame_formato.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Radiobutton(frame_formato, text="CSV (.csv)", variable=self.formato_salida, 
                       value="csv").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(frame_formato, text="Excel (.xlsx)", variable=self.formato_salida, 
                       value="xlsx").pack(side=tk.LEFT)
    
    def crear_seccion_columnas_ignorar(self):
        """Crea la sección para especificar columnas a ignorar."""
        frame_ignorar = ttk.LabelFrame(self.scrollable_frame, text="🚫 Columnas a Ignorar", padding="10")
        frame_ignorar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_ignorar.columnconfigure(1, weight=1)
        
        # Campo de entrada para columnas
        ttk.Label(frame_ignorar, text="Nombres de columnas (separadas por comas):").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.entry_columnas_ignorar = ttk.Entry(frame_ignorar, width=50)
        self.entry_columnas_ignorar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.entry_columnas_ignorar.insert(0, "Ejemplo: Telefono, Email, ID_interno")
        
        # Lista de columnas a ignorar
        ttk.Label(frame_ignorar, text="Columnas que se eliminarán:").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.lista_columnas_ignorar = tk.Listbox(frame_ignorar, height=4)
        self.lista_columnas_ignorar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Botones para gestionar columnas
        frame_botones_columnas = ttk.Frame(frame_ignorar)
        frame_botones_columnas.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(frame_botones_columnas, text="Agregar Columnas", 
                  command=self.agregar_columnas_ignorar).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_columnas, text="Eliminar Seleccionada", 
                  command=self.eliminar_columna_ignorar).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_columnas, text="Limpiar Lista", 
                  command=self.limpiar_columnas_ignorar).pack(side=tk.LEFT)
    
    def crear_seccion_opciones(self):
        """Crea la sección de opciones avanzadas."""
        frame_opciones = ttk.LabelFrame(self.scrollable_frame, text="🔧 Opciones Avanzadas", padding="10")
        frame_opciones.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Checkbox para eliminar duplicados
        self.eliminar_duplicados_var = tk.BooleanVar()
        ttk.Checkbutton(frame_opciones, text="Eliminar duplicados del resultado final", 
                       variable=self.eliminar_duplicados_var).pack(anchor=tk.W, pady=2)
        
        # Checkbox para mostrar progreso detallado
        self.progreso_detallado_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Mostrar progreso detallado", 
                       variable=self.progreso_detallado_var).pack(anchor=tk.W, pady=2)
    
    def crear_seccion_botones(self):
        """Crea la sección de botones principales."""
        frame_botones = ttk.Frame(self.scrollable_frame)
        frame_botones.grid(row=4, column=0, pady=20)
        
        # Botón principal de procesamiento
        self.btn_procesar = ttk.Button(frame_botones, text="🚀 Procesar y Consolidar", 
                                      command=self.procesar_archivos, style="Accent.TButton")
        self.btn_procesar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para limpiar todo
        ttk.Button(frame_botones, text="🧹 Limpiar Todo", 
                  command=self.limpiar_todo).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para salir
        ttk.Button(frame_botones, text="❌ Salir", 
                  command=self.root.quit).pack(side=tk.LEFT)
    
    def crear_seccion_resultados(self):
        """Crea la sección de resultados y logs."""
        frame_resultados = ttk.LabelFrame(self.scrollable_frame, text="📊 Resultados y Logs", padding="10")
        frame_resultados.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        
        # Área de texto para resultados
        self.texto_resultados = tk.Text(frame_resultados, height=15, width=80, wrap=tk.WORD)
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        # Scrollbar para el área de texto
        scrollbar_texto = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.texto_resultados.yview)
        scrollbar_texto.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.texto_resultados.configure(yscrollcommand=scrollbar_texto.set)
        
        # Frame para estadísticas
        self.frame_estadisticas = ttk.Frame(frame_resultados)
        self.frame_estadisticas.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def seleccionar_archivos(self):
        """Permite al usuario seleccionar múltiples archivos."""
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos CSV y Excel",
            filetypes=[
                ("Archivos CSV y Excel", "*.csv;*.xlsx"), 
                ("Archivos CSV", "*.csv"), 
                ("Archivos Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        for archivo in archivos:
            if archivo not in self.archivos_seleccionados:
                self.archivos_seleccionados.append(archivo)
                self.lista_archivos.insert(tk.END, os.path.basename(archivo))
        
        self.actualizar_estadisticas()
    
    def eliminar_archivos_seleccionados(self):
        """Elimina los archivos seleccionados de la lista."""
        seleccionados = self.lista_archivos.curselection()
        
        # Eliminar en orden inverso para mantener los índices
        for indice in reversed(seleccionados):
            self.archivos_seleccionados.pop(indice)
            self.lista_archivos.delete(indice)
        
        self.actualizar_estadisticas()
    
    def limpiar_lista_archivos(self):
        """Limpia la lista de archivos seleccionados."""
        self.archivos_seleccionados.clear()
        self.lista_archivos.delete(0, tk.END)
        self.actualizar_estadisticas()
    
    def agregar_columnas_ignorar(self):
        """Agrega columnas a la lista de columnas a ignorar."""
        texto = self.entry_columnas_ignorar.get().strip()
        
        if not texto or texto == "Ejemplo: Telefono, Email, ID_interno":
            messagebox.showwarning("Advertencia", "Por favor ingresa nombres de columnas")
            return
        
        # Separar por comas y limpiar
        columnas = [col.strip() for col in texto.split(',') if col.strip()]
        
        for columna in columnas:
            if columna not in self.columnas_a_ignorar:
                self.columnas_a_ignorar.append(columna)
                self.lista_columnas_ignorar.insert(tk.END, columna)
        
        self.entry_columnas_ignorar.delete(0, tk.END)
        self.entry_columnas_ignorar.insert(0, "")
    
    def eliminar_columna_ignorar(self):
        """Elimina la columna seleccionada de la lista."""
        seleccionado = self.lista_columnas_ignorar.curselection()
        
        if seleccionado:
            indice = seleccionado[0]
            self.columnas_a_ignorar.pop(indice)
            self.lista_columnas_ignorar.delete(indice)
    
    def limpiar_columnas_ignorar(self):
        """Limpia la lista de columnas a ignorar."""
        self.columnas_a_ignorar.clear()
        self.lista_columnas_ignorar.delete(0, tk.END)
    
    def procesar_archivos(self):
        """Procesa los archivos seleccionados en un hilo separado."""
        if self.procesando:
            return
        
        if not self.archivos_seleccionados:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados")
            return
        
        # Iniciar procesamiento en hilo separado
        self.procesando = True
        self.btn_procesar.config(text="⏳ Procesando...", state="disabled")
        
        thread = threading.Thread(target=self._procesar_archivos_thread)
        thread.daemon = True
        thread.start()
    
    def _procesar_archivos_thread(self):
        """Procesa los archivos en un hilo separado."""
        try:
            # Configurar consolidador
            self.consolidador.configurar(
                columna_1_nombre=self.entry_columna1.get().strip() or "Archivo_Origen",
                columna_2_nombre=self.entry_columna2.get().strip() or "Fecha_Procesamiento",
                columnas_a_ignorar=self.columnas_a_ignorar,
                eliminar_duplicados=self.eliminar_duplicados_var.get()
            )
            
            # Procesar y guardar
            resultado = self.consolidador.procesar_y_guardar(
                archivos=self.archivos_seleccionados,
                formato=self.formato_salida.get()
            )
            
            # Actualizar interfaz en el hilo principal
            self.root.after(0, self._mostrar_resultado, resultado)
            
        except Exception as e:
            logger.error(f"Error en procesamiento: {str(e)}")
            self.root.after(0, self._mostrar_error, str(e))
        
        finally:
            # Restaurar botón
            self.root.after(0, self._finalizar_procesamiento)
    
    def _mostrar_resultado(self, resultado: Dict[str, Any]):
        """Muestra el resultado del procesamiento."""
        self.texto_resultados.delete(1.0, tk.END)
        
        if resultado['exito']:
            self.texto_resultados.insert(tk.END, "✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE\n")
            self.texto_resultados.insert(tk.END, "="*60 + "\n\n")
            
            # Información general
            resumen = resultado['resumen']
            self.texto_resultados.insert(tk.END, f"📊 RESUMEN GENERAL:\n")
            self.texto_resultados.insert(tk.END, f"   • Total de registros: {resumen['total_registros']:,}\n")
            self.texto_resultados.insert(tk.END, f"   • Total de columnas: {resumen['total_columnas']}\n")
            self.texto_resultados.insert(tk.END, f"   • Archivos procesados: {resumen['archivos_procesados']}\n")
            self.texto_resultados.insert(tk.END, f"   • Formato de salida: {resultado['guardado']['formato'].upper()}\n\n")
            
            # Archivos procesados
            self.texto_resultados.insert(tk.END, f"📁 ARCHIVOS PROCESADOS:\n")
            for archivo in resumen['nombres_archivos']:
                self.texto_resultados.insert(tk.END, f"   • {archivo}\n")
            self.texto_resultados.insert(tk.END, "\n")
            
            # Columnas eliminadas
            if resultado['columnas_eliminadas_por_archivo']:
                self.texto_resultados.insert(tk.END, f"🚫 COLUMNAS ELIMINADAS:\n")
                for archivo, columnas in resultado['columnas_eliminadas_por_archivo'].items():
                    if columnas:
                        self.texto_resultados.insert(tk.END, f"   • {archivo}: {', '.join(columnas)}\n")
                self.texto_resultados.insert(tk.END, "\n")
            
            # Duplicados
            if resultado['duplicados_eliminados'] > 0:
                self.texto_resultados.insert(tk.END, f"🔄 DUPLICADOS ELIMINADOS: {resultado['duplicados_eliminados']}\n\n")
            
            # Información del archivo guardado
            guardado = resultado['guardado']
            self.texto_resultados.insert(tk.END, f"💾 ARCHIVO GUARDADO:\n")
            self.texto_resultados.insert(tk.END, f"   • Nombre: {guardado['nombre_archivo']}\n")
            self.texto_resultados.insert(tk.END, f"   • Ubicación: {guardado['ruta_archivo']}\n")
            self.texto_resultados.insert(tk.END, f"   • Registros: {guardado['registros']:,}\n")
            self.texto_resultados.insert(tk.END, f"   • Columnas: {guardado['columnas']}\n\n")
            
            # Errores si los hay
            if resultado['archivos_con_errores']:
                self.texto_resultados.insert(tk.END, f"⚠️ ARCHIVOS CON ERRORES:\n")
                for error in resultado['archivos_con_errores']:
                    self.texto_resultados.insert(tk.END, f"   • {error}\n")
                self.texto_resultados.insert(tk.END, "\n")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", 
                              f"Archivo consolidado creado exitosamente:\n{guardado['nombre_archivo']}\n\n"
                              f"Registros: {guardado['registros']:,}\n"
                              f"Ubicación: {guardado['ruta_archivo']}")
        else:
            self._mostrar_error(resultado.get('error', 'Error desconocido'))
    
    def _mostrar_error(self, error: str):
        """Muestra un mensaje de error."""
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"❌ ERROR EN EL PROCESAMIENTO:\n")
        self.texto_resultados.insert(tk.END, "="*60 + "\n\n")
        self.texto_resultados.insert(tk.END, f"{error}\n")
        
        messagebox.showerror("Error", f"Error durante el procesamiento:\n{error}")
    
    def _finalizar_procesamiento(self):
        """Finaliza el procesamiento y restaura la interfaz."""
        self.procesando = False
        self.btn_procesar.config(text="🚀 Procesar y Consolidar", state="normal")
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas."""
        # Limpiar estadísticas anteriores
        for widget in self.frame_estadisticas.winfo_children():
            widget.destroy()
        
        # Mostrar estadísticas básicas
        ttk.Label(self.frame_estadisticas, 
                 text=f"Archivos seleccionados: {len(self.archivos_seleccionados)} | "
                      f"Columnas a ignorar: {len(self.columnas_a_ignorar)}",
                 font=("Arial", 9, "bold")).pack(anchor=tk.W)
    
    def limpiar_todo(self):
        """Limpia toda la interfaz."""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres limpiar todo?"):
            self.limpiar_lista_archivos()
            self.limpiar_columnas_ignorar()
            self.texto_resultados.delete(1.0, tk.END)
            self.entry_columna1.delete(0, tk.END)
            self.entry_columna1.insert(0, "Archivo_Origen")
            self.entry_columna2.delete(0, tk.END)
            self.entry_columna2.insert(0, "Fecha_Procesamiento")
            self.entry_columnas_ignorar.delete(0, tk.END)
            self.entry_columnas_ignorar.insert(0, "Ejemplo: Telefono, Email, ID_interno")
            self.eliminar_duplicados_var.set(False)
            self.actualizar_estadisticas()
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.actualizar_estadisticas()
        self.root.mainloop()


# Importar os para uso en el módulo
import os
