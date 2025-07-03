import pandas as pd
import logging
import os

from typing import Literal

data_map = {
    'AAVEBTC': "/".join([ os.getcwd(), "dados", "Poloniex_AAVEBTC_1h" ]),
    'AAVEUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_AAVEUSDT_1h" ]),
    'ACMUSDD': "/".join([ os.getcwd(), "dados", "Poloniex_ACMUSDD_1h" ]),
    'ADAUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_ADAUSDT_1h" ]),
    'BNBUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_BNBUSDT_1h" ]),
    'BNTUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_BNTUSDT_1h" ]),
    'CVTBTC': "/".join([ os.getcwd(), "dados", "Poloniex_CVTBTC_1h" ]),
    'DOGEBTC': "/".join([ os.getcwd(), "dados", "Poloniex_DOGEBTC_1h" ]),
    'ETCETH': "/".join([ os.getcwd(), "dados", "Poloniex_ETCETH_1h" ]),
    'USDPUSDT': "/".join([ os.getcwd(), "dados", "Poloniex_USDPUSDT_1h" ]),
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

def load(coin: Coin) -> pd.DataFrame:
    """
    Carrega os dados da moeda AAVE/BTC e retorna o DataFrame.
    Returns:
        dataframe
    """
    try:
        df = pd.read_csv(coin, skiprows=1)
        return df
    except Exception as err:
        logging.error(str(err))