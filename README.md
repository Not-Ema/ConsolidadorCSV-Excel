# 🚀 Consolidador Pro v2.0.0

## 📋 Descripción

**Consolidador Pro** es una aplicación avanzada en Python para consolidar múltiples archivos CSV y Excel en un solo archivo con opciones avanzadas de configuración. La aplicación presenta una interfaz gráfica moderna y funcionalidades robustas para el procesamiento de datos.

## ✨ Características Principales

### 🔧 Funcionalidades Core
- **Soporte Multi-formato**: CSV (.csv) y Excel (.xlsx, .xls)
- **Múltiples Columnas a Ignorar**: Especifica varias columnas para eliminar
- **Exportación Dual**: Guarda resultados en CSV y Excel
- **Interfaz Gráfica Moderna**: UI intuitiva con Tkinter
- **Procesamiento Asíncrono**: Operaciones en hilos separados
- **Logging Detallado**: Sistema completo de logs y monitoreo

### 📁 Gestión de Archivos
- **Carpeta Separada**: Archivos generados en directorio `generados/`
- **Nombres Únicos**: Timestamps automáticos para evitar sobrescritura
- **Validación Automática**: Verificación de archivos válidos
- **Manejo de Errores**: Continuación con archivos válidos si hay errores

### 🎛️ Opciones Avanzadas
- **Eliminación de Duplicados**: Opción para limpiar datos duplicados
- **Columnas Personalizables**: Nombres personalizados para columnas agregadas
- **Progreso Detallado**: Monitoreo en tiempo real del procesamiento
- **Estadísticas Completas**: Resúmenes detallados de resultados

## 🏗️ Estructura del Proyecto

```
consolidador_pro/
├── 📁 src/                    # Código fuente
│   ├── __init__.py           # Paquete principal
│   ├── utils.py              # Utilidades y procesamiento de archivos
│   ├── processor.py          # Lógica de consolidación
│   └── ui.py                 # Interfaz gráfica
├── 📁 generados/             # Archivos de salida
├── 📁 examples/              # Archivos de ejemplo
├── 📁 logs/                  # Archivos de log
├── 📁 tests/                 # Pruebas unitarias
├── main.py                   # Punto de entrada
├── config.py                 # Configuración
├── requirements.txt          # Dependencias
└── README.md                 # Documentación
```

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.6 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install pandas openpyxl xlrd
```

### Ejecución
```bash
python main.py
```

## 📖 Guía de Uso

### 1. Selección de Archivos
- Haz clic en **"Seleccionar Archivos CSV/Excel"**
- Elige múltiples archivos (mezcla de CSV y Excel permitida)
- Los archivos aparecerán en la lista de seleccionados

### 2. Configuración de Columnas
- **Nombre Columna 1**: Archivo de origen (por defecto: "Archivo_Origen")
- **Nombre Columna 2**: Fecha de procesamiento (por defecto: "Fecha_Procesamiento")

### 3. Columnas a Ignorar
- Ingresa nombres de columnas separadas por comas
- Ejemplo: `Telefono, Email, ID_interno`
- Haz clic en **"Agregar Columnas"** para confirmar

### 4. Opciones Avanzadas
- ✅ **Eliminar duplicados**: Limpia registros duplicados
- ✅ **Mostrar progreso detallado**: Logs en tiempo real
- 📊 **Formato de salida**: CSV o Excel

### 5. Procesamiento
- Haz clic en **"🚀 Procesar y Consolidar"**
- El programa procesará archivos en segundo plano
- Los resultados se guardarán en `generados/`

## 📊 Ejemplo de Resultado

### Estructura del Archivo Consolidado:
```
Archivo_Origen | Fecha_Procesamiento | ID | Nombre | Apellido | Departamento | Salario | Fecha_Ingreso
ejemplo1.csv   | 2024-01-15 10:30:00 | 1  | Juan   | Pérez    | IT          | 50000   | 2023-01-15
ejemplo2.xlsx  | 2024-01-15 10:30:00 | 5  | Luis   | Rodríguez| Ventas      | 42000   | 2023-05-12
...
```

## 🔧 Configuración Avanzada

### Archivo `config.py`
Contiene todas las configuraciones del programa:
- Nombres por defecto de columnas
- Formatos soportados
- Configuración de logging
- Reglas de validación
- Configuración de exportación

### Personalización
Puedes modificar `config.py` para:
- Cambiar nombres por defecto
- Ajustar límites de procesamiento
- Personalizar colores de interfaz
- Configurar formatos de salida

## 📝 Logging y Monitoreo

### Archivos de Log
- Ubicación: `logs/consolidador.log`
- Nivel: INFO (configurable)
- Rotación automática
- Encoding UTF-8

### Información Registrada
- Proceso de lectura de archivos
- Errores de procesamiento
- Estadísticas de consolidación
- Tiempos de ejecución

## 🧪 Archivos de Ejemplo

La carpeta `examples/` contiene:
- `ejemplo1.csv`, `ejemplo2.csv`, `ejemplo3.csv`
- `ejemplo1.xlsx`, `ejemplo2.xlsx`, `ejemplo3.xlsx`

Cada archivo contiene datos de empleados con las siguientes columnas:
- ID, Nombre, Apellido, Email, Telefono, Departamento, Salario, Fecha_Ingreso

## 🔍 Solución de Problemas

### Errores Comunes

#### "No module named 'pandas'"
```bash
pip install pandas openpyxl
```

#### "Error al leer archivo"
- Verifica que el archivo no esté corrupto
- Asegúrate de que el formato sea soportado (.csv, .xlsx, .xls)
- Revisa permisos de lectura del archivo

#### "Columna no encontrada"
- Verifica el nombre exacto de la columna
- Considera diferencias en mayúsculas/minúsculas
- Revisa que la columna exista en todos los archivos

### Logs de Debug
Para más información, revisa:
- `logs/consolidador.log`
- Consola de la aplicación
- Área de resultados en la interfaz

## 🚀 Características Técnicas

### Rendimiento
- **Procesamiento asíncrono**: No bloquea la interfaz
- **Manejo eficiente de memoria**: Procesamiento por lotes
- **Validación rápida**: Verificación optimizada de archivos

### Compatibilidad
- **Windows**: ✅ Totalmente compatible
- **macOS**: ✅ Compatible
- **Linux**: ✅ Compatible
- **Python**: 3.6+ requerido

### Seguridad
- **Validación de entrada**: Sanitización de datos
- **Manejo de errores**: Continuación segura en caso de fallos
- **Logs seguros**: Sin información sensible

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa tus cambios
4. Agrega pruebas si es necesario
5. Envía un pull request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Soporte

Para soporte técnico o reportar bugs:
- Revisa la sección de solución de problemas
- Consulta los logs de la aplicación
- Crea un issue en el repositorio

## 🔄 Historial de Versiones

### v2.0.0 (Actual)
- ✨ Refactorización completa del código
- 🏗️ Arquitectura modular
- 🎨 Interfaz gráfica mejorada
- 📁 Gestión de archivos en carpetas separadas
- 🔧 Múltiples columnas a ignorar
- 📊 Exportación dual (CSV/Excel)
- 📝 Sistema de logging completo

### v1.0.0
- 🎯 Funcionalidad básica de consolidación
- 📋 Soporte para CSV y Excel
- 🖥️ Interfaz gráfica básica

---

**¡Gracias por usar Consolidador Pro! 🎉**
# ConsolidadorCSV-Excel
