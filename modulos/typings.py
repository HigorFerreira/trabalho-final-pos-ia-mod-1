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
]

SvcKernel = Literal['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']

class BaseNamespace(Namespace):
    def __init__(
            self,
            crypto: Coin,
            model: Model,
            figure: str,
            excel: str | None,
            **kwargs
        ):

        args = dict(
            crypto=crypto,
            model=model,
            figure=figure,
            excel=excel,
        )
        args = { **args, **kwargs }

        super().__init__(**args)

    crypto: Coin
    model: Model
    figure: str
    excel: str | None


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

class PredictNamespace(
    MLPNamespace,
    SVRNamespace,
): pass