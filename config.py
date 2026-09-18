"""
config.py
---------
Configuración centralizada del proyecto YOLO Aforo.
"""

from pathlib import Path

# --- Fuente de video ---
VIDEO_SOURCE = 0

# --- Modelo YOLO ---
MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5

# --- Frecuencia de muestreo ---
SAMPLING_INTERVAL_SECONDS = 3

# --- Almacenamiento ---
OUTPUT_DIR = Path("data")
RAW_DATASET_PATH = OUTPUT_DIR / "dataset_crudo.csv"
CSV_COLUMNS = ["fecha", "hora", "clase_objeto"]

# --- Visualización ---
SHOW_VIDEO_WINDOW = True

# --- Fase 2: Transformación ---
CLEAN_DATASET_PATH = OUTPUT_DIR / "dataset_limpio.csv"

# Mapeo de clases a conservar y su nombre final (idioma español)
CLASSES_TO_KEEP = {"person": "persona"}

# Rangos de jornada (formato "HH:MM:SS", límites inclusivos)
MORNING_RANGE = ("06:00:00", "13:59:59")
AFTERNOON_RANGE = ("14:00:00", "21:59:59")

# Columnas del dataset limpio (Fase 2)
CLEAN_CSV_COLUMNS = ["fecha", "dia", "hora", "clase_objeto", "bloque_horario"]
