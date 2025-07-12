from modulos.preparacao import preparar_dados
from modulos.analisa_moeda import analisar_moeda
from argparse import Namespace
from modulos.data_load import Coin

class AnalyseCoinProps(Namespace):
    n_splits: int
    crypto: Coin

def analyse_coin(args: AnalyseCoinProps):
    coin = args.crypto
    folds_por_moeda = preparar_dados(args.n_splits)
    df = analisar_moeda(coin, folds_por_moeda[coin])
    df.to_excel(f'ANALYSYS_{coin}.xlsx')