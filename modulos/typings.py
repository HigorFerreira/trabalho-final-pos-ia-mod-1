from typing import Literal
from argparse import Namespace

Coin = Literal[
    'AAVEUSDT'
    ,'ADAUSDT'
    ,'ALPACAUSDT'
    ,'APEUSDT'
    ,'ATLASUSDT'
    ,'BTCUSDT'
    ,'DOGEUSDT'
    ,'ETHUSDT'
    ,'XRPBULLUSDT'
    ,'YFIUSDT'
]

Model = Literal[
    'MLP_REGRESSOR',
    'SVR',
    'KNRegressor',
    'LINEAR',
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



class MLPNamespace(BaseNamespace):
    mlp_hidden_layer_sizes: list[int]
    mlp_activation: Literal['relu', 'identity', 'logistic', 'tanh']
    mlp_max_iter: int
    mlp_random_state: int

    def __init__(
            self, crypto, model, amount = 0.7, figure = 'out.png', excel = None,
            mlp_hidden_layer_sizes: list[int] = [50, 100, 50],
            mlp_activation: Literal['relu', 'identity', 'logistic', 'tanh'] = 'relu',
            mlp_max_iter: int = 800,
            mlp_random_state: int = 1,
            **kwargs
    ):
        super().__init__(**{
            'crypto': crypto,
            'model': model,
            'amount': amount,
            'figure': figure,
            'excel': excel,
            'mlp_hidden_layer_sizes': mlp_hidden_layer_sizes,
            'mlp_activation': mlp_activation,
            'mlp_max_iter': mlp_max_iter,
            'mlp_random_state': mlp_random_state,
            **kwargs,
        })

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

class LinearRegressorNamespace(BaseNamespace):
    fit_intercept: bool = True
    normalize: bool = False  # deprecated no sklearn atual, mas mantido por compatibilidade

    def __init__(
        self,
        fit_intercept: bool = True,
        normalize: bool = False,
        **kwargs
        ):
        super().__init__(**{
            'fit_intercept': fit_intercept,
            'normalize': normalize,
            **kwargs
        })


class PredictNamespace(
    MLPNamespace,
    SVRNamespace,
): pass

class MergeNamespace(Namespace):
    datasets: list[str]
    prefixes: list[str]
    last_comlumns: list[str]
    excel: str
    remove_from_dataset_1: list[str]
    remove_from_dataset_2: list[str]

    def validate(self):
        dt1, dt2 = self.datasets
        pr1, pr2 = self.prefixes

        if not dt1 or not isinstance(dt1, str): raise ValueError("There's not dataframe 1")
        if not dt2 or not isinstance(dt2, str): raise ValueError("There's not dataframe 2")
        if not pr1 or not isinstance(pr1, str): raise ValueError("There's not prefixer 1")
        if not pr2 or not isinstance(pr2, str): raise ValueError("There's not prefixer 2")

    def __init__(
        self,
        datasets: list[str],
        prefixes: list[str] = [ 'dt1', 'dt2' ],
        last_columns: list[str] = [],
        excel: str = 'out.xlsx',
        remove_from_dataset_1: list[str] = [],
        remove_from_dataset_2: list[str] = [],
        **kwargs
    ):
        super().__init__(**{
            'datasets': datasets,
            'prefixes': prefixes,
            'last_columns': last_columns,
            'excel': excel,
            'remove_from_dataset_1': remove_from_dataset_1,
            'remove_from_dataset_2': remove_from_dataset_2,
            **kwargs,
        })