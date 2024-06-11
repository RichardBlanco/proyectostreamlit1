import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.write("Simulador Cesde")

# Cargar los datos
try:
    df = pd.read_csv('static/datasets/data.csv')
except FileNotFoundError:
    st.error("El archivo de datos no se encontró. Asegúrate de que el archivo esté en la ruta correcta.")
    st.stop()

# Obtener las opciones únicas de cada filtro
gruposU = sorted(df['GRUPO'].unique())
nivelesU = sorted(df['NIVEL'].unique())
jornadasU = sorted(df['JORNADA'].unique())
horarioU = sorted(df['HORARIO'].unique())
submodulosU = sorted(df['SUBMODULO'].unique())
docentesU = sorted(df['DOCENTE'].unique())
momentosU = sorted(df['MOMENTO'].unique())

# Configurar las columnas y selectores
col1, col2, col3, col4 = st.columns(4)

with col1:
    gruposU.insert(0,"Todos")
    optionGrupo = st.selectbox('Grupo', (gruposU))

with col2:       
    optionMomento = st.selectbox('Momento', (momentosU))

with col3:
    nivelesU.insert(0, "Todos")
    optionNivel = st.selectbox('Nivel', (nivelesU))

with col4:
    jornadasU.insert(0, "Todos")
    optionJornada = st.selectbox('Jornada', (jornadasU))

col5, col6 = st.columns(2)

with col5:
    submodulosU.insert(0, "Todos")
    optionSubmodulo = st.selectbox('Submódulo', (submodulosU))

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionGrupo != 'Todos':
    filtered_data = filtered_data[filtered_data['GRUPO'] == optionGrupo]

if optionMomento:
    filtered_data = filtered_data[filtered_data['MOMENTO'] == optionMomento]

if optionNivel != 'Todos':
    filtered_data = filtered_data[filtered_data['NIVEL'] == optionNivel]

if optionJornada != 'Todos':
    filtered_data = filtered_data[filtered_data['JORNADA'] == optionJornada]

if optionSubmodulo != 'Todos':
    filtered_data = filtered_data[filtered_data['SUBMODULO'] == optionSubmodulo]

# Crear el gráfico de barras
if not filtered_data.empty:
    NOTAS = filtered_data['NOMBRE']
    fig = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=NOTAS, y=filtered_data['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=NOTAS, y=filtered_data['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=NOTAS, y=filtered_data['PRODUCTO'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No hay datos disponibles para los filtros seleccionados.")

# Crear un gráfico de barras para el rendimiento promedio por Submódulo
if optionSubmodulo == 'Todos' and not filtered_data.empty:
    grouped_data = df.groupby('SUBMODULO')[['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']].mean().reset_index()
    fig_submodulo = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=grouped_data['SUBMODULO'], y=grouped_data['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=grouped_data['SUBMODULO'], y=grouped_data['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=grouped_data['SUBMODULO'], y=grouped_data['PRODUCTO'])
    ])
    fig_submodulo.update_layout(barmode='group', title='Rendimiento promedio por Submódulo')
    st.plotly_chart(fig_submodulo, use_container_width=True)
