from copy import copy
from binance.client import Client
from binance.enums import *
import pandas as pd
from secrets import api_key, api_secret
import sqlite3
from moeda import moeda

#criando objeto de conexão com a Binance.
cliente = Client(api_key,api_secret)
moedas = ['BTCUSDT','XRPUSDT','BNBUSDT','GMTUSDT','ETHUSDT']   #lista de nomes para as moedas.

#criando os objetos com os nomes.
moedas_obj = []
for c in moedas:
    y = copy(c)
    c = moeda(y,cliente)
    moedas_obj.append(c)

#crianção do banco de dados para uma ou mais moedas.
def criandoBD(moedas,intervalo,dias,BD_nome,MA_rapida,MA_lenta,MA_tendencia):
    conn = sqlite3.connect(f'{BD_nome}.db')
    cursor = conn.cursor()

    for moeda in moedas:
        moeda.buscar_dados_históricos(intervalo,dias,MA_rapida,MA_lenta,MA_tendencia)
        tabela_moeda = moeda.df
        tabela_moeda.to_sql(f'{moeda.nome}',conn,if_exists='replace',index=False)
    return None

#exemplo de uso da função "criandoBD()"
criandoBD(moedas_obj,'15m',20,'segundo_BD',10,25,50)
