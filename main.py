import argparse
from operations import main_exec, predict_exec

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


if __name__ == '__main__':
    args = parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
