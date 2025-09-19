# 🚀 Inicio Rápido - Consolidador Pro

## ⚡ Instalación Express

### 1. Instalar dependencias
```bash
pip install pandas openpyxl
```

### 2. Ejecutar programa
```bash
python main.py
```

## 🎯 Uso Básico (3 pasos)

### Paso 1: Seleccionar archivos
1. Clic en **"Seleccionar Archivos CSV/Excel"**
2. Elegir archivos (CSV y/o Excel)
3. Ver archivos en la lista

### Paso 2: Configurar (opcional)
- **Columnas a ignorar**: `Telefono, Email` (separadas por comas)
- **Formato salida**: CSV o Excel
- **Eliminar duplicados**: ✅ (opcional)

### Paso 3: Procesar
1. Clic en **"🚀 Procesar y Consolidar"**
2. Esperar procesamiento
3. Archivo guardado en carpeta `generados/`

## 📁 Archivos de Ejemplo

Usa los archivos en `examples/`:
- `ejemplo1.csv`, `ejemplo2.csv`, `ejemplo3.csv`
- `ejemplo1.xlsx`, `ejemplo2.xlsx`, `ejemplo3.xlsx`

## ✅ Resultado Esperado

Archivo consolidado con:
- **2 columnas nuevas al inicio**: Archivo_Origen, Fecha_Procesamiento
- **Sin columnas ignoradas**: Telefono, Email (si las especificaste)
- **Todos los registros**: De todos los archivos seleccionados

## 🔧 Configuración Rápida

### Nombres de columnas por defecto:
- Columna 1: `Archivo_Origen`
- Columna 2: `Fecha_Procesamiento`

### Formatos soportados:
- CSV: `.csv`
- Excel: `.xlsx`, `.xls`

### Ubicación de salida:
- Carpeta: `generados/`
- Nombre: `consolidado_YYYYMMDD_HHMMSS.[csv/xlsx]`

## 🆘 Solución Rápida

### Error: "No module named 'pandas'"
```bash
pip install pandas openpyxl
```

### Error: "No hay archivos seleccionados"
- Selecciona archivos antes de procesar
- Verifica que sean CSV o Excel

### Error: "Columna no encontrada"
- Verifica nombre exacto de columna
- Considera mayúsculas/minúsculas

## 📞 Soporte

- 📖 Documentación completa: `README.md`
- 📝 Logs: `logs/consolidador.log`
- 🐛 Problemas: Revisa logs y consola

---

**¡Listo para consolidar! 🎉**
