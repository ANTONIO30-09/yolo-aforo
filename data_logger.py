"""
data_logger.py
--------------
Maneja la escritura del dataset crudo a disco (CSV).
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

import config
from detector import Detection


class CSVDataLogger:
    def __init__(self, output_path: Path = config.RAW_DATASET_PATH):
        self.output_path = output_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.output_path.exists():
            with open(self.output_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(config.CSV_COLUMNS)

    def log(self, detections: List[Detection], timestamp: datetime = None) -> int:
        timestamp = timestamp or datetime.now()
        fecha = timestamp.strftime("%Y-%m-%d")
        hora = timestamp.strftime("%H:%M:%S")

        with open(self.output_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for det in detections:
                writer.writerow([fecha, hora, det.class_name])

        return len(detections)
