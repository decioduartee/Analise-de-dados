# python -m streamlit run streamlit_app.py
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet='gasto', ttl=5)

# Mostrando conteudo total da planilha
## existing_data = existing_data.dropna(how="all")

# Puxando Data da planilha para fazer um filtro
existing_data['Date'] = pd.to_datetime(existing_data['Date'], errors='coerce')
existing_data = existing_data.sort_values("Date")

# Filtro de data ***Removendo os nan-nan com replace***
existing_data['Month'] = existing_data['Date'].apply(lambda x: str(x.month) + '-' + str(x.year)).replace("nan-nan")
# Selectbox com data
month = st.sidebar.selectbox('Mês', existing_data['Month'].unique())

# Removendo colunas vazias da planilha
existing_data_removeNaN = existing_data.loc[:,~existing_data.columns.str.match("Unnamed")]

# Filtro de dados
## Mes/ano
df_filtered = existing_data_removeNaN[existing_data['Month'] == month]
## City
city_total = df_filtered.groupby('City')[["Total"]].sum().reset_index()
## 
Rating_city_total = df_filtered.groupby('City')[["Rating"]].mean().reset_index()

# Criando colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Criando grafico
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Date", y="Product line", color="City", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

fig_rating = px.bar(Rating_city_total, y="Rating", x="City", title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)