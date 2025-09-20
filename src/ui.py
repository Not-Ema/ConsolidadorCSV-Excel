"""
Módulo de interfaz de usuario para el consolidador de archivos.
Contiene la interfaz gráfica usando Tkinter con funcionalidades mejoradas.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Dict, Any
import threading
import logging
import pandas as pd  # para detectar encabezados (rápido con nrows=0)
from .processor import Consolidator

logger = logging.getLogger(__name__)


class ConsolidadorUI:
    """Interfaz gráfica para el consolidador de archivos."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.consolidador = Consolidator()
        
        # Variables de la interfaz
        self.archivos_seleccionados: List[str] = []
        self.columnas_a_ignorar: List[str] = []

        # NUEVO: manejo de modos y columnas a incluir
        self.modo_columnas_var = tk.StringVar(value="ignorar")  # incluir_manual | incluir_lista | ignorar
        self.columnas_disponibles: List[str] = []
        self.columnas_a_incluir: List[str] = []  # para modo incluir_manual
        
        # Configurar ventana principal
        self.configurar_ventana()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Variables de control
        self.procesando = False
    
    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.root.title("Consolidador Pro - CSV y Excel")
        self.root.geometry("1000x780")
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

        # NUEVO: Selector de modo
        self.crear_seccion_modo_columnas()

        # NUEVO: Sección incluir (selección manual)
        self.crear_seccion_incluir_manual()

        # NUEVO: Sección incluir (por lista)
        self.crear_seccion_incluir_lista()
        
        # Sección de columnas a ignorar
        self.crear_seccion_columnas_ignorar()
        
        # Sección de opciones avanzadas
        self.crear_seccion_opciones()
        
        # Sección de botones
        self.crear_seccion_botones()
        
        # Sección de resultados
        self.crear_seccion_resultados()

        # Mostrar solo la sección correspondiente al modo actual
        self._actualizar_modo_columnas()
    
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
        frame_archivos = ttk.LabelFrame(self.scrollable_frame, text="📁 Archivos a Consolidar", padding="10")
        frame_archivos.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_archivos.columnconfigure(1, weight=1)
        
        ttk.Button(frame_archivos, text="Seleccionar Archivos CSV/Excel", 
                  command=self.seleccionar_archivos).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.lista_archivos = tk.Listbox(frame_archivos, height=6, selectmode=tk.EXTENDED)
        self.lista_archivos.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        scrollbar_lista = ttk.Scrollbar(frame_archivos, orient=tk.VERTICAL, command=self.lista_archivos.yview)
        scrollbar_lista.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.lista_archivos.configure(yscrollcommand=scrollbar_lista.set)
        
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
        
        ttk.Label(frame_config, text="Nombre Columna 1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_columna1 = ttk.Entry(frame_config, width=30)
        self.entry_columna1.insert(0, "Archivo_Origen")
        self.entry_columna1.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        ttk.Label(frame_config, text="Nombre Columna 2:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_columna2 = ttk.Entry(frame_config, width=30)
        self.entry_columna2.insert(0, "Fecha_Procesamiento")
        self.entry_columna2.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        ttk.Label(frame_config, text="Formato de salida:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.formato_salida = tk.StringVar(value="csv")
        frame_formato = ttk.Frame(frame_config)
        frame_formato.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Radiobutton(frame_formato, text="CSV (.csv)", variable=self.formato_salida, value="csv").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(frame_formato, text="Excel (.xlsx)", variable=self.formato_salida, value="xlsx").pack(side=tk.LEFT)
    
    # =============== NUEVO: Selector de modo de manejo de columnas ===============
    def crear_seccion_modo_columnas(self):
        frame_modo = ttk.LabelFrame(self.scrollable_frame, text="🧭 Modo de manejo de columnas", padding="10")
        frame_modo.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_modo.columnconfigure(0, weight=1)

        ttk.Radiobutton(frame_modo, text="Incluir (selección manual)", variable=self.modo_columnas_var,
                        value="incluir_manual", command=self._actualizar_modo_columnas).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(frame_modo, text="Incluir (por lista de nombres)", variable=self.modo_columnas_var,
                        value="incluir_lista", command=self._actualizar_modo_columnas).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(frame_modo, text="Ignorar (lista de nombres)", variable=self.modo_columnas_var,
                        value="ignorar", command=self._actualizar_modo_columnas).grid(row=2, column=0, sticky=tk.W, pady=2)

    # =============== NUEVO: Incluir (selección manual) ===============
    def crear_seccion_incluir_manual(self):
        self.frame_incluir_manual = ttk.LabelFrame(self.scrollable_frame, text="✅ Incluir (selección manual)", padding="10")
        self.frame_incluir_manual.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.frame_incluir_manual.columnconfigure(0, weight=1)
        self.frame_incluir_manual.columnconfigure(2, weight=1)

        ttk.Label(self.frame_incluir_manual, text="Disponibles (unión de todos los archivos):").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.frame_incluir_manual, text="A incluir:").grid(row=0, column=2, sticky=tk.W)

        self.lista_columnas_disponibles = tk.Listbox(self.frame_incluir_manual, height=8, selectmode=tk.EXTENDED)
        self.lista_columnas_disponibles.grid(row=1, column=0, sticky=(tk.W, tk.E))

        botones_mv = ttk.Frame(self.frame_incluir_manual)
        botones_mv.grid(row=1, column=1, padx=10)
        ttk.Button(botones_mv, text="➜ Añadir ▶", command=self.agregar_incluir_desde_seleccion).pack(pady=2)
        ttk.Button(botones_mv, text="◀ Quitar", command=self.quitar_incluir_desde_seleccion).pack(pady=2)
        ttk.Button(botones_mv, text="Limpiar", command=self.limpiar_columnas_incluir).pack(pady=2)

        self.lista_columnas_incluir = tk.Listbox(self.frame_incluir_manual, height=8, selectmode=tk.EXTENDED)
        self.lista_columnas_incluir.grid(row=1, column=2, sticky=(tk.W, tk.E))

    # =============== NUEVO: Incluir (por lista) ===============
    def crear_seccion_incluir_lista(self):
        self.frame_incluir_lista = ttk.LabelFrame(self.scrollable_frame, text="✅ Incluir (por lista de nombres)", padding="10")
        self.frame_incluir_lista.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.frame_incluir_lista.columnconfigure(0, weight=1)

        ttk.Label(self.frame_incluir_lista, text="Escribe los nombres de columnas a incluir, separados por comas:").grid(row=0, column=0, sticky=tk.W)
        self.entry_incluir_lista = ttk.Entry(self.frame_incluir_lista)
        self.entry_incluir_lista.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(6, 0))

        ttk.Label(self.frame_incluir_lista, text="Ejemplo: Cliente, Documento, Valor, FECHA_ASIG, FECHA_LEG", foreground="#555").grid(row=2, column=0, sticky=tk.W, pady=(6, 0))

    def agregar_incluir_desde_seleccion(self):
        sel = [self.lista_columnas_disponibles.get(i) for i in self.lista_columnas_disponibles.curselection()]
        for c in sel:
            if c not in self.columnas_a_incluir:
                self.columnas_a_incluir.append(c)
                self.lista_columnas_incluir.insert(tk.END, c)
        self.actualizar_estadisticas()

    def quitar_incluir_desde_seleccion(self):
        sel_idx = list(self.lista_columnas_incluir.curselection())
        for i in reversed(sel_idx):
            col = self.lista_columnas_incluir.get(i)
            self.columnas_a_incluir.remove(col)
            self.lista_columnas_incluir.delete(i)
        self.actualizar_estadisticas()

    def limpiar_columnas_incluir(self):
        self.columnas_a_incluir.clear()
        self.lista_columnas_incluir.delete(0, tk.END)
        self.actualizar_estadisticas()

    # =================== Columnas a Ignorar (como antes) ===================
    def crear_seccion_columnas_ignorar(self):
        """Crea la sección para especificar columnas a ignorar."""
        self.frame_ignorar = ttk.LabelFrame(self.scrollable_frame, text="🚫 Ignorar columnas (si eliges este modo)", padding="10")
        self.frame_ignorar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.frame_ignorar.columnconfigure(1, weight=1)
        
        ttk.Label(self.frame_ignorar, text="Nombres de columnas (separadas por comas):").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.entry_columnas_ignorar = ttk.Entry(self.frame_ignorar, width=50)
        self.entry_columnas_ignorar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.entry_columnas_ignorar.insert(0, "Ejemplo: Telefono, Email, ID_interno")
        
        ttk.Label(self.frame_ignorar, text="Columnas que se eliminarán:").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.lista_columnas_ignorar = tk.Listbox(self.frame_ignorar, height=4)
        self.lista_columnas_ignorar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        frame_botones_columnas = ttk.Frame(self.frame_ignorar)
        frame_botones_columnas.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(frame_botones_columnas, text="Agregar Columnas", command=self.agregar_columnas_ignorar).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_columnas, text="Eliminar Seleccionada", command=self.eliminar_columna_ignorar).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones_columnas, text="Limpiar Lista", command=self.limpiar_columnas_ignorar).pack(side=tk.LEFT)
    
    def crear_seccion_opciones(self):
        """Crea la sección de opciones avanzadas."""
        frame_opciones = ttk.LabelFrame(self.scrollable_frame, text="🔧 Opciones Avanzadas", padding="10")
        frame_opciones.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.eliminar_duplicados_var = tk.BooleanVar()
        ttk.Checkbutton(frame_opciones, text="Eliminar duplicados del resultado final", 
                       variable=self.eliminar_duplicados_var).pack(anchor=tk.W, pady=2)
        
        self.progreso_detallado_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Mostrar progreso detallado", 
                       variable=self.progreso_detallado_var).pack(anchor=tk.W, pady=2)
    
    def crear_seccion_botones(self):
        """Crea la sección de botones principales."""
        frame_botones = ttk.Frame(self.scrollable_frame)
        frame_botones.grid(row=7, column=0, pady=20)
        
        self.btn_procesar = ttk.Button(frame_botones, text="🚀 Procesar y Consolidar", 
                                      command=self.procesar_archivos, style="Accent.TButton")
        self.btn_procesar.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(frame_botones, text="🧹 Limpiar Todo", 
                  command=self.limpiar_todo).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(frame_botones, text="❌ Salir", 
                  command=self.root.quit).pack(side=tk.LEFT)
    
    def crear_seccion_resultados(self):
        """Crea la sección de resultados y logs."""
        frame_resultados = ttk.LabelFrame(self.scrollable_frame, text="📊 Resultados y Logs", padding="10")
        frame_resultados.grid(row=8, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        
        self.texto_resultados = tk.Text(frame_resultados, height=15, width=80, wrap=tk.WORD)
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        scrollbar_texto = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.texto_resultados.yview)
        scrollbar_texto.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.texto_resultados.configure(yscrollcommand=scrollbar_texto.set)
        
        self.frame_estadisticas = ttk.Frame(frame_resultados)
        self.frame_estadisticas.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def seleccionar_archivos(self):
        """Permite al usuario seleccionar múltiples archivos."""
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos CSV y Excel",
            filetypes=[
                ("Archivos CSV y Excel", "*.csv;*.xlsx;*.xls"), 
                ("Archivos CSV", "*.csv"), 
                ("Archivos Excel", "*.xlsx;*.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        for archivo in archivos:
            if archivo not in self.archivos_seleccionados:
                self.archivos_seleccionados.append(archivo)
                self.lista_archivos.insert(tk.END, os.path.basename(archivo))

        # Detectar columnas disponibles para selección manual
        self._cargar_columnas_disponibles()
        self.actualizar_estadisticas()
    
    def eliminar_archivos_seleccionados(self):
        """Elimina los archivos seleccionados de la lista."""
        seleccionados = self.lista_archivos.curselection()
        
        for indice in reversed(seleccionados):
            self.archivos_seleccionados.pop(indice)
            self.lista_archivos.delete(indice)

        self._cargar_columnas_disponibles()
        self.actualizar_estadisticas()
    
    def limpiar_lista_archivos(self):
        """Limpia la lista de archivos seleccionados."""
        self.archivos_seleccionados.clear()
        self.lista_archivos.delete(0, tk.END)
        self._cargar_columnas_disponibles()
        self.actualizar_estadisticas()
    
    def agregar_columnas_ignorar(self):
        """Agrega columnas a la lista de columnas a ignorar."""
        texto = self.entry_columnas_ignorar.get().strip()
        
        if not texto or texto == "Ejemplo: Telefono, Email, ID_interno":
            messagebox.showwarning("Advertencia", "Por favor ingresa nombres de columnas")
            return
        
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
        
        self.procesando = True
        self.btn_procesar.config(text="⏳ Procesando...", state="disabled")
        
        thread = threading.Thread(target=self._procesar_archivos_thread)
        thread.daemon = True
        thread.start()
    
    def _procesar_archivos_thread(self):
        """Procesa los archivos en un hilo separado."""
        try:
            modo = self.modo_columnas_var.get()
            logger.info(f"Modo de columnas: {modo}")

            if modo in ("incluir_manual", "incluir_lista"):
                # Obtener lista a incluir
                if modo == "incluir_manual":
                    columnas_incluir = list(self.columnas_a_incluir)
                else:  # incluir_lista
                    texto = (self.entry_incluir_lista.get() or "").strip()
                    columnas_incluir = [c.strip() for c in texto.split(",") if c.strip()]

                # Descubrir unión de columnas de archivos seleccionados
                union_cols = self._descubrir_union_columnas(self.archivos_seleccionados)
                # Ignorar todo lo que no esté en la lista a incluir
                usar_cols_ignorar = [c for c in union_cols if c not in set(columnas_incluir)]
                logger.info(f"Incluir: {len(columnas_incluir)} | Se ignorarán (complemento): {len(usar_cols_ignorar)}")
            else:
                usar_cols_ignorar = list(self.columnas_a_ignorar)
                logger.info(f"Ignorar explícitas: {len(usar_cols_ignorar)}")

            # Configurar consolidador
            self.consolidador.configurar(
                columna_1_nombre=self.entry_columna1.get().strip() or "Archivo_Origen",
                columna_2_nombre=self.entry_columna2.get().strip() or "Fecha_Procesamiento",
                columnas_a_ignorar=usar_cols_ignorar,
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
            self.root.after(0, self._finalizar_procesamiento)
    
    def _mostrar_resultado(self, resultado: Dict[str, Any]):
        """Muestra el resultado del procesamiento."""
        self.texto_resultados.delete(1.0, tk.END)
        
        if resultado['exito']:
            self.texto_resultados.insert(tk.END, "✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE\n")
            self.texto_resultados.insert(tk.END, "="*60 + "\n\n")
            
            resumen = resultado['resumen']
            self.texto_resultados.insert(tk.END, f"📊 RESUMEN GENERAL:\n")
            self.texto_resultados.insert(tk.END, f"   • Total de registros: {resumen['total_registros']:,}\n")
            self.texto_resultados.insert(tk.END, f"   • Total de columnas: {resumen['total_columnas']}\n")
            self.texto_resultados.insert(tk.END, f"   • Archivos procesados: {resumen['archivos_procesados']}\n")
            self.texto_resultados.insert(tk.END, f"   • Formato de salida: {resultado['guardado']['formato'].upper()}\n\n")
            
            self.texto_resultados.insert(tk.END, f"📁 ARCHIVOS PROCESADOS:\n")
            for archivo in resumen['nombres_archivos']:
                self.texto_resultados.insert(tk.END, f"   • {archivo}\n")
            self.texto_resultados.insert(tk.END, "\n")
            
            if resultado['columnas_eliminadas_por_archivo']:
                self.texto_resultados.insert(tk.END, f"🚫 COLUMNAS ELIMINADAS:\n")
                for archivo, columnas in resultado['columnas_eliminadas_por_archivo'].items():
                    if columnas:
                        self.texto_resultados.insert(tk.END, f"   • {archivo}: {', '.join(columnas)}\n")
                self.texto_resultados.insert(tk.END, "\n")
            
            if resultado['duplicados_eliminados'] > 0:
                self.texto_resultados.insert(tk.END, f"🔄 DUPLICADOS ELIMINADOS: {resultado['duplicados_eliminados']}\n\n")
            
            guardado = resultado['guardado']
            self.texto_resultados.insert(tk.END, f"💾 ARCHIVO GUARDADO:\n")
            self.texto_resultados.insert(tk.END, f"   • Nombre: {guardado['nombre_archivo']}\n")
            self.texto_resultados.insert(tk.END, f"   • Ubicación: {guardado['ruta_archivo']}\n")
            self.texto_resultados.insert(tk.END, f"   • Registros: {guardado['registros']:,}\n")
            self.texto_resultados.insert(tk.END, f"   • Columnas: {guardado['columnas']}\n\n")
            
            if resultado['archivos_con_errores']:
                self.texto_resultados.insert(tk.END, f"⚠️ ARCHIVOS CON ERRORES:\n")
                for error in resultado['archivos_con_errores']:
                    self.texto_resultados.insert(tk.END, f"   • {error}\n")
                self.texto_resultados.insert(tk.END, "\n")
            
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
        for widget in self.frame_estadisticas.winfo_children():
            widget.destroy()
        
        modo = self.modo_columnas_var.get()
        if modo == "incluir_manual":
            detalle = f"Columnas a incluir (manual): {len(self.columnas_a_incluir)}"
        elif modo == "incluir_lista":
            txt = (self.entry_incluir_lista.get() or "").strip()
            cnt = len([c for c in txt.split(",") if c.strip()])
            detalle = f"Columnas a incluir (lista): {cnt}"
        else:
            detalle = f"Columnas a ignorar: {len(self.columnas_a_ignorar)}"

        ttk.Label(
            self.frame_estadisticas, 
            text=(f"Archivos seleccionados: {len(self.archivos_seleccionados)} | "
                  f"Modo: {modo} | {detalle}"),
            font=("Arial", 9, "bold")
        ).pack(anchor=tk.W)
    
    def limpiar_todo(self):
        """Limpia toda la interfaz."""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres limpiar todo?"):
            self.limpiar_lista_archivos()
            self.limpiar_columnas_ignorar()
            self.limpiar_columnas_incluir()
            self.texto_resultados.delete(1.0, tk.END)
            self.entry_columna1.delete(0, tk.END)
            self.entry_columna1.insert(0, "Archivo_Origen")
            self.entry_columna2.delete(0, tk.END)
            self.entry_columna2.insert(0, "Fecha_Procesamiento")
            self.entry_columnas_ignorar.delete(0, tk.END)
            self.entry_columnas_ignorar.insert(0, "Ejemplo: Telefono, Email, ID_interno")
            if hasattr(self, "entry_incluir_lista"):
                self.entry_incluir_lista.delete(0, tk.END)
            self.modo_columnas_var.set("ignorar")
            self._actualizar_modo_columnas()
            self.eliminar_duplicados_var.set(False)
            self.actualizar_estadisticas()
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.actualizar_estadisticas()
        self.root.mainloop()

    # ========= Helpers de UI y detección de columnas =========
    def _cargar_columnas_disponibles(self):
        """Carga en UI la unión de columnas de todos los archivos seleccionados."""
        self.columnas_disponibles = self._descubrir_union_columnas(self.archivos_seleccionados)
        if hasattr(self, "lista_columnas_disponibles"):
            self.lista_columnas_disponibles.delete(0, tk.END)
            for c in self.columnas_disponibles:
                self.lista_columnas_disponibles.insert(tk.END, c)

    def _descubrir_union_columnas(self, archivos: List[str]) -> List[str]:
        cols = set()
        for ruta in archivos:
            try:
                low = ruta.lower()
                if low.endswith(".csv"):
                    df = pd.read_csv(ruta, nrows=0, encoding="utf-8", engine="python")
                elif low.endswith(".xlsx"):
                    df = pd.read_excel(ruta, nrows=0, engine="openpyxl")
                elif low.endswith(".xls"):
                    df = pd.read_excel(ruta, nrows=0, engine="xlrd")
                else:
                    continue
                cols.update(map(str, df.columns))
            except Exception as e:
                logger.warning(f"No se pudieron leer encabezados de {os.path.basename(ruta)}: {e}")
        return sorted(cols)

    def _actualizar_modo_columnas(self):
        """Muestra/oculta secciones según el modo seleccionado."""
        modo = self.modo_columnas_var.get()
        # Asegurar que las secciones existen antes de manipular
        for f in ("frame_incluir_manual", "frame_incluir_lista", "frame_ignorar"):
            if hasattr(self, f):
                getattr(self, f).grid_remove()

        if modo == "incluir_manual" and hasattr(self, "frame_incluir_manual"):
            self.frame_incluir_manual.grid()
        elif modo == "incluir_lista" and hasattr(self, "frame_incluir_lista"):
            self.frame_incluir_lista.grid()
        elif modo == "ignorar" and hasattr(self, "frame_ignorar"):
            self.frame_ignorar.grid()

        self.actualizar_estadisticas()


# Importar os para uso en el módulo
import os
