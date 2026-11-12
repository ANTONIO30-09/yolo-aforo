"""
transformer.py
--------------
Transforma los datos crudos en un dataset limpio.
Clasifica en bloques: Mañana, Tarde y Noche.
"""
import glob
import pandas as pd
from datetime import datetime
import config

def load_raw_data() -> pd.DataFrame:
    print("[FASE 4] Cargando todos los archivos diarios...")
    archivos = glob.glob(str(config.OUTPUT_DIR / "dataset_crudo_*.csv"))
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos dataset_crudo_*.csv")
    
    dfs = [pd.read_csv(f) for f in archivos]
    df = pd.concat(dfs, ignore_index=True)
    print(f" -> Se leyeron {len(archivos)} archivos. Total de registros crudos: {len(df)}")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("[FASE 4] Iniciando limpieza de datos...")
    registros_iniciales = len(df)
    
    df = df.dropna(subset=['fecha', 'hora', 'clase_objeto'])
    nulos_eliminados = registros_iniciales - len(df)
    
    df = df[df['clase_objeto'] == 'person'].copy()
    df['clase_objeto'] = 'persona'
    no_personas_eliminadas = registros_iniciales - nulos_eliminados - len(df)
    
    df = df.drop_duplicates(subset=['fecha', 'hora', 'clase_objeto'])
    duplicados_eliminados = (registros_iniciales - nulos_eliminados - no_personas_eliminadas) - len(df)
    
    print(" --- REPORTE DE LIMPIEZA ---")
    print(f" -> Registros con nulos eliminados: {nulos_eliminados}")
    print(f" -> Registros no-persona eliminados: {no_personas_eliminadas}")
    print(f" -> Registros duplicados eliminados: {duplicados_eliminados}")
    print(f" -> Total de registros limpios conservados: {len(df)}")
    
    return df

def enrich_time_block(df: pd.DataFrame) -> pd.DataFrame:
    print("[FASE 4] Enriqueciendo datos (Mañana, Tarde, Noche)...")
    def obtener_bloque(hora_str):
        try:
            h = datetime.strptime(hora_str, "%H:%M").time()
            
            manana_inicio = datetime.strptime(config.MORNING_RANGE[0], "%H:%M:%S").time()
            manana_fin = datetime.strptime(config.MORNING_RANGE[1], "%H:%M:%S").time()
            
            tarde_inicio = datetime.strptime(config.AFTERNOON_RANGE[0], "%H:%M:%S").time()
            tarde_fin = datetime.strptime(config.AFTERNOON_RANGE[1], "%H:%M:%S").time()
            
            if manana_inicio <= h <= manana_fin:
                return "Mañana"
            elif tarde_inicio <= h <= tarde_fin:
                return "Tarde"
            else:
                return "Noche"
        except:
            return "Desconocido"
    
    df['bloque_horario'] = df['hora'].apply(obtener_bloque)
    return df

def transform() -> pd.DataFrame:
    df = load_raw_data()
    df = clean_data(df)
    df = enrich_time_block(df)
    
    if 'dia_semana' in df.columns:
        df = df.rename(columns={'dia_semana': 'dia'})
        
    columnas = ["fecha", "dia", "hora", "clase_objeto", "bloque_horario"]
    return df[columnas]

def save_clean_data(df: pd.DataFrame, path=config.CLEAN_DATASET_PATH) -> None:
    df.to_csv(path, index=False)
    print(f"[FASE 4] Dataset limpio guardado exitosamente en: {path}")
