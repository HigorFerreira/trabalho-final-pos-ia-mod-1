import pandas as pd
import logging
import os

from .typings import Coin

from typing import Literal

data_map = {
    'AAVEUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_AAVEUSDT_d.csv" ]),
    'ADAUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_ADAUSDT_d.csv" ]),
    'ALPACAUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_ALPACAUSDT_d.csv" ]),
    'APEUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_APEUSDT_d.csv" ]),
    'ATLASUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_ATLASUSDT_d.csv" ]),
    'BTCUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_BTCUSDT_d.csv" ]),
    'DOGEUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_DOGEUSDT_d.csv" ]),
    'ETHUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_ETHUSDT_d.csv" ]),
    'XRPBULLUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_XRPBULLUSDT_d.csv" ]),
    'YFIUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_YFIUSDT_d.csv" ]),
}

coins = ('AAVEUSDT', 'ADAUSDT', 'ALPACAUSDT', 'APEUSDT', 'ATLASUSDT', 'BTCUSDT', 'DOGEUSDT', 'ETHUSDT', 'XRPBULLUSDT', 'YFIUSDT')
models = (
    'MLP_REGRESSOR',
    'SVR',
    'KNRegressor',
)

def load(coin: Coin) -> pd.DataFrame:
    """
    Carrega os dados de determinada moeda e retorna o DataFrame.
    Returns:
        dataframe
    """
    try:
        if not isinstance(coin, str): raise TypeError('Coin must be string')
        logging.info(f"Reading coin {coin} from path: {data_map[coin]}")
        df = pd.read_csv(data_map[coin], skiprows=1)
        df['date'] = pd.to_datetime(df['date'])
        df = column_normalizer(df)
        df = df.sort_values(by='unix', ascending=True)
        return df
    except Exception as err:
        logging.error(str(err))
        raise err


def column_normalizer(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame")

    if df.empty:
        raise ValueError("Invalid empty dataframe")
    
    def get_transform_fn(arr: list):
        new_arr = [ "Volume 1" if i == 7  else "Volume 2" if i == 8 else x for i, x in enumerate(arr) ]
        def transform(extern_arr: list): return { str(extern_arr[i]): x for i, x in enumerate(new_arr) }
        return transform
    
    cols = list(df.columns)
    transform = get_transform_fn(cols)

    return df.rename(columns=transform(cols))
