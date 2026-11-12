"""
data_logger.py
--------------
Maneja la escritura del dataset crudo a disco (CSV).
Genera un archivo dinámico por cada día de la semana.
"""
import csv
from datetime import datetime
from pathlib import Path
from typing import List
import config
from detector import Detection

DIAS_SEMANA = {0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves", 4: "Viernes", 5: "Sabado", 6: "Domingo"}

class CSVDataLogger:
    def __init__(self):
        config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def _get_daily_path(self, timestamp: datetime) -> Path:
        dia_str = DIAS_SEMANA[timestamp.weekday()]
        fecha_str = timestamp.strftime("%Y-%m-%d")
        filename = f"dataset_crudo_{dia_str}_{fecha_str}.csv"
        return config.OUTPUT_DIR / filename

    def _ensure_file_exists(self, path: Path) -> None:
        if not path.exists():
            with open(path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(config.CSV_COLUMNS)

    def log(self, detections: List[Detection], timestamp: datetime = None) -> int:
        timestamp = timestamp or datetime.now()
        dia_semana = DIAS_SEMANA[timestamp.weekday()]
        fecha = timestamp.strftime("%Y-%m-%d")
        hora_minuto = timestamp.strftime("%H:%M")
        daily_path = self._get_daily_path(timestamp)
        self._ensure_file_exists(daily_path)
        with open(daily_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for det in detections:
                writer.writerow([dia_semana, fecha, hora_minuto, det.class_name])
        return len(detections)
