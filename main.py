import argparse
import pandas as pd
from modulos.data_load import coins, load, column_normalizer
import logging

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description="Main script to analise Cryptos")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Check the effects of this command later
    # subparsers.required = True

    predict = subparsers.add_parser("predict", help="Use a model do predict a coin")
    predict.add_argument("--crypto", type=str, required=True, help="Cryptocurrency symbol (e.g., AAVEBTC, DOGEBTC)")
    predict.add_argument("--model", type=str, required=True, help="Model")
    predict.add_argument("--figure", type=str, default="out.png", required=False, help="Figure file out")
    predict.add_argument("--excel", type=str, default=None, required=False, help="Excel file out")
    predict.set_defaults(func=predict_exec)
    
    parser.add_argument('--list', nargs='+', help='List: crypto, model')
    parser.set_defaults(func=main_exec)

    args = parser.parse_args()
    return args

# from modulos.preparacao import preparar_dados
# from modulos.analisa_moeda import analisar_moeda

# folds_por_moeda = preparar_dados()

# for coin, folds in folds_por_moeda.items():
#     analisar_moeda(coin, folds)

def main_exec(args):
    if args.list:
        list = args.list
        if 'crypto' in list:
            print("-"*30)
            print("Coins:")
            print("-"*30)
            for c in coins: print(c)
            print("-"*30, "\n")

        if 'model' in list:
            print("-"*30)
            print("Models:")
            print("-"*30)
            print("MLP_REGRESSOR")


def predict_exec(args):
    crypto: str = args.crypto
    model: str = args.model
    figure: str = args.figure
    excel: str | None = args.excel
    

    logging.info(f"Starting {model} for crypto {crypto}")
    logging.warning(f"Other models aren't implemented yet")
    df = load(crypto)
    df = column_normalizer(df)

    predictors = [ 'unix', 'Volume 1', 'Volume 2', 'tradeCount', 'weightedAverage' ]
    outcome = 'close'

    X = df[predictors]
    y = df[outcome]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled

    regg = MLPRegressor(hidden_layer_sizes=(50,100,50), activation='relu', max_iter=800, random_state=1)
    regg.fit(X_scaled, y)

    if len(set(regg.predict(X_scaled))) < 0.8*len(df):
        logging.warning(f"Less predicted entries")

    dff = df
    dff['PREDICTED'] = regg.predict(X_scaled)
    dff = dff[[ 'symbol', 'date', 'close', 'PREDICTED' ]].rename(columns={ 'close': 'FECHAMENTO REAL' })
    dff['ERRO'] = dff[['FECHAMENTO REAL', 'PREDICTED']].apply(lambda row: abs(row['FECHAMENTO REAL'] - row['PREDICTED']), axis=1)
    if excel is not None:
        dff.to_excel(excel)

    logging.info(f"Max error: {dff[dff['ERRO'] == dff['ERRO'].max()]}")
    logging.info(f"Min error: {dff[dff['ERRO'] == dff['ERRO'].min()]}")

    plt.figure(figsize=(14, 6))
    plt.title(crypto)
    plt.plot(dff['date'], dff['PREDICTED'], label='Predição')
    plt.plot(dff['date'], dff['FECHAMENTO REAL'], label='Valor real')
    plt.ylim(dff['FECHAMENTO REAL'].min()-0.005, dff['FECHAMENTO REAL'].max()+0.005)
    plt.legend()
    plt.savefig(figure)



if __name__ == '__main__':
    args = parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
