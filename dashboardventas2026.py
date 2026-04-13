import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. CARGA DE DATOS (Ruta corregida para GitHub)
@st.cache_data
def load_data():
    # USAMOS RUTA RELATIVA PARA GITHUB
    file_path = 'datosII/SalidaVentas.xlsx' 
    df = pd.read_excel(file_path)
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

st.set_page_config(layout='wide', page_title="Dashboard de Ventas")
st.title('📊 Análisis de Ventas por Región y Tiempo')

# --- SIDEBAR FILTROS ---
st.sidebar.header('Filtros de Control')

all_regions = ['All'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox('Selecciona una Región', all_regions)

filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = df[df['Region'] == selected_region]

# Filtro de Fechas
min_date = df['Order Date'].min().to_pydatetime()
max_date = df['Order Date'].max().to_pydatetime()
start_date, end_date = st.sidebar.date_input('Rango de fechas', [min_date, max_date])

filtered_df = filtered_df[(filtered_df['Order Date'].dt.date >= start_date) & 
                           (filtered_df['Order Date'].dt.date <= end_date)]

# Filtro de Categoría
all_cats = df['Category'].unique().tolist()
selected_cats = st.sidebar.multiselect('Categorías', options=all_cats, default=all_cats)
if selected_cats:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_cats)]

# --- MÉTRICAS ---
st.subheader('Métricas Clave')
c1, c2 = st.columns(2)
c1.metric('Ventas Totales', f'${filtered_df["Sales"].sum():,.2f}')
c2.metric('Ganancia Total', f'${filtered_df["Profit"].sum():,.2f}')

# --- GRÁFICAS ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader('Ventas por Región')
    sales_reg = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots()
    sns.barplot(x=sales_reg.index, y=sales_reg.values, palette='viridis', ax=ax1)
    st.pyplot(fig1)

with col_b:
    st.subheader('Ventas por Categoría')
    sales_cat = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    sns.barplot(x=sales_cat.index, y=sales_cat.values, palette='magma', ax=ax2)
    st.pyplot(fig2)

# --- MAPA (REQUISITO) ---
st.subheader('🌍 Mapa de Ventas por Estado (USA)')
sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
fig_map = px.choropleth(sales_state, locations='State', locationmode='USA-states', 
                         color='Sales', scope='usa', color_continuous_scale='Viridis')
st.plotly_chart(fig_map, use_container_width=True)

# --- TENDENCIA (CORREGIDO 'ME') ---
st.subheader('📈 Evolución de Ventas')
# Cambio de 'M' a 'ME' para evitar el error que mencionaste
sales_time = filtered_df.set_index('Order Date').resample('ME')['Sales'].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(10,4))
sns.lineplot(data=sales_time, x='Order Date', y='Sales', marker='o', ax=ax3)
st.pyplot(fig3)

st.write("### Vista de Datos Filtrados")
st.dataframe(filtered_df)
