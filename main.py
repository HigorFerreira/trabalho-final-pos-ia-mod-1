import argparse
from operations import (
    main_exec,
    predict_exec,
    analyse_coin,
    merge_exec
)

def parse_args():
    parser = argparse.ArgumentParser(description="Main script to analise Cryptos")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    predict = subparsers.add_parser("predict", help="Use a model do predict a coin")
    predict.add_argument("--crypto", type=str, required=True, help="Cryptocurrency symbol (e.g., AAVEBTC, DOGEBTC)")
    predict.add_argument("--model", type=str, required=True, help="Model")
    predict.add_argument("--amount", type=float, required=False, default=0.7, help="The percentage of data to use for training. Represented as a number between 0 and 1, with a default value of 0.7")
    predict.add_argument("--figure", type=str, default="out.png", required=False, help="Figure file out")
    predict.add_argument("--excel", type=str, default=None, required=False, help="Excel file out")
    predict.add_argument("--mlp_hidden_layer_sizes", nargs='+', default=[50, 100, 50], help='(MLP MODEL) Hidden layer neurons. Default 50 100 50')
    predict.add_argument("--mlp_activation", type=str, default='relu', help='(MLP MODEL) Activation (relu, identity, logistic, tanh). Default relu')
    predict.add_argument("--mlp_max_iter", type=int, default=800, help='(MLP MODEL) Max iterations. Default 800')
    predict.add_argument("--mlp_random_state", type=int, default=1, help='Default 1')
    predict.add_argument("--svr_kernel", type=str, default='linear', required=False, help="(SVR MODEL) Svr kernel ('linear', 'poly', 'rbf', 'sigmoid', 'precomputed')")
    predict.add_argument("--svr_degree", type=int, default=1, required=False, help="(SVR MODEL) Svr degree for svr_kernel poly option")
    predict.add_argument("--kn_neighbors", type=int, default=5, required=False, help="(KNR MODEL) Number of k neightbors. Default 5")
    predict.add_argument("--kn_weights", type=str, default='distance', required=False, help="(KNR MODEL) Weight (uniform or distance). Default distance")
    predict.set_defaults(func=predict_exec)

    merge = subparsers.add_parser("merge", help="Merge two datasets do compare")
    merge.add_argument("--datasets", nargs='+', required=True, help="Dataset paths: dataset1 dataset2")
    merge.add_argument("--prefixes", nargs='+', default=[ 'dt1', 'dt2' ], required=False, help="Column prefixers. Defaul: dt1 dt2")
    merge.add_argument("--last_columns", nargs='+', default=[], required=False, help="Last columns of the final dataset")
    merge.add_argument("--excel", type=str, default='out.xlsx', required=False, help="Excel file output. Default out.xlsx")
    merge.add_argument("--remove_from_dataset_1", nargs='+', default=[], required=False, help="Remove columns from dataset 1")
    merge.add_argument("--remove_from_dataset_2", nargs='+', default=[], required=False, help="Remove columns from dataset 2")
    merge.set_defaults(func=merge_exec)

    analysys = subparsers.add_parser("analysys", help="Make analyse to each coin")
    analysys.add_argument("--n_splits", type=int, required=False, default=5, help="Set n_splits")
    analysys.add_argument("--crypto", type=str, required=True, help="Cryptocurrency symbol (e.g., AAVEBTC, DOGEBTC)")
    analysys.set_defaults(func=analyse_coin)
    
    parser.add_argument('--list', nargs='+', help='List: crypto, model')
    parser.set_defaults(func=main_exec)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
