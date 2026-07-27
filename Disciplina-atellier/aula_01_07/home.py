from pandas import col
import streamlit as st
import pandas as pd
st.title("Otimização de Carteiras — Ibovespa")

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados():
    return pd.read_csv('carteiras.csv')


@st.cache_data
def acumulado_f(ano):
    return pd.read_csv(f'acumulado_f/acumulado_{ano+1}.csv')

@st.cache_data
def acumulado(ano):
    return pd.read_csv(f'acumulado/acumulado_{ano}.csv')


df = carregar_dados()
ano = st.sidebar.selectbox("Ano da carteira", sorted(df['ano'].unique()))
df_ano = df[df['ano'] == ano].sort_values('peso', ascending=False).drop(columns=['Unnamed: 0'])
# st.dataframe(df_ano, hide_index=True,
#              column_config={'peso': st.column_config.NumberColumn(format="%.2f%%")})


#Acumulado pra frente
func_acum_f =  acumulado_f(ano)
df_acum_f = func_acum_f.set_index('date').rename(columns={'0':'retorno'})

#acumulado atual
func_acum = acumulado(ano)
df_acum = func_acum.set_index('date').rename(columns={'0':'retorno'})


st.dataframe(df_ano, hide_index=True)


titulo1 = f"Gráfico da carteira do ano {ano} plotada para proprio ano {ano}"
st.subheader(titulo1)
st.line_chart(df_acum)


titulo2 = f"Gráfico da carteira do ano {ano} plotada para frente {ano+1}"
st.subheader(titulo2)
st.line_chart(df_acum_f)

