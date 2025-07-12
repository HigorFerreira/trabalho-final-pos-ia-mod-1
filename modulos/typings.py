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

class SVCNamespace(BaseNamespace):
    svc_kernel: SvcKernel
    svc_degree: int
    def __init__(
        self,
        svc_kernel: SvcKernel = 'linear',
        svc_degree: int = 1,
        **kwargs
    ):
        super().__init__(**{
            'svc_kernel': svc_kernel,
            'svc_degree': svc_degree,
            **kwargs
        })

class PredictNamespace(
    MLPNamespace,
    SVCNamespace,
): pass