from .predict.mlp import mlp
from .predict.svr import svr
from .predict.knr import knr
from .predict.linear import linear
from modulos.typings import PredictNamespace


def predict_exec(args: PredictNamespace):
    match args.model:
        case 'MLP_REGRESSOR':
            return mlp(args)
        case 'SVR':
            return svr(args)
        case 'KNRegressor':
            return knr(args)
        case 'LINEAR':
            return linear(args)