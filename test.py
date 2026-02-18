import pandas as pd
import numpy as np
import random
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.environ import SolverFactory
import yfinance as yf
import matplotlib.pyplot as plt



lista_ativos = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'WEGE3.SA',
       'B3SA3.SA', 'BBAS3.SA', 'RENT3.SA', 'PRIO3.SA', 'SUZB3.SA', 'GGBR4.SA',
       'CSNA3.SA', 'GOAU4.SA', 'RADL3.SA', 'ENEV3.SA', 'EQTL3.SA', 'FLRY3.SA',
       'HAPV3.SA', 'MGLU3.SA', '^BVSP']

lista_ativos = random.sample(lista_ativos[0:-1],10)

print("-----------COMEÇANDO---------")

mydf = pd.DataFrame()
for ativo in lista_ativos:
    mydf[ativo] = yf.download(ativo, period="6mo")["Close"]

retornos = (mydf / mydf.shift(1))-1

retorno_media = retornos.mean()*127

valor_total_investir = 50000
tamanho_carteira = 10
maximo_peso_carteira = 0.15


#MODELO
model = pyo.ConcreteModel()

#Definindo Variaveis
model.x = pyo.Var(range(tamanho_carteira), bounds=(0, 0.15))
x=model.x

#Restrições
model.soma_peso_percent = pyo.Constraint(expr = sum(x[i] for i in range(int(tamanho_carteira))) == 1 )
model.soma_total_investido = pyo.Constraint(expr = sum(x[i] * retorno_media.iloc[i] for i in range(tamanho_carteira)) <= 50000)

model.maximo_peso_ativo = pyo.ConstraintList()
for i in range(tamanho_carteira):
    model.maximo_peso_ativo.add(expr = x[i] <= 0.15)

#Objetivo
model.obj = pyo.Objective(expr = sum(x[i] * retorno_media.iloc[i] for i in range(tamanho_carteira)))

opt = SolverFactory('cplex')
opt.solve(model)

retorno_media['Porcentagem Na Carteira'] = pyo.value(x)
print('-----------')
print(retorno_media)
print('-----------')
print("-------MODELO IMPRESSO----------")
# model.pprint()






print('------------FIM-----')