from heapq import merge
import os
import streamlit as st
import pandas as pd
st.title("Otimização de Carteiras — Ibovespa")

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados():
    return pd.read_csv('carteiras.csv')

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados_piotroski():
    return pd.read_csv('carteiras_piotroski.csv')

@st.cache_data
def acumulado_f(ano):
    pa_th = f'plotagem_streamlit/acumulado_f/acumulado_{ano+1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado(ano):
    pa_th = f'plotagem_streamlit/acumulado/acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_ibov_f(ano):
    pa_th = f'plotagem_streamlit/acumulado_ibov_f/ibov_acumulado_{ano+1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_ibov(ano):
    pa_th = f'plotagem_streamlit/acumulado_ibov/ibov_acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

#piotroski
@st.cache_data
def acumulado_piotroski(ano):
    pa_th = f'plotagem_streamlit/acumulados_piotroski/acumulado/acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_piotroski_f(ano):
    pa_th = f'plotagem_streamlit/acumulados_piotroski/acumulado_f/acumulado_{ano+1}.csv'
    return pd.read_csv(pa_th)


df = carregar_dados()
ano = st.sidebar.selectbox("Ano da carteira", sorted(df['ano'].unique()))
df_ano = df[df['ano'] == ano].sort_values('peso', ascending=False).drop(columns=['Unnamed: 0'])
# st.dataframe(df_ano, hide_index=True,
#              column_config={'peso': st.column_config.NumberColumn(format="%.2f%%")})
df_ano.rename(columns={'ativo':'ativos_mf','peso':'peso_mf'}, inplace=True)
df_piotroski = carregar_dados_piotroski()

df_ano['ativo_piotroski'] = df_piotroski['ativo']
df_ano['peso_piotroski'] = df_piotroski['peso']
print(df_piotroski)


st.dataframe(df_ano, hide_index=True)

#Acumulado pra frente
func_acum_f =  acumulado_f(ano)
df_acum_f = func_acum_f.set_index('date').rename(columns={'0':'retorno'})
#-----piotroski
func_piotroski_acum_f = acumulado_piotroski_f(ano)
df_piotroski_acum_f = func_piotroski_acum_f.set_index('date').rename(columns={'0':'retorno'})


#acumulado atual
func_acum = acumulado(ano)
df_acum = func_acum.set_index('date').rename(columns={'0':'retorno'})
#----piotroski
func_piotroski_acum = acumulado_piotroski(ano)
df_piotroski_acum = func_piotroski_acum.set_index('date').rename(columns={'0':'retorno'})


## IBov atual
func_acum_ibov = acumulado_ibov(ano)
df_acum_ibov = func_acum_ibov.set_index('Date').rename(columns={'IBOV':'retorno'})
df_acum_ibov.rename(index={'Date':'date'}, inplace=True)
## ibov pra frente
func_acum_ibov_f = acumulado_ibov_f(ano)
df_acum_ibov_f = func_acum_ibov_f.set_index('Date').rename(columns={'IBOV':'retorno'})
df_acum_ibov_f.rename(index={'Date':'date'}, inplace=True)



titulo1 = f"Gráfico da carteira do ano {ano} plotada para proprio ano {ano}"
st.subheader(titulo1)
merged_df = pd.merge(pd.merge(df_acum, df_acum_ibov, left_index=True, right_index=True),df_piotroski_acum, left_index=True, right_index=True)
merged_df.rename(columns={'retorno_x':'retorno_magic_formula', 'retorno_y':'retorno_ibov', 'retorno':'retorno_piotroski'}, inplace=True)
# print(merged_df)
# st.line_chart(df_acum)
# st.line_chart(df_acum_ibov)
st.line_chart(merged_df, y=['retorno_magic_formula', 'retorno_ibov','retorno_piotroski'], x_label = ['data'], y_label = ['retorno'])

titulo2 = f"Gráfico da carteira do ano {ano} plotada para frente {ano+1}"
st.subheader(titulo2)
merged_df_f = pd.merge(pd.merge(df_acum_f, df_acum_ibov_f, left_index=True, right_index=True),df_piotroski_acum_f, left_index=True, right_index=True)
merged_df_f.rename(columns={'retorno_x':'retorno_magic_formula', 'retorno_y':'retorno_ibov','retorno':'retorno_piotroski'}, inplace=True)
# st.line_chart(df_acum_f)
# st.line_chart(df_acum_ibov_f)
st.line_chart(merged_df_f, y=['retorno_magic_formula', 'retorno_ibov','retorno_piotroski'], x_label = ['data'], y_label = ['retorno'])
