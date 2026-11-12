import nbformat as nbf
import os

print("[INFO] Generando el Jupyter Notebook estructurado...")

# Crear un nuevo notebook vacío
nb = nbf.v4.new_notebook()

# Función auxiliar para añadir celdas de Markdown
def md(texto):
    nb.cells.append(nbf.v4.new_markdown_cell(texto))

# Función auxiliar para añadir celdas de Código
def code(texto):
    nb.cells.append(nbf.v4.new_code_cell(texto))

# ==========================================
# ESTRUCTURA DEL NOTEBOOK (PUNTO POR PUNTO)
# ==========================================

md("""# PROYECTO YOLO AFORO - MINERÍA DE DATOS (MDA-611)
**Autor:** Antonio
**Hito 4: Análisis y Visualización**

Este cuaderno documenta todo el ciclo de vida del proyecto de minería de datos para el aforo de personas, desde la configuración inicial hasta la generación del Dashboard final.
""")

# --- PUNTO 1 ---
md("""## Punto 1: Configuración e Instalación del Entorno

### 1.1 Instalación de Dependencias
Instalamos las librerías necesarias para la detección, transformación y visualización.""")
code("!pip install ultralytics opencv-python pandas matplotlib nbformat -q")

md("""### 1.2 Configuración Centralizada (`config.py`)
Se definen las rutas, el modelo a utilizar, los umbrales de confianza y el diccionario de traducción al español para mantener un backend modular.""")
code("""# Mostramos el contenido de config.py
with open('config.py', 'r') as f:
    print(f.read())""")

# --- PUNTO 2 ---
md("""## Punto 2: Fase 1 - Detección de Objetos con YOLO

### 2.1 Lógica de Detección (`detector.py`)
Aquí encapsulamos YOLOv8. Destaca nuestra implementación para **traducir las clases al español** en tiempo real y el uso de tracking para mantener el ID de las personas.""")

code("""# Mostramos el código del detector
with open('detector.py', 'r') as f:
    print(f.read())""")

# --- PUNTO 3 ---
md("""## Punto 3: Fase 2 - Colecta de Datos (Ingesta)

### 3.1 Lógica de Guardado Diario (`data_logger.py`)
A diferencia de un CSV único, nuestro backend crea un archivo distinto por cada día (ej. `dataset_crudo_Jueves_2026-11-12.csv`), guardando la hora exacta sin segundos para evitar ruido.""")

code("""with open('data_logger.py', 'r') as f:
    print(f.read())""")

md("""### 3.2 Ejecución de la Colecta (`main.py`)
Este script abre la cámara, detecta personas, y guarda los registros. (Nota: En un entorno de Notebook, ejecutar este script abrirá una ventana de video. Si no hay cámara, se pueden usar los CSVs ya generados).""")
code("""# Para ejecutar la cámara (Descomentar si se tiene webcam)
# %run main.py

# En su defecto, verificamos los archivos generados
import glob
archivos = glob.glob('data/dataset_crudo_*.csv')
print(f"Archivos crudos encontrados: {len(archivos)}")
for a in archivos:
    print(f" - {a}")""")

# --- PUNTO 4 ---
md("""## Punto 4: Fase 4 - Transformación y Limpieza de Datos (DATA QUALITY)

### 4.1 Limpieza y Reporte de Calidad (`transformer.py`)
Este es el núcleo de la ingeniería de datos. El script lee todos los CSVs diarios, filtra falsos positivos (perros, celulares), **elimina duplicados exactos** para no inflar el aforo, y genera un reporte de calidad.""")

code("""with open('transformer.py', 'r') as f:
    print(f.read())""")

md("""### 4.2 Ejecutando la Transformación
Corremos el pipeline para generar el `dataset_limpio.csv`.""")
code("""%run transform.py

import pandas as pd
df_limpio = pd.read_csv('data/dataset_limpio.csv')
print("\\n--- Muestra del Dataset Limpio ---")
display(df_limpio.head(10))""")

# --- PUNTO 5 ---
md("""## Punto 5: Fase 6 - Visualización de Resultados y Dashboard

### 5.1 Generación de Gráficos
Creamos un dashboard unificado que muestra el aforo total por día (barras) y la tendencia acumulada por hora (escalones).""")

code("""with open('dashboard.py', 'r') as f:
    print(f.read())""")

md("""### 5.2 Ejecutando el Dashboard
Generamos la imagen final.""")
code("""%run dashboard.py

# Mostrar la imagen generada en el Notebook
from IPython.display import Image, display
display(Image(filename='data/dashboard_aforo.png'))""")

# --- GUARDAR EL NOTEBOOK ---
nombre_archivo = 'Hito4_Proyecto_YOLO_Aforo_FINAL.ipynb'
with open(nombre_archivo, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"[ÉXITO] Notebook generado correctamente: {nombre_archivo}")
