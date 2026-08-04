import streamlit as st
import pandas as pd
st.title("Otimização de Carteiras — Ibovespa")

@st.cache_data                    # roda 1x, guarda o resultado
def carregar_dados():
    return pd.read_csv('Disciplina-atellier/mestrado/carteiras.csv')


@st.cache_data
def acumulado_f(ano):
    pa_th = f'Disciplina-atellier/mestrado/plotagem_streamlit/acumulado_f/acumulado_{ano+1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado(ano):
    pa_th = f'Disciplina-atellier/mestrado/plotagem_streamlit/acumulado/acumulado_{ano}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_ibov_f(ano):
    pa_th = f'Disciplina-atellier/mestrado/plotagem_streamlit/acumulado_ibov_f/ibov_acumulado_{ano+1}.csv'
    return pd.read_csv(pa_th)

@st.cache_data
def acumulado_ibov(ano):
    pa_th = f'Disciplina-atellier/mestrado/plotagem_streamlit/acumulado_ibov/ibov_acumulado_{ano}.csv'
    return pd.read_csv(pa_th)


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

## IBov atual
func_acum_ibov = acumulado_ibov(ano)
df_acum_ibov = func_acum_ibov.set_index('Date').rename(columns={'IBOV':'retorno'})
df_acum_ibov.rename(index={'Date':'date'}, inplace=True)
## ibov pra frente
func_acum_ibov_f = acumulado_ibov_f(ano)
df_acum_ibov_f = func_acum_ibov_f.set_index('Date').rename(columns={'IBOV':'retorno'})
df_acum_ibov_f.rename(index={'Date':'date'}, inplace=True)
st.dataframe(df_ano, hide_index=True)


titulo1 = f"Gráfico da carteira do ano {ano} plotada para proprio ano {ano}"
st.subheader(titulo1)
merged_df = pd.merge(df_acum, df_acum_ibov, left_index=True, right_index=True)
merged_df.rename(columns={'retorno_x':'retorno_carteira', 'retorno_y':'retorno_ibov'}, inplace=True)
# st.line_chart(df_acum)
# st.line_chart(df_acum_ibov)
st.line_chart(merged_df, y=['retorno_carteira', 'retorno_ibov'], x_label = ['data'], y_label = ['retorno'])

titulo2 = f"Gráfico da carteira do ano {ano} plotada para frente {ano+1}"
st.subheader(titulo2)
merged_df_f = pd.merge(df_acum_f, df_acum_ibov_f, left_index=True, right_index=True)
merged_df_f.rename(columns={'retorno_x':'retorno_carteira', 'retorno_y':'retorno_ibov'}, inplace=True)
# st.line_chart(df_acum_f)
# st.line_chart(df_acum_ibov_f)
print(merged_df_f)
st.line_chart(merged_df_f, y=['retorno_carteira', 'retorno_ibov'], x_label = ['data'], y_label = ['retorno'])
