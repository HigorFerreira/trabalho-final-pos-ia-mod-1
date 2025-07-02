import pandas as pd
import logging
import os

def load() -> pd.DataFrame:
    """
    Carrega os dados da moeda AAVE/BTC e retorna o DataFrame.
    Returns:
        dataframe
    """
    try:
        df = pd.read_csv("/".join([ os.getcwd(), "dados", "Poloniex_AAVEBTC_1h.csv" ]), skiprows=1)
        return df
    except Exception as err:
        logging.error(str(err))