"""
dashboard.py
------------
Dashboard de Aforo - Análisis Integral (2x2).
Soluciona la superposición de días usando desplazamiento horizontal (Jitter).
"""
import pandas as pd
import matplotlib.pyplot as plt
import config

def generar_dashboard():
    print("[INFO] Leyendo dataset limpio...")
    df = pd.read_csv(config.CLEAN_DATASET_PATH)
    
    if df.empty:
        print("[WARN] El dataset está vacío.")
        return

    # Preparar datos generales
    orden_dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    orden_bloques = ['Mañana', 'Tarde', 'Noche']
    df['hora_hh'] = df['hora'].str.slice(0, 2) + ":00"

    # Configurar el lienzo 2x2
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Dashboard de Aforo - Análisis Integral', fontsize=18, fontweight='bold')
    fig.subplots_adjust(hspace=0.5, wspace=0.3)

    # ==========================================
    # GRÁFICO 1 (Arriba Izq): Barras por Día y Bloque
    # ==========================================
    ax1 = axes[0, 0]
    pivot_df = df.groupby(['dia', 'bloque_horario']).size().unstack(fill_value=0)
    for col in orden_bloques:
        if col not in pivot_df.columns: pivot_df[col] = 0
    pivot_df = pivot_df[orden_bloques].reindex(orden_dias, fill_value=0)
    
    pivot_df.plot(kind='bar', ax=ax1, color=['#FFD700', '#FF8C00', '#4A55A2'], edgecolor='black', width=0.7)
    ax1.set_title('Aforo por Día y Bloque Horario')
    ax1.set_xlabel('Día de la Semana')
    ax1.set_ylabel('Total Personas')
    ax1.set_xticklabels(orden_dias, rotation=45)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.legend(title='Bloque')
    for p in ax1.patches:
        if p.get_height() > 0:
            ax1.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

    # ==========================================
    # GRÁFICO 2 (Arriba Der): Pastel por Bloque Horario
    # ==========================================
    ax2 = axes[0, 1]
    conteo_bloques = df.groupby('bloque_horario').size().reindex(orden_bloques, fill_value=0)
    conteo_bloques = conteo_bloques[conteo_bloques > 0]
    
    if not conteo_bloques.empty:
        ax2.pie(conteo_bloques, labels=conteo_bloques.index, autopct='%1.1f%%', 
                colors=['#FFD700', '#FF8C00', '#4A55A2'], startangle=90, textprops={'fontsize': 12})
    ax2.set_title('Distribución Porcentual por Bloque')

    # ==========================================
    # GRÁFICO 3 (Abajo Izq): Barras por Hora
    # ==========================================
    ax3 = axes[1, 0]
    conteo_horas = df.groupby('hora_hh').size().reset_index(name='total')
    ax3.bar(conteo_horas['hora_hh'], conteo_horas['total'], color='#3498DB', edgecolor='black', alpha=0.8)
    ax3.set_title('Aforo Total por Hora del Día')
    ax3.set_xlabel('Hora (HH:00)')
    ax3.set_ylabel('Total Personas')
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    for p in ax3.patches:
        if p.get_height() > 0:
            ax3.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

    # ==========================================
    # GRÁFICO 4 (Abajo Der): Línea Acumulada CON DESPLAZAMIENTO (JITTER)
    # ==========================================
    ax4 = axes[1, 1]
    colores_lineas = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    estilos_linea = ['-', '--', '-.', ':']
    marcadores = ['o', 's', '^', 'D']
    
    # Obtener todas las horas únicas ordenadas
    horas_unicas = sorted(df['hora'].unique())
    hora_a_idx = {h: i for i, h in enumerate(horas_unicas)} # Mapear hora a un índice numérico
    
    fechas_unicas = df['fecha'].unique()
    num_dias = len(fechas_unicas)
    
    for i, fecha in enumerate(fechas_unicas):
        df_dia = df[df['fecha'] == fecha].copy()
        df_dia['acumulado'] = range(1, len(df_dia) + 1)
        
        nombre_dia = df_dia['dia'].iloc[0]
        color = colores_lineas[i % len(colores_lineas)]
        estilo = estilos_linea[i % len(estilos_linea)]
        marcador = marcadores[i % len(marcadores)]
        
        # Calcular desplazamiento (Jitter): si hay 3 días, los offsets serán -0.15, 0, +0.15
        offset = (i - (num_dias - 1) / 2) * 0.15
        
        # Crear posiciones X desplazadas
        x_pos = [hora_a_idx[h] + offset for h in df_dia['hora']]
        
        # Graficar con estilos distintos y el eje X desplazado
        ax4.plot(x_pos, df_dia['acumulado'], marker=marcador, linestyle=estilo,
                 label=f"{nombre_dia}", color=color, linewidth=2.5, markersize=8, drawstyle='steps-post')
        
        # Rellenar debajo de la línea
        ax4.fill_between(x_pos, df_dia['acumulado'], alpha=0.05, color=color, step='post')
        
        # Poner los números sobre cada punto
        for x, y in zip(x_pos, df_dia['acumulado']):
            ax4.text(x, y + 0.15, str(y), ha='center', va='bottom', fontweight='bold', color=color)

    # Configurar el eje X para que muestre las horas en lugar de números
    ax4.set_xticks(range(len(horas_unicas)))
    ax4.set_xticklabels(horas_unicas, rotation=45)
    
    ax4.set_title('Tendencia Acumulada por Hora (con desplazamiento)')
    ax4.set_xlabel('Hora del día')
    ax4.set_ylabel('Personas Acumuladas')
    ax4.legend(loc='upper left')
    ax4.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    ruta_salida = 'data/dashboard_aforo.png'
    plt.savefig(ruta_salida, dpi=150)
    print(f"[INFO] Dashboard con Jitter guardado en: {ruta_salida}")

if __name__ == "__main__":
    generar_dashboard()
