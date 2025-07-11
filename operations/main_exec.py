from modulos.data_load import coins

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

