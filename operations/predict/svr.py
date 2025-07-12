from sklearn import svm
from modulos.data_load import load, column_normalizer
from sklearn.preprocessing import StandardScaler
from modulos.typings import SVRNamespace
from matplotlib import pyplot as plt
import logging

from modulos.typings import SVRNamespace

def svr(args: SVRNamespace):

    features = ['unix', 'weightedAverage']

    logging.info(f"Running {args.model} on {args.crypto} crypto for features {features}")
    df = load(args.crypto)
    df = column_normalizer(df)
    
    logging.warning(f"Features {features} are normalized using StandardScaler().fit_transform")
    X = StandardScaler().fit_transform(df[features])
    y = df['close']

    logging.info(f"Trainning SVR...")
    regr = svm.SVR(kernel=args.svr_kernel, degree=args.svr_degree)
    regr.fit(X, y)
    logging.info(f"SVR Trainned")

    columns = df.columns.copy().to_list()
    columns.remove('close')
    columns.append('close')
    df = df[columns]

    df['PREDICTED'] = regr.predict(X)
    logging.info(f"Predicted values assigned to dataframe")

    error = df[[ 'close', 'PREDICTED' ]].apply(lambda row: abs(row['close'] - row['PREDICTED']), axis=1)
    df.loc[error.index, 'ERROR'] = error
    logging.info(f"Error values assigned")

    logging.info(f"Writing {args.figure} figure...")
    plt.figure(figsize=(14, 6))
    plt.plot(df['date'], df['PREDICTED'], label='Predição')
    plt.plot(df['date'], df['close'], label='Valor real')
    plt.title(f"Modelo {args.model} aplicado em: {args.crypto} (kernel {args.svr_kernel}{
        f', degree {args.svr_degree}' if args.svr_kernel == 'poly' else ''
    })")
    plt.legend()
    plt.savefig(args.figure)
    logging.info(f"Figure wrote successfully")

    if args.excel is not None:
        logging.info(f"Writing {args.excel} excel...")
        df.to_excel(args.excel, sheet_name=f"Modelo {args.model} aplicado em {args.crypto} (kernel {args.svr_kernel}{
            f', degree {args.svr_degree}' if args.svr_kernel == 'poly' else ''
        })")
        logging.info(f"Excel wrote successfully")

    
    print(f"{args.model} finished successfully")
    logging.info(f"{args.model} finished successfully")