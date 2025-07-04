import pandas as pd
import logging
import os

from typing import Literal

data_map = {
    'AAVEBTC': "/".join([ os.getcwd(), "dados", "Poloniex_AAVEBTC_1h.csv" ]),
    'AAVEUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_AAVEUSDT_1h.csv" ]),
    'ACMUSDD': "/".join([ os.getcwd(), "dados", "Poloniex_ACMUSDD_1h.csv" ]),
    'ADAUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_ADAUSDT_1h.csv" ]),
    'BNBUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_BNBUSDT_1h.csv" ]),
    'BNTUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_BNTUSDT_1h.csv" ]),
    'CVTBTC': "/".join([ os.getcwd(), "dados", "Poloniex_CVTBTC_1h.csv" ]),
    'DOGEBTC': "/".join([ os.getcwd(), "dados", "Poloniex_DOGEBTC_1h.csv" ]),
    'ETCETH': "/".join([ os.getcwd(), "dados", "Poloniex_ETCETH_1h.csv" ]),
    'USDPUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_USDPUSDT_1h.csv" ]),
}

Coin = Literal[
    'AAVEBTC'
    , 'AAVEUSDT'
    , 'ACMUSDD'
    , 'ADAUSDT'
    , 'BNBUSDT'
    , 'BNTUSDT'
    , 'CVTBTC'
    , 'DOGEBTC'
    , 'ETCETH'
    , 'USDPUSDT'
]

coins = ( 'AAVEBTC', 'AAVEUSDT', 'ACMUSDD', 'ADAUSDT', 'BNBUSDT', 'BNTUSDT', 'CVTBTC', 'DOGEBTC', 'ETCETH', 'USDPUSDT' )

def load(coin: Coin) -> pd.DataFrame:
    """
    Carrega os dados de determinada moeda e retorna o DataFrame.
    Returns:
        dataframe
    """
    try:
        logging.info(f"Reading coin {coin} from path: {data_map[coin]}")
        df = pd.read_csv(data_map[coin], skiprows=1)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        return df
    except Exception as err:
        logging.error(str(err))
        raise err