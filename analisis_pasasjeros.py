# -*- coding: utf-8 -*-
# analisis_pasajeros.py
#%%
import pandas as pd
import matplotlib.pyplot as plt

print('Hola Mundo')

# Cargar datos
url = 'https://raw.githubusercontent.com/knunez-ecci/Seminario/refs/heads/main/salida_mensual_pasajeros_aeropuerto_destino_internacional.csv'
aeropuerto_df = pd.read_csv(url)

print("Información del DataFrame:")
print(aeropuerto_df.info())
print("Columnas disponibles:", aeropuerto_df.columns.to_list())

# Renombrar columnas
column_rename_map = {
    "sal_codigo": "Código",
    "sal_destinoint": "Destino Internacional",
    "sal_indicador": "Indicador",
    "sal_periodo": "Periodo",
    "sal_valor": "Valor"
}
aeropuerto_df.rename(columns=column_rename_map, inplace=True)

print("Primeros 5 registros:")
print(aeropuerto_df.head())

print("Indicadores únicos:", pd.unique(aeropuerto_df['Indicador']))
print("Códigos únicos:", pd.unique(aeropuerto_df['Código']))
print("Destinos únicos:", pd.unique(aeropuerto_df['Destino Internacional']))

print("Estadísticas de 'Valor':")
print(aeropuerto_df['Valor'].describe())

# Gráfico frecuencia por código país
plt.figure(figsize=(18, 10))
frecuencia_paises = aeropuerto_df['Código'].value_counts()

ax = frecuencia_paises.plot(kind='bar', color='skyblue', edgecolor='black')
umbral = 50

for p in ax.patches:
    if p.get_height() > umbral:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', rotation=45)

plt.xticks(rotation=45, ha='right')
plt.title('Frecuencia de código país')
plt.xlabel('Código de País')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.show()

# ------------------------------------------------
# Extraer el año-mes correcto de 'Periodo'
aeropuerto_df['Periodo_str'] = aeropuerto_df['Periodo'].astype(str).str[-6:]
aeropuerto_df['Fecha'] = pd.to_datetime(aeropuerto_df['Periodo_str'], format='%Y%m', errors='coerce')

# Verificar conversión
print(aeropuerto_df[['Periodo', 'Periodo_str', 'Fecha']].head())

# Tendencia total pasajeros por fecha
tendencia = aeropuerto_df.groupby('Fecha')['Valor'].sum().reset_index()

# Separar antes y después de 2020 (inicio pandemia)
fecha_corte = pd.to_datetime('2020-01-01')
antes_df = tendencia[tendencia['Fecha'] < fecha_corte]
despues_df = tendencia[tendencia['Fecha'] >= fecha_corte]

plt.figure(figsize=(14, 6))
plt.fill_between(antes_df['Fecha'], 0, antes_df['Valor'], color='green', alpha=0.3, label='Antes de 2020')
plt.fill_between(despues_df['Fecha'], 0, despues_df['Valor'], color='red', alpha=0.3, label='Desde 2020 (Pandemia)')
plt.plot(tendencia['Fecha'], tendencia['Valor'], marker='o', linestyle='-', linewidth=2, label='Tendencia')
plt.title('Tendencia cronológica de pasajeros internacionales')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de pasajeros')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------
# Agrupar por país y fecha, obtener top 6 países con más visitantes
df_grouped = aeropuerto_df.groupby(['Destino Internacional', 'Fecha'])['Valor'].sum().reset_index()
top_paises = df_grouped.groupby('Destino Internacional')['Valor'].sum().nlargest(6).index
df_top = df_grouped[df_grouped['Destino Internacional'].isin(top_paises)]

# Gráficos múltiples para los 6 países más visitados
fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=True, sharey=True)
axes = axes.flatten()

for i, pais in enumerate(top_paises):
    ax = axes[i]
    data = df_top[df_top['Destino Internacional'] == pais].sort_values('Fecha')
    ax.plot(data['Fecha'], data['Valor'], marker='o')
    ax.set_title(pais)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Visitantes')
    ax.grid(True)

plt.tight_layout()
plt.show()

# ------------------------------------------------
# Gráfico único comparando la tendencia de los 6 países
plt.figure(figsize=(12, 7))
for pais in top_paises:
    data = df_top[df_top['Destino Internacional'] == pais].sort_values('Fecha')
    plt.plot(data['Fecha'], data['Valor'], marker='o', label=pais)
plt.title('Tendencia de visitantes de los 6 países más visitados')
plt.xlabel('Fecha')
plt.ylabel('Visitantes')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------
# Gráfico específico para Estados Unidos
df_us = aeropuerto_df[aeropuerto_df['Destino Internacional'] == 'Estados Unidos'].sort_values('Fecha')
plt.figure(figsize=(14, 7))
plt.plot(df_us['Fecha'], df_us['Valor'], marker='o', color='blue')
plt.title('Tendencia de visitantes - Estados Unidos')
plt.xlabel('Fecha')
plt.ylabel('Visitantes')
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
