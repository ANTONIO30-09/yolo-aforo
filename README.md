# YOLO Aforo: Sistema de Monitoreo de Aforo en Tiempo Real

Pipeline de minería de datos que detecta personas por webcam usando **YOLOv8**, registra los datos por día, los limpia con un **reporte de calidad** y genera un **dashboard unificado** para analizar la afluencia.

---

## Arquitectura del Proyecto

El backend está dividido en **módulos independientes** para garantizar escalabilidad y mantenibilidad:

1.  **Colecta e Ingesta** (`main.py` + `detector.py` + `data_logger.py`)
    *   Detecta objetos con YOLOv8n (traducidos al español).
    *   Guarda **solo personas** en un archivo CSV distinto por cada día (ej. `dataset_crudo_Jueves_2026-11-12.csv`).
    *   Registra la hora exacta en formato `HH:MM` (sin segundos).
2.  **Transformación y Limpieza** (`transformer.py` + `transform.py`)
    *   Lee **todos** los archivos diarios y los unifica.
    *   Filtra falsos positivos (perros, celulares, etc.).
    *   **Elimina duplicados** (misma persona detectada varias veces en el mismo minuto).
    *   Genera un **reporte de calidad** (nulos, no-persona, duplicados eliminados).
    *   Enriquece con `dia` de la semana y `bloque_horario` (Mañana / Vespertina).
3.  **Visualización y Dashboard** (`dashboard.py` + `graficar_dias.py` + `graficar_tendencia.py`)
    *   Genera un **Dashboard unificado** con:
        *   Gráfico de **barras** (aforo total por día de la semana).
        *   Gráfico de **escalones** (tendencia acumulada por hora).
    *   Incluye línea de **promedio** en ambos gráficos.

---

## Estructura de Archivos

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
    +-- generar_notebook_completo.py # Genera el cuaderno Hito 4
    +-- Hito4_Proyecto_YOLO_Aforo_COMPLETO.ipynb # Cuaderno de entrega final
    +-- requirements.txt
    +-- .gitignore

---

## Requisitos e Instalación

    # 1. Crear y activar entorno virtual
    python3 -m venv venv
    source venv/bin/activate

    # 2. Instalar dependencias
    pip install -r requirements.txt

*La primera ejecución de `main.py` descargará automáticamente el modelo `yolov8n.pt` (~6 MB).*

---

## Uso (Paso a Paso)

### 1. Capturar datos desde la webcam
    python main.py
*   Muestra el video con las detecciones en español (ej. "persona", "celular").
*   Presiona **`q`** en la ventana de video (o `Ctrl+C` en terminal) para detener.
*   Genera archivos como `data/dataset_crudo_Lunes_2026-11-12.csv`.

### 2. Limpiar y transformar los datos
    python transform.py
*   Lee todos los archivos diarios.
*   Imprime un **reporte de calidad** (cuántos nulos, no-persona y duplicados se eliminaron).
*   Genera `data/dataset_limpio.csv`.

### 3. Generar el Dashboard
    python dashboard.py
*   Crea `data/dashboard_aforo.png` con los dos gráficos unificados.

### 4. Abrir el Cuaderno de Entrega
    jupyter notebook Hito4_Proyecto_YOLO_Aforo_COMPLETO.ipynb
*   Contiene todo el código fuente, explicaciones y resultados renderizados.

---

## Configuración (`config.py`)

Todos los parámetros ajustables están centralizados en el archivo `config.py`:

| Parámetro | Descripción |
| :--- | :--- |
| `VIDEO_SOURCE` | Índice de la webcam (0, 1, 2...) o ruta a un `.mp4`. |
| `MODEL_PATH` | Ruta del modelo YOLO (por defecto `yolov8n.pt`). |
| `CONFIDENCE_THRESHOLD` | Confianza mínima para aceptar una detección. |
| `SAMPLING_INTERVAL_SECONDS` | Segundos entre cada registro. |
| `MORNING_RANGE` / `AFTERNOON_RANGE` | Rangos horarios de cada jornada. |
| `CLASS_TRANSLATIONS` | Diccionario de traducción de clases al español. |

---

## Ejemplos de Datasets

### Dataset crudo (un archivo por día)

    dia_semana,fecha,hora,clase_objeto
    Jueves,2026-11-12,11:46,persona
    Jueves,2026-11-12,11:46,celular
    Jueves,2026-11-12,11:49,persona

### Dataset limpio (`dataset_limpio.csv`)

    fecha,dia,hora,clase_objeto,bloque_horario
    2026-11-12,Jueves,11:46,persona,Mañana
    2026-11-12,Jueves,11:49,persona,Mañana

---

## Notas

*   El proyecto corre sobre **CPU** usando `yolov8n.pt` (el modelo más liviano de la familia), pensado para hardware limitado.
*   Los datasets generados (`data/`) y los modelos descargados (`*.pt`) **no se versionan** (ver `.gitignore`).
*   Desarrollado para el curso **MDA-611 Minería de Datos**.
