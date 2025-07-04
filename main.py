import argparse
from modulos.data_load import coins

def parse_args():
    parser = argparse.ArgumentParser(description="Main script to analise Cryptos")

    parser.add_argument("--crypto", type=str, required=False, help="Cryptocurrency symbol (e.g., AAVEBTC, DOGEBTC)")
    parser.add_argument("--model", type=str, required=False, help="Model")
    parser.add_argument("-l", "--list", action="store_true", help="List cryptos")


    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = parse_args()

    if args.list:
        print("-"*30)
        print("Coins:")
        print("-"*30)
        for c in coins: print(c)
        print("-"*30, "\n"*3)

    # print(f'Crypto: {args.crypto}')
    # print(f'List: {args.list}')