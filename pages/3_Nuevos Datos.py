import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Control de Rutas")

# Especificar la ruta del archivo CSV
file_path = '/static/datasets/controlruta.csv'

# Leer el archivo CSV
try:
    df = pd.read_csv(file_path, encoding='utf-8', sep=';')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1', sep=';')

# Asegurarse de que los nombres de las columnas no tengan espacios al principio o al final
df.columns = df.columns.str.strip()

# Convertir la columna 'Fecha' a datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')

# Filtrar las filas con fechas no convertibles
df = df.dropna(subset=['FECHA'])

# Obtener las opciones únicas de cada filtro
rutasU = sorted(df['RUTA'].unique())
vehiculosU = sorted(df['VEHICULO'].unique())
estadosU = sorted(df['ESTADO'].unique())

# Configurar las columnas y selectores
col1, col2, col3 = st.columns(3)

with col1:
    rutasU.insert(0, "Todas")
    optionRuta = st.selectbox('Ruta', (rutasU))

with col2:
    vehiculosU.insert(0, "Todos")
    optionVehiculo = st.selectbox('Vehículo', (vehiculosU))

with col3:
    estadosU.insert(0, "Todos")
    optionEstado = st.selectbox('Estado', (estadosU))

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionRuta != "Todas":
    filtered_data = filtered_data[filtered_data['RUTA'] == optionRuta]

if optionVehiculo != "Todos":
    filtered_data = filtered_data[filtered_data['VEHICULO'] == optionVehiculo]

if optionEstado != "Todos":
    filtered_data = filtered_data[filtered_data['ESTADO'] == optionEstado]

# Crear un gráfico de barras para la cantidad de registros por ESTADO
registros_por_estado = filtered_data['ESTADO'].value_counts().reset_index()
registros_por_estado.columns = ['Estado', 'Cantidad']
fig_bar = px.bar(registros_por_estado, x='Estado', y='Cantidad', title='Cantidad de Registros por Estado')

# Crear un gráfico de líneas para la diferencia de tiempo (DIFERENCIA) a lo largo del tiempo (FECHA)
fig_line = px.line(filtered_data, x='FECHA', y='DIFERENCIA', title='Diferencia de Tiempo a lo Largo del Tiempo')

# Mostrar los gráficos
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)

# Mostrar la tabla filtrada
st.write("Datos filtrados", filtered_data)

