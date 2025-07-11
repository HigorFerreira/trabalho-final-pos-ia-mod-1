from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def analisar_moeda(coin, folds):
    print(f"\n🔍 Analisando moeda: {coin}")
    resultados = []

    for fold_idx, split in enumerate(folds, start=1):
        X_train = split['train'][[
            'media_movel_7d', 'std_7d', 'momentum_7d', 'retorno_pct_7d',
            'volume_2_7d', 'taker_ratio', 'buy_pressure', 'volume_volatilidade_ratio',
            'dia_da_semana'
        ]].values
        y_train = split['train']['close'].values
        X_val = split['val'][[
            'media_movel_7d', 'std_7d', 'momentum_7d', 'retorno_pct_7d',
            'volume_2_7d', 'taker_ratio', 'buy_pressure', 'volume_volatilidade_ratio',
            'dia_da_semana'
        ]].values
        y_val = split['val']['close'].values

        modelos = {
            'MLP': MLPRegressor(hidden_layer_sizes=(50,100,50), max_iter=800, random_state=42),
            'Linear': LinearRegression()
        }

        for grau in range(2, 11):
            modelos[f'Poly_{grau}'] = make_pipeline(
                PolynomialFeatures(degree=grau, include_bias=False),
                LinearRegression()
            )

        for nome, modelo in modelos.items():
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_val)

            mse = mean_squared_error(y_val, y_pred)
            mae = mean_absolute_error(y_val, y_pred)
            r2  = r2_score(y_val, y_pred)

            sinais = (y_pred[1:] > y_val[:-1]).astype(int)
            retornos = np.where(sinais, y_val[1:] / y_val[:-1], 1.0)
            profit = 1000 * np.cumprod(retornos)[-1]

            resultados.append({
                'fold': fold_idx,
                'modelo': nome,
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'profit': profit
            })

    df_resultado = pd.DataFrame(resultados)
    resumo = df_resultado.groupby('modelo').mean().sort_values('profit', ascending=False)

    print("\n📊 Resultados médios por modelo (ordenados por lucro):")
    print(resumo)

    return df_resultado
