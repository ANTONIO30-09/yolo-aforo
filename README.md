# YOLO Aforo

Sistema de monitoreo de aforo en tiempo real con YOLOv8 y OpenCV: detecta
personas por webcam, transforma los datos por jornada horaria y genera
metricas para optimizar la asignacion de personal en recintos comerciales
(restaurantes, cines, bancos, supermercados).

## Arquitectura del proyecto

El pipeline esta dividido en 3 fases independientes y validadas:

1. **Colecta e Ingesta** (`main.py`): captura video de la webcam, detecta
   objetos con YOLOv8n y registra cada deteccion (fecha, hora, clase) en
   `data/dataset_crudo.csv`.
2. **Transformacion** (`transform.py`): filtra el dataset conservando solo
   la clase `persona`, y enriquece con `dia` de la semana y `bloque_horario`
   (Matinal / Vespertina). Genera `data/dataset_limpio.csv`.
3. **Analisis** (`analisis_fase3.ipynb`): calcula metricas (conteo total,
   promedio y pico por bloque horario) y genera un grafico comparativo.

## Estructura de archivos
yolo_aforo/
├── config.py # Configuracion centralizada (parametros ajustables)
├── detector.py # Wrapper de YOLO para deteccion de objetos
├── data_logger.py # Escritura del dataset crudo a CSV
├── main.py # Fase 1: captura + deteccion + logging
├── transformer.py # Fase 2: logica de limpieza y enriquecimiento
├── transform.py # Fase 2: script orquestador
├── build_notebook.py # Genera el notebook de la Fase 3
├── analisis_fase3.ipynb # Fase 3: notebook de analisis y metricas
└── requirements.txt

## Instalacion

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

La primera ejecucion de main.py descargara automaticamente los pesos yolov8n.pt (~6MB).

## Uso

Fase 1 - Capturar datos desde la webcam:

    python main.py

Presiona 'q' en la ventana de video (o Ctrl+C en terminal) para detener.
Genera data/dataset_crudo.csv.

Fase 2 - Limpiar y transformar los datos:

    python transform.py

Genera data/dataset_limpio.csv (el dataset crudo queda intacto).

Fase 3 - Analizar metricas (regenera el notebook si se modifico build_notebook.py):

    python build_notebook.py
    jupyter lab analisis_fase3.ipynb

Dentro de Jupyter Lab: Run -> Run All Cells.

## Configuracion

Todos los parametros ajustables estan centralizados en config.py:

- VIDEO_SOURCE: indice de la webcam (0, 1, 2...) o ruta a un .mp4
- CONFIDENCE_THRESHOLD: confianza minima para aceptar una deteccion
- SAMPLING_INTERVAL_SECONDS: segundos entre cada registro
- MORNING_RANGE / AFTERNOON_RANGE: rangos horarios de cada jornada

## Dataset crudo (ejemplo)

fecha,hora,clase_objeto
2026-09-17,20:45:50,person
2026-09-17,20:46:01,cell phone

## Dataset limpio (ejemplo)

fecha,dia,hora,clase_objeto,bloque_horario
2026-09-17,Jueves,20:45:50,persona,Vespertina

## Notas

- Corre sobre CPU (sin GPU dedicada) usando YOLOv8n, el modelo mas liviano
  de la familia, pensado para hardware limitado.
- Los datasets generados (data/) y el modelo descargado (*.pt) no se
  versionan en este repositorio (ver .gitignore).
- Proyecto desarrollado para el curso MDA-611 Mineria de Datos.
