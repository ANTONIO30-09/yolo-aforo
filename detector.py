"""
detector.py
-----------
Encapsula la lógica de detección de objetos con YOLO.
Dibuja las cajas manualmente para mostrar los nombres en español.
"""
from dataclasses import dataclass
from typing import List
import cv2
from ultralytics import YOLO
import numpy as np
import config

@dataclass
class Detection:
    class_name: str
    confidence: float
    track_id: int = None

class ObjectDetector:
    def __init__(self, model_path: str = config.MODEL_PATH,
                 confidence_threshold: float = config.CONFIDENCE_THRESHOLD):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, frame: np.ndarray) -> List[Detection]:
        results = self.model.track(frame, persist=True, verbose=False)[0]
        detections = []
        
        if results.boxes is None:
            return detections

        for box in results.boxes:
            confidence = float(box.conf[0])
            if confidence < self.confidence_threshold:
                continue
                
            class_id = int(box.cls[0])
            class_name_en = self.model.names[class_id]
            class_name_es = config.CLASS_TRANSLATIONS.get(class_name_en, class_name_en)
            track_id = int(box.id[0]) if box.id is not None else None
            
            detections.append(Detection(
                class_name=class_name_es, 
                confidence=confidence,
                track_id=track_id
            ))
        return detections

    def annotate(self, frame: np.ndarray):
        # En lugar de results.plot(), dibujamos manualmente para traducir
        results = self.model.track(frame, persist=True, verbose=False)[0]
        annotated_frame = frame.copy()
        
        if results.boxes is not None:
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                
                if confidence < self.confidence_threshold:
                    continue
                    
                class_id = int(box.cls[0])
                class_name_en = self.model.names[class_id]
                class_name_es = config.CLASS_TRANSLATIONS.get(class_name_en, class_name_en)
                
                # Dibujar caja verde
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Escribir el texto en español
                label = f"{class_name_es} {confidence:.2f}"
                cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                            
        return annotated_frame
