import sqlite3
import pandas as pd
from bancoDados import moedas


#criando tendências de alta e baixa
def definir_posi_MA(df):
    #variáveis de tendência de posição
    df['tendencia'] = ''
    df['posicao'] = 'fora de op.'

    #indicandores de tendência 
    for n in df.index.values:
        if df.loc[n,'MA_moderada'] > df.loc[n,'MA_lenta']:
            df.loc[n,'tendencia'] = 'alta'
        else:
            df.loc[n,'tendencia'] = 'baixa'
    return df



#definir posições de compra
def compra_simula_MA(df):
    for i in df.index.values:
        if i == 0:
            continue
        if df.loc[i-1, 'posicao'] == 'comprar' or df.loc[i-1,'posicao'] == 'comprado':
            if df.loc[i,'MA_rapida'] > df.loc[i,'MA_moderada']:
                df.loc[i,'posicao'] = 'comprado'
            else:
                df.loc[i,'posicao'] = 'real. Long'
        else:
            if df.loc[i,'tendencia'] == 'alta' and df.loc[i,'MA_rapida'] > df.loc[i,'MA_moderada']:
                df.loc[i,'posicao'] = 'comprar'


    return df

def venda_simula_MA(df):
    for i in df.index.values:
        if i == 0:
            continue
        if df.loc[i-1, 'posicao'] == 'vender' or df.loc[i-1,'posicao'] == 'vendido':
            if df.loc[i,'MA_rapida'] > df.loc[i,'MA_moderada']:
                df.loc[i,'posicao'] = 'real. Short'
            else:
                df.loc[i,'posicao'] = 'vendido'
        else:
            if df.loc[i,'tendencia'] == 'baixa' and df.loc[i,'MA_rapida'] < df.loc[i,'MA_moderada']:
                df.loc[i,'posicao'] = 'vender'

    return df


#definir L/P
def lucroPreju(df):

    #compra
    precoUltimaCompra = 0.0
    for i in df.index.values:
        #L/P == 0 para a primeira linha da tabela
        if i == 0 or df.loc[i,'posicao'] == 'fora de op.':
            df.loc[i,'L/P'] = 0
        else:
            if df.loc[i,'posicao'] == 'comprar':
                precoUltimaCompra = df.loc[i,'fechamento']
                df.loc[i,'L/P'] = df.loc[i-1,'L/P']
            elif df.loc[i,'posicao'] == 'comprado' or df.loc[i,'posicao'] == 'real. Long':
                LeP = df.loc[i,'fechamento'] / precoUltimaCompra - 0.04
                if LeP < 1:
                    LeP -= 1
                df.loc[i,'L/P'] = LeP 
    #venda 
    precoUltimavenda = 0.0
    for i in df.index.values:
    #L/P == 0 para a primeira linha da tabela
        if i == 0 or df.loc[i,'posicao'] == 'fora de op.':
            df.loc[i,'L/P'] = 0
        else:
            if df.loc[i,'posicao'] == 'vender':
                precoUltimavenda = df.loc[i,'fechamento']
                df.loc[i,'L/P'] = df.loc[i-1,'L/P']
            elif df.loc[i,'posicao'] == 'vendido' or df.loc[i,'posicao'] == 'real. Short':
                LeP =   precoUltimavenda / df.loc[i,'fechamento'] - 0.04
                if LeP < 1:
                    LeP -= 1
                df.loc[i,'L/P'] = LeP 
    return df

#retornando estatísticas gerais
def estatsGerais(df):
    #compra
    LPcompra = df.loc[df['posicao'] == 'real. Long', 'L/P'].sum()
    tradesCompra = 0
    for i in df.index.values:
        if df.loc[i,'posicao'] == 'real. Long':
            tradesCompra += 1
    #venda
    LPvenda = df.loc[df['posicao'] == 'real. Short', 'L/P'].sum()
    tradesVenda = 0
    for i in df.index.values:
        if df.loc[i,'posicao'] == 'real. Short':
            tradesVenda += 1
    #total
    LPtotal = LPcompra + LPvenda
    tradesTotal = tradesCompra + tradesVenda

    estats = {'LPcompra' : LPcompra,'tradesCompra': tradesCompra, 'LPvenda': LPvenda, 'tradesVenda': tradesVenda, 'LPtotal': LPtotal, 'tradesTotal': tradesTotal}
    return estats


def teste_estrat_MA(moeda,BD_nome,MA_rap,MA_mod,MA_len,tabela=True):
    #crianção de médias móveis 
    conn = sqlite3.connect(f'{BD_nome}.db')

    df = pd.read_sql( f'SELECT * FROM {moeda}',conn)
    df['MA_rapida'] = df['fechamento'].rolling(MA_rap).mean()
    df['MA_moderada'] = df['fechamento'].rolling(MA_mod).mean()
    df['MA_lenta'] = df['fechamento'].rolling(MA_len).mean()
    
    #alta
    definir_posi_MA(df)
    compra_simula_MA(df)

    #baixa
    venda_simula_MA(df)

    #reajuste
    compra_simula_MA(df)
    #resultados
    lucroPreju(df)
    stats = estatsGerais(df)

    if tabela == True:
        return [df,stats]
    else:
        return stats
