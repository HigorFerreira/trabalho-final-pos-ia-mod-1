import pytest
import pandas as pd
from modulos.data_load import load, coins

def test_load_returns_dataframe():
    res = load('AAVEBTC')

    # Check if result is a dataframe
    assert isinstance(res, pd.DataFrame)

    assert not res.empty

def test_load_raises_error_if_not_coin_invalid_input_type():
    invalid_inputs = [ 123, None, True, False ]
    for inv_ipt in  invalid_inputs:
        with pytest.raises(TypeError, match="Coin must be string"):
            load(inv_ipt)


def test_load_raises_error_if_invalid_coin():
    with pytest.raises(Exception):
        load('Something')

def test_list_of_coins_10():
    assert len(coins) >= 10
    for coin in coins:
        assert  isinstance(coin, str)

def test_each_coin_returns_dataframe():
    for coin in coins:
        res = load(coin)
        assert isinstance(res, pd.DataFrame)
        assert not res.empty