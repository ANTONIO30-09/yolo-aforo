"""
transform.py
------------
Script de ejecución para la Fase 2.
Llama a las funciones del nuevo transformer.py que lee los archivos diarios.
"""
from transformer import transform, save_clean_data
import config

def run() -> None:
    print("[INFO] Iniciando Fase 2: Transformación de datos...")
    
    # Ejecuta la transformación (lee todos los dataset_crudo_*.csv)
    df_limpio = transform()
    
    # Guarda el resultado en dataset_limpio.csv
    save_clean_data(df_limpio, config.CLEAN_DATASET_PATH)
    
    print(f"[INFO] Transformación completada. Total de registros limpios: {len(df_limpio)}")

if __name__ == "__main__":
    run()
