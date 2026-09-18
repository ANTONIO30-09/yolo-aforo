"""
transform.py
------------
Punto de entrada de la Fase 2: Ingenieria y Transformacion de Datos.

Lee el dataset crudo, aplica limpieza y enriquecimiento, y genera
un nuevo archivo dataset_limpio.csv (el crudo queda intacto).

Ejecucion:
    python transform.py
"""

import config
from transformer import transform, save_clean_data


def run() -> None:
    print(f"[INFO] Leyendo dataset crudo: {config.RAW_DATASET_PATH}")
    df_clean = transform()

    print(f"[INFO] Registros tras filtrado (solo 'persona'): {len(df_clean)}")
    print("[INFO] Distribucion por bloque horario:")
    print(df_clean["bloque_horario"].value_counts().to_string())

    save_clean_data(df_clean)
    print(f"[INFO] Dataset limpio guardado en: {config.CLEAN_DATASET_PATH.resolve()}")


if __name__ == "__main__":
    run()
