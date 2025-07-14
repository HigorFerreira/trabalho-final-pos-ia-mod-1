from modulos.typings import MergeNamespace
import pandas as pd

def merge(args: MergeNamespace):
    print(args)
    # args.validate()
    dt1, dt2 = args.datasets
    pr1, pr2 = args.prefixes

    df1 = pd.read_excel(dt1)
    df2 = pd.read_excel(dt2)

    df1 = df1.drop(columns=args.remove_from_dataset_1)
    df2 = df2.drop(columns=args.remove_from_dataset_2)
    df1 = df1.rename(columns={ str(col): "_".join([pr1, col]) for col in df1.columns })
    df2 = df2.rename(columns={ str(col): "_".join([pr2, col]) for col in df2.columns })
    # print(dict(df1=df1.columns, df2=df2.columns))

    df = df1.join(df2)

    for col in args.last_columns:
        try:
            columns = df.columns.to_list()
            columns.remove(col)
            columns.append(col)
            df = df[columns]
        except ValueError:
            raise ValueError(f"Column {col} not in dataframe")
        except Exception as err:
            raise Exception(err)

    df.to_excel(args.excel)