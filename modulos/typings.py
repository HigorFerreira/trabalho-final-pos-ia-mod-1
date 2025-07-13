from typing import Literal
from argparse import Namespace

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

Model = Literal[
    'MLP_REGRESSOR',
    'SVR',
    'KNRegressor',
]

SvcKernel = Literal['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']

class BaseNamespace(Namespace):
    crypto: Coin
    model: Model
    amount: float
    figure: str
    excel: str | None

    def __init__(
            self,
            crypto: Coin,
            model: Model,
            amount: float = 0.7,
            figure: str = 'out.png',
            excel: str | None = None,
            **kwargs
        ):

        args = dict(
            crypto=crypto,
            model=model,
            amount=amount,
            figure=figure,
            excel=excel,
        )
        args = { **args, **kwargs }

        super().__init__(**args)



class MLPNamespace(BaseNamespace): pass

class SVRNamespace(BaseNamespace):
    svr_kernel: SvcKernel
    svr_degree: int
    def __init__(
        self,
        svr_kernel: SvcKernel = 'linear',
        svr_degree: int = 1,
        **kwargs
    ):
        super().__init__(**{
            'svr_kernel': svr_kernel,
            'svr_degree': svr_degree,
            **kwargs
        })

class KNRegressorNamespace(BaseNamespace):
    kn_neighbors: int = 5
    kn_weights: Literal['uniform', 'distance']
    def __init__(
            self,
            kn_neighbors: int = 5,
            kn_weights: Literal['uniform', 'distance'] = 'distance',
            **kwargs
        ):
        super().__init__(**{
            'kn_neighbors': kn_neighbors,
            'kn_weights': kn_weights,
            **kwargs
        })

class PredictNamespace(
    MLPNamespace,
    SVRNamespace,
): pass