"""
transformer.py
---------------
Fase 2: Ingeniería y Transformación de Datos.

Contiene la lógica pura de limpieza y enriquecimiento, separada del
script orquestador (transform.py) para poder testearla o reutilizarla
independientemente (ej. en un notebook de análisis).
"""

from datetime import datetime
from typing import Dict, Tuple

import pandas as pd

import config

# Mapeo de número de día (datetime.weekday(): 0=Lunes) a nombre en español.
# Se usa un mapeo manual en vez de strftime("%A") para no depender de la
# configuración regional (locale) del sistema operativo.
DIAS_ES = {
    0: "Lunes",
    1: "Martes",
    2: "Miercoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sabado",
    6: "Domingo",
}


def load_raw_data(path=config.RAW_DATASET_PATH) -> pd.DataFrame:
    """Carga el dataset crudo desde CSV."""
    return pd.read_csv(path)


def filter_and_rename_classes(df: pd.DataFrame,
                               classes_to_keep: Dict[str, str] = config.CLASSES_TO_KEEP
                               ) -> pd.DataFrame:
    """
    Conserva unicamente las filas cuya clase_objeto esta en classes_to_keep
    y renombra la clase segun el mapeo (ej. 'person' -> 'persona').
    """
    df = df[df["clase_objeto"].isin(classes_to_keep.keys())].copy()
    df["clase_objeto"] = df["clase_objeto"].map(classes_to_keep)
    return df


def enrich_day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega la columna 'dia' (dia de la semana en espanol) a partir de 'fecha'."""
    fechas = pd.to_datetime(df["fecha"], format="%Y-%m-%d")
    df["dia"] = fechas.dt.weekday.map(DIAS_ES)
    return df


def _time_in_range(hora_str: str, rango: Tuple[str, str]) -> bool:
    """Verifica si una hora (HH:MM:SS) cae dentro de un rango inclusivo."""
    hora = datetime.strptime(hora_str, "%H:%M:%S").time()
    inicio = datetime.strptime(rango[0], "%H:%M:%S").time()
    fin = datetime.strptime(rango[1], "%H:%M:%S").time()
    return inicio <= hora <= fin


def enrich_time_block(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega la columna 'bloque_horario' clasificando cada registro como
    'Matinal' o 'Vespertina' segun config.MORNING_RANGE / AFTERNOON_RANGE.
    Registros fuera de ambos rangos se marcan como 'Fuera de horario'.
    """
    def classify(hora_str: str) -> str:
        if _time_in_range(hora_str, config.MORNING_RANGE):
            return "Matinal"
        if _time_in_range(hora_str, config.AFTERNOON_RANGE):
            return "Vespertina"
        return "Fuera de horario"

    df["bloque_horario"] = df["hora"].apply(classify)
    return df


def transform(raw_path=config.RAW_DATASET_PATH) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de transformacion:
    carga -> filtrado/renombrado -> enriquecimiento dia -> enriquecimiento bloque.
    """
    df = load_raw_data(raw_path)
    df = filter_and_rename_classes(df)
    df = enrich_day_of_week(df)
    df = enrich_time_block(df)
    return df[config.CLEAN_CSV_COLUMNS]


def save_clean_data(df: pd.DataFrame, path=config.CLEAN_DATASET_PATH) -> None:
    """Guarda el dataset transformado en CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
