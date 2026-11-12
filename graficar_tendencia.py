"""
graficar_tendencia.py
---------------------
Genera un gráfico de líneas (tendencia) con línea de promedio.
"""
import pandas as pd
import matplotlib.pyplot as plt
import config

def generar_grafico():
    print("[INFO] Leyendo dataset limpio...")
    df = pd.read_csv(config.CLEAN_DATASET_PATH)
    
    df['hora_minuto'] = df['hora'].str.slice(0, 5)
    conteo = df.groupby('hora_minuto').size().reset_index(name='cantidad_personas')
    
    # Calcular el promedio
    promedio = conteo['cantidad_personas'].mean()
    
    plt.figure(figsize=(12, 6))
    plt.plot(conteo['hora_minuto'], conteo['cantidad_personas'], 
             marker='o', linestyle='-', color='#4A55A2', linewidth=2, label='Aforo por minuto')
    
    plt.fill_between(conteo['hora_minuto'], conteo['cantidad_personas'], 
                     color='#4A55A2', alpha=0.3)
    
    # Línea de promedio (Lo que tiene tu compañero)
    plt.axhline(y=promedio, color='red', linestyle='--', linewidth=1.5, label=f'Promedio: {promedio:.1f}')
    
    plt.title('Tendencia de Aforo (Personas por Minuto)', fontsize=14)
    plt.xlabel('Hora (HH:MM)', fontsize=12)
    plt.ylabel('Cantidad de Personas', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    ruta_salida = 'data/grafico_tendencia.png'
    plt.savefig(ruta_salida, dpi=150)
    print(f"[INFO] Gráfico con promedio guardado en: {ruta_salida}")

if __name__ == "__main__":
    generar_grafico()
