import pytest
import pandas as pd
import json
from modulos.data_load import load, coins, column_normalizer, Coin

expected_column_shape = ["unix", "date", "symbol", "open", "high", "low", "close", "Volume 1", "Volume 2", "buyTakerAmount", "buyTakerQuantity", "tradeCount", "weightedAverage"]

def test_column_normalizer_argment_typing():
    invalid_entries = [ 123, 'error', None, True, False, 12.6 ]
    for invld_ent in invalid_entries:
        with pytest.raises(TypeError):
            column_normalizer(invld_ent)
            
    df = pd.DataFrame({ 'Column1': [ 1, 2 ], 'Column2': [ 3, 4 ] })
    res = column_normalizer(df)
    assert isinstance(res, pd.DataFrame)

def test_column_normalizer_empty_data_frame():
    df = pd.DataFrame()
    with pytest.raises(ValueError, match="Invalid empty dataframe"):
        column_normalizer(df)


def test_each_column_normalization():
    _coins: list[Coin] = coins
    for coin in _coins:
        df = load(coin)
        df = column_normalizer(df)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert json.dumps(list(df.columns)) == json.dumps(expected_column_shape)