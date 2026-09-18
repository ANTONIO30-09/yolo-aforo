"""
detector.py
-----------
Encapsula la lógica de detección de objetos con YOLO (Ultralytics).
"""

from dataclasses import dataclass
from typing import List

from ultralytics import YOLO
import numpy as np

import config


@dataclass
class Detection:
    class_name: str
    confidence: float


class ObjectDetector:
    def __init__(self, model_path: str = config.MODEL_PATH,
                 confidence_threshold: float = config.CONFIDENCE_THRESHOLD):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, frame: np.ndarray) -> List[Detection]:
        results = self.model(frame, verbose=False)[0]
        detections = []
        for box in results.boxes:
            confidence = float(box.conf[0])
            if confidence < self.confidence_threshold:
                continue
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            detections.append(Detection(class_name=class_name, confidence=confidence))
        return detections

    def annotate(self, frame: np.ndarray):
        results = self.model(frame, verbose=False)[0]
        return results.plot()
