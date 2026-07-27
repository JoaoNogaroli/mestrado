from pandas import col
import streamlit as st
import pandas as pd
st.title("Otimização de Carteiras — Ibovespa")

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados():
    return pd.read_csv('carteiras.csv')


@st.cache_data
def acumulado_f(ano):
    return pd.read_csv(f'acumulado_{ano}')


df = carregar_dados()
ano = st.sidebar.selectbox("Ano da carteira", sorted(df['ano'].unique()))
df_ano = df[df['ano'] == ano].sort_values('peso', ascending=False).drop(columns=['Unnamed: 0'])
# st.dataframe(df_ano, hide_index=True,
#              column_config={'peso': st.column_config.NumberColumn(format="%.2f%%")})

func_acum =  acumulado_f(ano)
# df_acum = 

st.dataframe(df_ano, hide_index=True)

st.dataframe(df_ano, hide_index=True)

