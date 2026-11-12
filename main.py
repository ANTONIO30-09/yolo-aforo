"""
main.py
-------
Punto de entrada del sistema YOLO Aforo.
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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente de video '{config.VIDEO_SOURCE}'.")

    print(f"[INFO] Muestreando cada {config.SAMPLING_INTERVAL_SECONDS}s. Presiona 'q' para detener.")

    last_sample_time = 0.0
    total_registros = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()

            if now - last_sample_time >= config.SAMPLING_INTERVAL_SECONDS:
                detections = detector.detect(frame)
                
                # Extraemos los nombres de TODO lo que ve YOLO
                nombres_objetos = [d.class_name for d in detections]
                # Filtramos solo las personas para el aforo
                personas = [d for d in detections if d.class_name == "persona"]

                timestamp = datetime.now()
                filas_escritas = logger.log(personas, timestamp=timestamp)
                total_registros += filas_escritas

                # Mostramos en consola todo lo detectado
                print(f"[{timestamp.strftime('%H:%M:%S')}] YOLO ve: {nombres_objetos} | Aforo guardado: {len(personas)} personas")

                last_sample_time = now

            if config.SHOW_VIDEO_WINDOW:
                annotated_frame = detector.annotate(frame)
                annotated_frame = cv2.resize(annotated_frame, (640, 480))
                cv2.imshow("YOLO Aforo - Fase 1", annotated_frame)
                
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"[INFO] Finalizado. Registros de personas escritos: {total_registros}")

if __name__ == "__main__":
    run()
