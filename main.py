import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Main script to analise Cryptos")

    parser.add_argument("--crypto", type=str, required=True, help="Cryptocurrency symbol (e.g., BTC, ETH)")

    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = parse_args()

    print(f'Crypto: {args.crypto}')