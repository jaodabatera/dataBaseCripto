from binance.client import Client
from binance.enums import *
import pandas as pd
#importando variáveis "api_key" e "api_secret" do arquivo "secrets".
from secrets import api_key, api_secret


#criando variável de conexão com os serviços da Binance.
cliente = Client(api_key,api_secret)

#declarando a classe, que receberá um nome("ETHUSDT","BTCUSDT","ADAUSDT"...) para a criação do objeto.
class moeda:
    def __init__(self,nome):
        self.nome = nome
        return None
      
    #Função responsável por adquirir informações atualizadas necessárias para a futura criação de um bot trader. Essa função também cria informações
    #necessárias como as médias móveis que queremos utilizar para a estratégia.
    #IMPORTANTE: As médias móveis devem ser colocadas em ordem da mais rápida para a mais lenta para o melhor funcionamento do programa.
    def atualizar(self,intervalo,MA_rapida,MA_lenta,MA_tendencia):
        ultima = pd.DataFrame(Client.get_historical_klines(cliente,self.nome,intervalo,limit=MA_tendencia,klines_type=HistoricalKlinesType.FUTURES))
        ultima = ultima.iloc[:,1:5]
        ultima.columns = [['abertura','máxima','mínima','fechamento']]
        ultima['MA_rap'] = ultima.fechamento.rolling(MA_rapida).mean()
        ultima['MA_lenta'] = ultima.fechamento.rolling(MA_lenta).mean()
        ultima['MA_tendencia'] = ultima.fechamento.rolling(MA_tendencia).mean()
        self.MA_rap = ultima.iloc[-1,-3]
        self.MA_lenta = ultima.iloc[-1,-2]
        self.MA_tendecia = ultima.iloc[-1,-1]
        self.fechamento = ultima.iloc[-1,3]
        self.maxima = ultima.iloc[-1,1]
        self.minima = ultima.iloc[-1,2]
        self.abertura = ultima.iloc[-1,0]
        return self
      
    #Função parecida com a "atualizar()", mas não retorna apenas os dados do último candle(dados mais recentes), mas nos traz um dataframe completo das 
    #variações de preços e médias móveis nos últimos x dias sendo x definido pelo usuário.
    def buscar_dados_históricos(self,intervalo,dias,MA_rapida,MA_lenta,MA_tendencia):
        df = pd.DataFrame(Client.get_historical_klines(cliente,self.nome,intervalo,f'{dias} days ago UTC',limit=MA_tendencia,klines_type=HistoricalKlinesType.FUTURES))
        df = df.iloc[:,0:5]
        df.columns([['horário de abertura','abertura','máxima','mínima','fechamento']])
        
#EXEMPLO DE FUNCIONAMENTO:

#criando o objeto "ETHUSDT":
ETHUSDT = moeda('ETHUSDT')

#atualizando(utilizando candles de 1 minutos e médias móveis de 10,25,50):
ETHUSDT.atualizar('15m',10,25,50)

#criando um dataframe com as variações dos últimos 10 dias usando os mesmos parâmentros do exemplo acima:
ETHUSDT.buscar_dados_históricos('15m',10,10,25,50)
