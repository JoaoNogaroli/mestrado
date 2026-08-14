from heapq import merge
import os
import streamlit as st
import pandas as pd
st.title("Otimização de Carteiras — Ibovespa")

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados():
    return pd.read_csv('carteiras_mf.csv')

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados_piotroski():
    return pd.read_csv('carteiras_piotroski.csv')

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados_minvar():
    return pd.read_csv('carteiras_minvar.csv')

@st.cache_data
def mf_acumulado_f(ano):
    pa_th = f'plotagem_streamlit/magic_formula_acumulados/ano_frente/acumulado_f/acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def mf_acumulado(ano):
    pa_th = f'plotagem_streamlit/magic_formula_acumulados/ano_igual/acumulado/acumulado_{ano-1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_ibov_f(ano):
    pa_th = f'plotagem_streamlit/magic_formula_acumulados/ano_frente/acumulado_f_ibov/ibov_acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_ibov(ano):
    pa_th = f'plotagem_streamlit/magic_formula_acumulados/ano_igual/acumulado_ibov/ibov_acumulado_{ano-1}.csv'
    return pd.read_csv(pa_th)

#piotroski--------------
@st.cache_data
def acumulado_piotroski(ano):
    pa_th = f'plotagem_streamlit/piotroski_acumulados/ano_igual/acumulado/acumulado_{ano-1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_piotroski_f(ano):
    pa_th = f'plotagem_streamlit/piotroski_acumulados/ano_frente/acumulado_f/acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

# MIN VAR
@st.cache_data
def acumulado_minvar(ano):
    pa_th = f'plotagem_streamlit/minvar/ano_igual/acumulado/acumulado_{ano-1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_minvar_f(ano):
    pa_th = f'plotagem_streamlit/minvar/ano_frente/acumulado_f/acumulado_{ano}.csv'
    return pd.read_csv(pa_th)


# ________________________________________


df = carregar_dados()
ano = st.sidebar.selectbox("Ano da carteira", sorted(df['ano'].unique()))
df_ano = df[df['ano'] == ano].sort_values('peso', ascending=False).drop(columns=['Unnamed: 0'])
# st.dataframe(df_ano, hide_index=True,
#              column_config={'peso': st.column_config.NumberColumn(format="%.2f%%")})
df_ano.rename(columns={'ativo':'ativos_mf','peso':'peso_mf'}, inplace=True)
df_piotroski = carregar_dados_piotroski()

df_minvar = carregar_dados_minvar()


df_ano['ativo_piotroski'] = df_piotroski['ativo']
df_ano['peso_piotroski'] = df_piotroski['peso']

df_ano['ativo_minvar'] = df_minvar['ativo']
df_ano['peso_minvar'] = df_minvar['peso']
# print(df_piotroski)


st.dataframe(df_ano, hide_index=True)


# =========================================================
#ACUMULADOS atual
func_acum = mf_acumulado(ano)
df_acum = func_acum.set_index('date').rename(columns={'0':'retorno_mf'})
#----piotroski
func_piotroski_acum = acumulado_piotroski(ano)
df_piotroski_acum = func_piotroski_acum.set_index('date').rename(columns={'0':'retorno_piotroski'})
#-----minvar
func_minvar_acum = acumulado_minvar(ano)
df_minvar_acum = func_minvar_acum.set_index('date').rename(columns={'0':'retorno_minvar'})
# print("==============df_minvar_acum")
# print(df_minvar_acum)
# =========================================================

## IBov atual
func_acum_ibov = acumulado_ibov(ano)
df_acum_ibov = func_acum_ibov.set_index('Date').rename(columns={'IBOV':'retorno_ibov'})
df_acum_ibov.rename(index={'Date':'date'}, inplace=True)


tit0 = f"Usando dados de treino da data: 01/10/({int(ano)-1}) -> 31/03/({ano}), comprei a carteira no dia 01/04/{ano}"
st.subheader(tit0)

titulo1 = f"Gráfico da carteira do ano {ano} com dados do retorno {int(ano)-1} ->  {ano}: DENTRO DA AMOSTRA "
st.subheader(titulo1)
merged_df = pd.merge(pd.merge(pd.merge(df_acum, df_acum_ibov, left_index=True, right_index=True),df_piotroski_acum, left_index=True, right_index=True),df_minvar_acum,left_index=True, right_index=True)

# merged_df.rename(columns={'retorno_x':'retorno_magic_formula', 'retorno_y':'retorno_ibov', 'retorno':'retorno_piotroski'}, inplace=True)
# print(merged_df)
# st.line_chart(df_acum)
# st.line_chart(df_acum_ibov)
st.line_chart(merged_df, y=['retorno_mf', 'retorno_ibov','retorno_piotroski','retorno_minvar'], x_label = ['data'], y_label = ['retorno'])

try:

    # ===============================================
    #Acumulados pra frente
    func_acum_f =  mf_acumulado_f(ano)
    df_acum_f = func_acum_f.set_index('date').rename(columns={'0':'retorno_mf'})
    #-----piotroski
    func_piotroski_acum_f = acumulado_piotroski_f(ano)
    df_piotroski_acum_f = func_piotroski_acum_f.set_index('date').rename(columns={'0':'retorno_piotroski'})
    # ----minvar
    func_minvar_acum_f = acumulado_minvar_f(ano)
    df_minvar_acum_f = func_minvar_acum_f.set_index('date').rename(columns={'0':'retorno_minvar'})
    print("df_minvar_acum_f")
    print(df_minvar_acum_f)
    # ===============================================

    ## ibov pra frente
    func_acum_ibov_f = acumulado_ibov_f(ano)
    df_acum_ibov_f = func_acum_ibov_f.set_index('Date').rename(columns={'IBOV':'retorno_ibov'})
    df_acum_ibov_f.rename(index={'Date':'date'}, inplace=True)

    titulo2 = f"Gráfico da carteira do ano {ano} plotada 1 ano para frente, FORA DA AMOSTRA:  "
    st.subheader(titulo2)
    merged_df_f = pd.merge(pd.merge(pd.merge(df_acum_f, df_acum_ibov_f, left_index=True, right_index=True),df_piotroski_acum_f, left_index=True, right_index=True),df_minvar_acum_f, left_index=True, right_index=True)
    # merged_df_f.rename(columns={'retorno_x':'retorno_magic_formula', 'retorno_y':'retorno_ibov','retorno':'retorno_piotroski'}, inplace=True)
    # st.line_chart(df_acum_f)
    # st.line_chart(df_acum_ibov_f)
    st.line_chart(merged_df_f, y=['retorno_mf', 'retorno_ibov','retorno_piotroski','retorno_minvar'], x_label = ['data'], y_label = ['retorno'])
except Exception as e:
    print(e)

    pass