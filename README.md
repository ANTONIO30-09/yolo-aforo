# YOLO Aforo: Sistema de Monitoreo de Aforo en Tiempo Real

Pipeline de minería de datos que detecta personas por webcam usando **YOLOv8**, registra los datos por día, los limpia con un **reporte de calidad** y genera un **dashboard unificado** para analizar la afluencia.

## Arquitectura del Proyecto

El backend está dividido en módulos independientes para garantizar escalabilidad y mantenibilidad:

1. Colecta e Ingesta (main.py + detector.py + data_logger.py)
   - Detecta objetos con YOLOv8n (traducidos al español).
   - Guarda solo personas en un archivo CSV distinto por cada día (ej. dataset_crudo_Jueves_2026-11-12.csv).
   - Registra la hora exacta en formato HH:MM (sin segundos).

2. Transformación y Limpieza (transformer.py + transform.py)
   - Lee todos los archivos diarios y los unifica.
   - Filtra falsos positivos (perros, celulares, etc.).
   - Elimina duplicados (misma persona detectada varias veces en el mismo minuto).
   - Genera un reporte de calidad (nulos, no-persona, duplicados eliminados).
   - Enriquece con día de la semana y bloque_horario (Mañana / Vespertina).

3. Visualización y Dashboard (dashboard.py + graficar_dias.py + graficar_tendencia.py)
   - Genera un Dashboard unificado con:
     * Gráfico de barras (aforo total por día de la semana).
     * Gráfico de escalones (tendencia acumulada por hora).
   - Incluye línea de promedio en ambos gráficos.

## Estructura del Proyecto y Ejecución

El flujo del proyecto se ejecuta así:

    yolo_aforo/
    +-- config.py                 # Configuración centralizada (rutas, modelo, traducciones)
    +-- detector.py               # Wrapper de YOLO + traducción al español + tracking
    +-- data_logger.py            # Escritura de CSV diarios (particionamiento por fecha)
    +-- main.py                   # Fase 1: captura + detección + logging
    +-- transformer.py            # Fase 2: lógica de limpieza + reporte de calidad
    +-- transform.py              # Fase 2: script orquestador
    +-- dashboard.py              # Fase 3: genera el dashboard unificado
    +-- graficar_dias.py          # Fase 3: gráfico de barras por día
    +-- graficar_tendencia.py     # Fase 3: gráfico de tendencia por minuto
    +-- Hito4_Proyecto_YOLO_Aforo_COMPLETO.ipynb # Cuaderno de entrega final
    +-- requirements.txt
    +-- .gitignore

COMANDOS DE EJECUCIÓN (PASO A PASO):

1. Crear y activar entorno virtual
   python3 -m venv venv
   source venv/bin/activate

2. Instalar dependencias
   pip install -r requirements.txt

3. Capturar datos desde la webcam (Presiona 'q' para detener)
   python main.py

4. Limpiar y transformar los datos
   python transform.py

5. Generar el Dashboard
   python dashboard.py

6. Abrir el Cuaderno de Entrega
   jupyter notebook Hito4_Proyecto_YOLO_Aforo_COMPLETO.ipynb

## Ejemplos de Datasets

Dataset crudo (un archivo por día):
dia_semana,fecha,hora,clase_objeto
Jueves,2026-11-12,11:46,persona

Dataset limpio (dataset_limpio.csv):
fecha,dia,hora,clase_objeto,bloque_horario
2026-11-12,Jueves,11:46,persona,Mañana

## Notas
- El proyecto corre sobre CPU usando yolov8n.pt (el modelo más liviano de la familia), pensado para hardware limitado.
- Los datasets generados (data/) y los modelos descargados (*.pt) no se versionan (ver .gitignore).
- Desarrollado para el curso MDA-611 Minería de Datos.
