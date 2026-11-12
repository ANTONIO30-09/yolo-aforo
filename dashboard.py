"""
dashboard.py
------------
Genera un Dashboard unificado con el Aforo Total por Día (Barras)
y la Tendencia Acumulada por Hora (Escalones).
Lee el dataset_limpio.csv real del proyecto.
"""
import pandas as pd
import matplotlib.pyplot as plt
import config

def generar_dashboard():
    print("[INFO] Leyendo dataset limpio para el Dashboard...")
    df = pd.read_csv(config.CLEAN_DATASET_PATH)
    
    if df.empty:
        print("[WARN] El dataset está vacío. Ejecuta main.py y transform.py primero.")
        return

    # ==========================================
    # PREPARACIÓN DE DATOS
    # ==========================================
    # 1. Totales por Día (Para el gráfico de barras)
    conteo_dias = df.groupby('dia').size().reset_index(name='total')
    orden_dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    dias_completos = pd.DataFrame({'dia': orden_dias})
    conteo_dias = dias_completos.merge(conteo_dias, on='dia', how='left').fillna(0)
    promedio = conteo_dias['total'].mean()

    # ==========================================
    # CREANDO EL DASHBOARD
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Dashboard de Aforo - Análisis de Datos', fontsize=16, fontweight='bold')

    # --- GRÁFICO 1: BARRAS POR DÍA ---
    barras = ax1.bar(conteo_dias['dia'], conteo_dias['total'], color='#4A55A2', alpha=0.8)
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:
            ax1.text(barra.get_x() + barra.get_width()/2., altura, f'{int(altura)}', 
                     ha='center', va='bottom', fontweight='bold')

    ax1.axhline(y=promedio, color='red', linestyle='--', label=f'Promedio: {promedio:.1f}')
    ax1.set_title('Aforo Total por Día de la Semana')
    ax1.set_ylabel('Total Personas Detectadas')
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # --- GRÁFICO 2: TENDENCIA ACUMULADA POR HORA ---
    # Agrupamos por fecha y hora para sacar el acumulado real
    colores = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']
    
    for i, fecha in enumerate(df['fecha'].unique()):
        df_dia = df[df['fecha'] == fecha]
        # Contamos cuántas personas hay en cada minuto exacto de ese día
        conteo_hora = df_dia.groupby('hora').size().reset_index(name='cantidad')
        # Calculamos el acumulado
        conteo_hora['acumulado'] = conteo_hora['cantidad'].cumsum()
        
        nombre_dia = df_dia['dia'].iloc[0]
        color = colores[i % len(colores)]
        
        # drawstyle='steps-post' crea el efecto de escalón
        ax2.plot(conteo_hora['hora'], conteo_hora['acumulado'], marker='o', 
                 label=f"{nombre_dia} ({fecha})", color=color, linewidth=2, drawstyle='steps-post')

    ax2.set_title('Tendencia de Aforo Acumulado por Hora')
    ax2.set_xlabel('Hora del día (HH:MM)')
    ax2.set_ylabel('Personas Acumuladas')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    ruta_salida = 'data/dashboard_aforo.png'
    plt.savefig(ruta_salida, dpi=150)
    print(f"[INFO] Dashboard guardado exitosamente en: {ruta_salida}")

if __name__ == "__main__":
    generar_dashboard()
