"""
graficar_dias.py
----------------
Genera un gráfico de barras mostrando el aforo total por cada día de la semana.
"""
import pandas as pd
import matplotlib.pyplot as plt
import config

def generar_grafico_dias():
    print("[INFO] Leyendo dataset limpio...")
    df = pd.read_csv(config.CLEAN_DATASET_PATH)
    
    # Contar cuántas personas hay por día
    conteo_dias = df.groupby('dia').size().reset_index(name='cantidad_personas')
    
    # Definir el orden correcto de los días (para que no se ordene alfabéticamente)
    orden_dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    
    # Asegurarnos de que todos los días aparezcan, incluso si tienen 0 personas
    dias_completos = pd.DataFrame({'dia': orden_dias})
    conteo_dias = dias_completos.merge(conteo_dias, on='dia', how='left').fillna(0)
    
    # Calcular el promedio de aforo diario
    promedio = conteo_dias['cantidad_personas'].mean()
    
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    barras = plt.bar(conteo_dias['dia'], conteo_dias['cantidad_personas'], 
                     color='#4A55A2', alpha=0.8, edgecolor='black')
    
    # Añadir el valor numérico arriba de cada barra
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:
            plt.text(barra.get_x() + barra.get_width()/2., altura, 
                     f'{int(altura)}', ha='center', va='bottom', fontweight='bold')

    # Línea de promedio
    plt.axhline(y=promedio, color='red', linestyle='--', linewidth=1.5, label=f'Promedio: {promedio:.1f}')
    
    plt.title('Aforo Total de Personas por Día de la Semana', fontsize=14)
    plt.xlabel('Día de la Semana', fontsize=12)
    plt.ylabel('Total de Personas Detectadas', fontsize=12)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    ruta_salida = 'data/grafico_dias.png'
    plt.savefig(ruta_salida, dpi=150)
    print(f"[INFO] Gráfico de días guardado en: {ruta_salida}")

if __name__ == "__main__":
    generar_grafico_dias()
