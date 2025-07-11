from modulos.preparacao import preparar_dados
from modulos.analisa_moeda import analisar_moeda

def analyse_coin(args):
    folds_por_moeda = preparar_dados(args.n_splits)

    for coin, folds in folds_por_moeda.items():
        df = analisar_moeda(coin, folds)
        df.to_excel("Analysys.xlsx", sheet_name=coin)