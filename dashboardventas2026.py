import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    file_path = 'datosII/SalidaVentas.xlsx'
    df = pd.read_excel(file_path)
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

st.set_page_config(layout='wide')
st.title('Análisis de Ventas por Región y Tiempo')

st.sidebar.header('Filtros')

# Region filter
all_regions = ['All'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox('Selecciona una Región', all_regions)

filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = df[df['Region'] == selected_region]

# Date filter
min_date = df['Order Date'].min().to_pydatetime()
max_date = df['Order Date'].max().to_pydatetime()

start_date, end_date = st.sidebar.date_input(
    'Selecciona un rango de fechas',
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = filtered_df[(filtered_df['Order Date'].dt.date >= start_date) & (filtered_df['Order Date'].dt.date <= end_date)]

st.subheader('Métricas Clave')
col1, col2 = st.columns(2)

with col1:
    total_sales = filtered_df['Sales'].sum()
    st.metric(label='Ventas Totales', value=f'${total_sales:,.2f}')

with col2:
    total_profit = filtered_df['Profit'].sum()
    st.metric(label='Ganancia Total', value=f'${total_profit:,.2f}')

st.subheader('Ventas por Región')
sales_by_region = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=sales_by_region.index, y=sales_by_region.values, ax=ax1, palette='viridis')
ax1.set_title('Ventas Totales por Región')
ax1.set_xlabel('Región')
ax1.set_ylabel('Ventas')
st.pyplot(fig1)

st.subheader('Ventas por Categoría de Producto')
sales_by_category = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=sales_by_category.index, y=sales_by_category.values, ax=ax2, palette='magma')
ax2.set_title('Ventas Totales por Categoría de Producto')
ax2.set_xlabel('Categoría')
ax2.set_ylabel('Ventas')
st.pyplot(fig2)

st.subheader('Ventas a lo largo del tiempo')
sales_over_time = filtered_df.set_index('Order Date').resample('ME')['Sales'].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.lineplot(x='Order Date', y='Sales', data=sales_over_time, marker='o', ax=ax3)
ax3.set_title('Ventas Mensuales a lo largo del tiempo')
ax3.set_xlabel('Fecha de Pedido')
ax3.set_ylabel('Ventas')
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

st.write("### Datos Subyacentes")
st.dataframe(filtered_df)
