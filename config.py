"""
config.py
---------
Configuración centralizada del proyecto YOLO Aforo.
"""
from pathlib import Path

VIDEO_SOURCE = 0
MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.3
SAMPLING_INTERVAL_SECONDS = 3
OUTPUT_DIR = Path("data")
CSV_COLUMNS = ["dia_semana", "fecha", "hora", "clase_objeto"]
SHOW_VIDEO_WINDOW = True

CLEAN_DATASET_PATH = OUTPUT_DIR / "dataset_limpio.csv"
CLASSES_TO_KEEP = {"person": "persona"}

# Nuevos rangos de jornada (Mañana, Tarde y Noche)
MORNING_RANGE = ("06:00:00", "11:59:59")
AFTERNOON_RANGE = ("12:00:00", "18:59:59")
NIGHT_RANGE = ("19:00:00", "05:59:59")

CLEAN_CSV_COLUMNS = ["fecha", "dia", "hora", "clase_objeto", "bloque_horario"]

CLASS_TRANSLATIONS = {
    "person": "persona",
    "dog": "perro",
    "cat": "gato",
    "car": "coche",
    "motorcycle": "moto",
    "bicycle": "bicicleta",
    "cell phone": "celular",
    "chair": "silla",
    "bottle": "botella",
    "cup": "taza",
    "laptop": "portatil",
    "book": "libro",
    "backpack": "mochila"
}
