from modulos.data_load import load, column_normalizer
import logging

from modulos.typings import MLPNamespace
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def mlp(args: MLPNamespace):
    logging.info(f"Running {args.model} on {args.crypto} crypto")
    df = load(args.crypto)
    df = column_normalizer(df)

    features = ['unix', 'weightedAverage']

    X = StandardScaler().fit_transform(df[features].iloc[0:int(len(df)*args.amount)])
    y = df['close'].iloc[0:int(len(df)*args.amount)]

    args.mlp_hidden_layer_sizes = list(map(lambda x: int(x), args.mlp_hidden_layer_sizes))

    regg = MLPRegressor(hidden_layer_sizes=args.mlp_hidden_layer_sizes, activation=args.mlp_activation, max_iter=args.mlp_max_iter, random_state=args.mlp_random_state)
    regg.fit(X, y)

    if len(set(regg.predict(StandardScaler().fit_transform(df[features])))) < 0.8*len(df):
        logging.warning(f"Less predicted entries")

    columns = df.columns.copy().to_list()
    columns.remove('close')
    columns.append('close')
    df = df[columns]

    df['PREDICTED'] = regg.predict(StandardScaler().fit_transform(df[features]))
    error = df[[ 'close', 'PREDICTED' ]].apply(lambda row: abs(row['close'] - row['PREDICTED']), axis=1)
    df.loc[error.index, 'ERROR'] = error
    

    logging.warning(f"Max error: {df[df['ERROR'] == df['ERROR'].max()]}")
    logging.warning(f"Min error: {df[df['ERROR'] == df['ERROR'].min()]}")


    logging.info(f"Writing {args.figure} figure...")
    plt.figure(figsize=(14, 6))
    plt.plot(df['date'], df['PREDICTED'], label='Predição')
    plt.plot(df['date'], df['close'], label='Valor real')
    plt.title(f"Modelo {args.model} aplicado em: {args.crypto}")
    plt.legend()
    plt.savefig(args.figure)
    logging.info(f"Figure wrote successfully")


    if args.excel is not None:
        df.to_excel(args.excel, sheet_name=f"Modelo {args.model} aplicado em {args.crypto}")

