"""
main.py
-------
Punto de entrada del sistema YOLO Aforo - Fase 1: Colecta e Ingesta de Datos.
"""

import time
from datetime import datetime

import cv2

import config
from detector import ObjectDetector
from data_logger import CSVDataLogger


def run() -> None:
    print(f"[INFO] Cargando modelo {config.MODEL_PATH}...")
    detector = ObjectDetector()
    logger = CSVDataLogger()

    print(f"[INFO] Abriendo fuente de video: {config.VIDEO_SOURCE}")
    cap = cv2.VideoCapture(config.VIDEO_SOURCE)

    if not cap.isOpened():
        raise RuntimeError(
            f"No se pudo abrir la fuente de video '{config.VIDEO_SOURCE}'. "
            "Verifica el índice de la webcam en config.py."
        )

    print(f"[INFO] Muestreando cada {config.SAMPLING_INTERVAL_SECONDS}s. "
          "Presiona 'q' en la ventana de video para detener.")

    last_sample_time = 0.0
    total_registros = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[WARN] No se pudo leer el frame. Terminando.")
                break

            now = time.time()

            if now - last_sample_time >= config.SAMPLING_INTERVAL_SECONDS:
                detections = detector.detect(frame)
                personas = [d for d in detections if d.class_name == "person"]

                timestamp = datetime.now()
                filas_escritas = logger.log(detections, timestamp=timestamp)
                total_registros += filas_escritas

                print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                      f"Detecciones: {len(detections)} | Personas: {len(personas)}")

                last_sample_time = now

            if config.SHOW_VIDEO_WINDOW:
                annotated_frame = detector.annotate(frame)
                cv2.imshow("YOLO Aforo - Fase 1", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("[INFO] Detención solicitada por el usuario.")
                    break

    except KeyboardInterrupt:
        print("\n[INFO] Interrumpido por teclado (Ctrl+C).")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"[INFO] Finalizado. Total de registros escritos: {total_registros}")
        print(f"[INFO] Dataset guardado en: {config.RAW_DATASET_PATH.resolve()}")


if __name__ == "__main__":
    run()
