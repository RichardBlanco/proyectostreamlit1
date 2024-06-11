import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Protecto Integrador - Ventas Restaurante")

# Especificar la ruta del archivo CSV
file_path = 'static/datasets/Restaurante.csv'

# Intentar leer el archivo CSV con diferentes encodings
try:
    df = pd.read_csv(file_path, encoding='utf-8', sep=';')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1', sep=';')

# Asegurarse de que los nombres de las columnas no tengan espacios al principio o al final
df.columns = df.columns.str.strip()

# Verificar si la columna 'Fecha' existe en el DataFrame
if 'Fecha' not in df.columns:
    st.error("La columna 'Fecha' no se encontró en el archivo de datos. Asegúrate de que el archivo CSV tenga la columna 'Fecha'.")
    st.stop()

# Convertir la columna 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

# Filtrar las filas con fechas no convertibles
df = df.dropna(subset=['Fecha'])

# Obtener las opciones únicas de cada filtro
productosU = sorted(df['Producto'].unique())
fechasU = sorted(df['Fecha'].dt.date.unique())

# Configurar las columnas y selectores
col1, col2 = st.columns(2)

with col1:
    fechasU.insert(0, "Todas")
    optionFecha = st.selectbox('Fecha', (fechasU))

with col2:
    productosU.insert(0, "Todos")
    optionProducto = st.selectbox('Producto', (productosU))

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionFecha != "Todas":
    filtered_data = filtered_data[filtered_data['Fecha'].dt.date == optionFecha]

if optionProducto != "Todos":
    filtered_data = filtered_data[filtered_data['Producto'] == optionProducto]

# Crear un gráfico de barras para el total de ventas por producto
ventas_por_producto = filtered_data.groupby('Producto')['Total'].sum().reset_index()
fig_bar = px.bar(ventas_por_producto, x='Producto', y='Total', title='Total de Ventas por Producto')

# Crear un gráfico de líneas para la evolución de ventas en el tiempo
ventas_por_fecha = filtered_data.groupby('Fecha')['Total'].sum().reset_index()
fig_line = px.line(ventas_por_fecha, x='Fecha', y='Total', title='Evolución de Ventas a lo Largo del Tiempo')

# Mostrar los gráficos
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)

# Mostrar la tabla filtrada
st.write("Datos filtrados", filtered_data)
