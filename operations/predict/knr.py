from sklearn.neighbors import KNeighborsRegressor
from modulos.data_load import load, column_normalizer
from sklearn.preprocessing import StandardScaler
from argparse import Namespace
from modulos.typings import KNRegressorNamespace
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import logging

def knr(args: KNRegressorNamespace):
    logging.info(f"Running {args.model} on {args.crypto} crypto")
    df = load(args.crypto)
    df = column_normalizer(df)

    features = ['unix', 'weightedAverage']

    X = StandardScaler().fit_transform(df[features].iloc[0:int(len(df)*args.amount)])
    y = df['close'].iloc[0:int(len(df)*args.amount)]

    regr = KNeighborsRegressor(n_neighbors=args.kn_neighbors, weights=args.kn_weights)
    regr.fit(X, y)

    columns = df.columns.copy().to_list()
    columns.remove('close')
    columns.append('close')
    df = df[columns]

    df['PREDICTED'] = regr.predict(StandardScaler().fit_transform(df[features]))
    error = df[[ 'close', 'PREDICTED' ]].apply(lambda row: abs(row['close'] - row['PREDICTED']), axis=1)
    df.loc[error.index, 'ERROR'] = error


    # region: Figure plotting
    figure, axs = plt.subplots(2, 1)
    ax1: Axes = axs[0]
    ax2: Axes = axs[1]
    figure.set_figwidth(14)
    figure.set_figheight(12)
    # plt.figure(figsize=(14, 6))
    ax1.plot(df['date'], df['PREDICTED'], 'b', label='Predição')
    ax1.plot(df['date'], df['close'], 'r', label='Valor real')
    ax1.set_title(f"Modelo {args.model} aplicado em: {args.crypto} (k = {args.kn_neighbors}, a = {args.amount}, w = {args.kn_weights})")
    ax1.legend()


    ax2.plot(df['date'], df['close'], 'r', label='Valor real')
    ax2.set_title(f"Modelo {args.model} aplicado em: {args.crypto} (apenas dados reais)")
    ax2.legend()

    figure.savefig(args.figure)
    # endregion


    if args.excel is not None:
        df.to_excel(args.excel, sheet_name=f"Modelo {args.model} aplicado em {args.crypto}")