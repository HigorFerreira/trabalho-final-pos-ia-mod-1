from modulos.data_load import load, column_normalizer
import logging

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np


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

