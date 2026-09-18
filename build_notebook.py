"""
build_notebook.py
------------------
Genera el notebook de analisis de la Fase 3 (analisis_fase3.ipynb)
de forma programatica, para asegurar que las celdas queden bien
formadas sin errores de copiado manual.

Ejecucion:
    python build_notebook.py
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
    "# Fase 3: Analisis e Interpretacion - YOLO Aforo\n"
    "\n"
    "Analisis del aforo agrupado por bloque horario, a partir del "
    "dataset limpio generado en la Fase 2."
))

cells.append(nbf.v4.new_code_cell(
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "\n"
    "import config\n"
    "\n"
    "df = pd.read_csv(config.CLEAN_DATASET_PATH)\n"
    "df.head()"
))

cells.append(nbf.v4.new_markdown_cell("## 1. Conteo total de personas por bloque horario"))

cells.append(nbf.v4.new_code_cell(
    "conteo_total = df.groupby('bloque_horario').size().rename('total_personas')\n"
    "conteo_total"
))

cells.append(nbf.v4.new_markdown_cell(
    "## 2. Promedio de personas por muestra\n"
    "\n"
    "Cada fila del dataset limpio es una deteccion individual en un instante "
    "de muestreo. Agrupamos primero por instante (fecha+hora) contando "
    "personas, y luego promediamos esos conteos por bloque horario."
))

cells.append(nbf.v4.new_code_cell(
    "personas_por_muestra = (\n"
    "    df.groupby(['fecha', 'hora', 'bloque_horario'])\n"
    "      .size()\n"
    "      .reset_index(name='personas_en_muestra')\n"
    ")\n"
    "\n"
    "promedio_por_bloque = (\n"
    "    personas_por_muestra.groupby('bloque_horario')['personas_en_muestra']\n"
    "    .mean()\n"
    "    .rename('promedio_personas')\n"
    ")\n"
    "promedio_por_bloque"
))

cells.append(nbf.v4.new_markdown_cell("## 3. Pico maximo de personas detectadas por bloque"))

cells.append(nbf.v4.new_code_cell(
    "pico_por_bloque = (\n"
    "    personas_por_muestra.groupby('bloque_horario')['personas_en_muestra']\n"
    "    .max()\n"
    "    .rename('pico_maximo')\n"
    ")\n"
    "pico_por_bloque"
))

cells.append(nbf.v4.new_markdown_cell("## 4. Tabla resumen de metricas por bloque horario"))

cells.append(nbf.v4.new_code_cell(
    "resumen = pd.concat([conteo_total, promedio_por_bloque, pico_por_bloque], axis=1)\n"
    "resumen"
))

cells.append(nbf.v4.new_markdown_cell(
    "## 5. Grafico comparativo\n"
    "\n"
    "Comparacion visual del total de personas detectadas en cada jornada, "
    "para apoyar decisiones de asignacion de personal."
))

cells.append(nbf.v4.new_code_cell(
    "fig, ax = plt.subplots(figsize=(6, 4))\n"
    "conteo_total.plot(kind='bar', ax=ax, color=['#4C72B0', '#DD8452'])\n"
    "ax.set_title('Total de personas detectadas por bloque horario')\n"
    "ax.set_xlabel('Bloque horario')\n"
    "ax.set_ylabel('Cantidad de personas detectadas')\n"
    "plt.xticks(rotation=0)\n"
    "plt.tight_layout()\n"
    "plt.savefig('data/grafico_bloques.png', dpi=150)\n"
    "plt.show()"
))

nb['cells'] = cells

with open('analisis_fase3.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("[INFO] Notebook generado: analisis_fase3.ipynb")
