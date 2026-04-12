!pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title('Streamlit DataFrame y Gráfica de Línea')

st.write("### DataFrame de Ejemplo")

# Crear un DataFrame de ejemplo
data = {
    'Fecha': pd.to_datetime(pd.date_range(start='2023-01-01', periods=10)),
    'Valor_A': np.random.rand(10) * 100,
    'Valor_B': np.random.rand(10) * 50 + 20
}
df = pd.DataFrame(data)

# Establecer 'Fecha' como índice para la gráfica de línea si se usa st.line_chart
df = df.set_index('Fecha')

# Mostrar el DataFrame
st.dataframe(df)

st.write("### Gráfica de Línea de Valor_A y Valor_B")

# Crear una gráfica de línea usando st.line_chart
st.line_chart(df[['Valor_A', 'Valor_B']])

st.write("\nPara ejecutar esta aplicación, guarda el código en un archivo `.py` (por ejemplo, `app.py`) y luego ejecuta `streamlit run app.py` en tu terminal.")
