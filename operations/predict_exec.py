from .predict.mlp import mlp
from .predict.svr import svr
from modulos.typings import PredictNamespace


def predict_exec(args: PredictNamespace):
    match args.model:
        case 'MLP_REGRESSOR':
            return mlp(args)
        case 'SVR':
            return svr(args)