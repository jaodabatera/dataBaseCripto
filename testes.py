from teste_estrat_codigos import teste_estrat_MA
import pandas as pd
from bancoDados import moedas
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)

lptodas_moedas = 0
for moeda in moedas:
    resultado = teste_estrat_MA(moeda,'DFmoedas',20,50,100,False)
    lptodas_moedas += resultado['LPtotal']
    print( f'''{moeda}: L/P total: {resultado['LPtotal']:.2f}%, Trades: {resultado['tradesTotal']}\r\nLong: {resultado['tradesCompra']} trades, {resultado['LPcompra']:.2f}%\r\nShort: {resultado['tradesVenda']} trades, {resultado['LPvenda']:.2f}%\r\n''')
print(f'L/P final: {lptodas_moedas:.2f}%')
#teste = teste_estrat_MA('XRPUSDT','DFmoedas',20,50,100)
#print(teste[0][['tendencia','posicao','MA_lenta','MA_moderada','MA_rapida']])