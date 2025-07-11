import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from modulos.data_load import load, coins
from sklearn.model_selection import TimeSeriesSplit

import warnings
warnings.filterwarnings("ignore")

"""
preparacao.py
    
Etapas do trabalho: 6, 7 e 8

Este script prepara os dados de cada moeda para modelagem:

1. Carrega e ordena as séries temporais.
2. Gera features como volatilidade (faixa de preço), retornos e momentum de 7 dias,
   médias móveis, desvio padrão, indicadores de volume e dia da semana.
3. Trata divisões por zero com np.where e remove valores ausentes.
4. Normaliza as features dentro de cada fold usando StandardScaler.
5. Usa TimeSeriesSplit (5 folds) para criar conjuntos de treino e validação temporais.
6. Retorna um dicionário com, para cada moeda, seus 5 folds prontos para o próximo passo.
"""


def preparar_dados(n_splits=5):
    resultados = {}

    for coin in coins:
        df = load(coin)
        print(f'Processando moeda: {coin}')
        
        df = df.sort_values('date').reset_index(drop=True)

        # Features derivadas
        df['faixa_preco'] = df['high'] - df['low']
        df['retorno_pct_7d'] = df['close'].pct_change(7)
        df['momentum_7d'] = df['close'] - df['close'].shift(7)
        df['media_movel_7d'] = df['close'].rolling(window=7).mean()
        df['std_7d'] = df['close'].rolling(window=7).std()
        df['volume_2_7d'] = df['Volume 2'].rolling(window=7).mean()

        # Evita divisão por zero usando np.where
        df['taker_ratio'] = np.where(df['Volume 2'] != 0, df['buyTakerAmount'] / df['Volume 2'], np.nan)
        df['buy_pressure'] = np.where(df['tradeCount'] != 0, df['buyTakerQuantity'] / df['tradeCount'], np.nan)
        df['volume_volatilidade_ratio'] = np.where(df['faixa_preco'] != 0, df['Volume 2'] / df['faixa_preco'], np.nan)

        df['date'] = pd.to_datetime(df['date'])
        df['dia_da_semana'] = df['date'].dt.dayofweek

        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)

        features = [
            'media_movel_7d', 'std_7d', 'momentum_7d', 'retorno_pct_7d',
            'volume_2_7d', 'taker_ratio', 'buy_pressure', 'volume_volatilidade_ratio',
            'dia_da_semana'
        ]

        tscv = TimeSeriesSplit(n_splits=n_splits)
        folds = []

        for fold_idx, (train_idx, val_idx) in enumerate(tscv.split(df)):
            df_train = df.iloc[train_idx].copy()
            df_val = df.iloc[val_idx].copy()

            scaler = StandardScaler()
            scaler.fit(df_train[features])

            df_train.loc[:, features] = scaler.transform(df_train[features])
            df_val.loc[:, features] = scaler.transform(df_val[features])

            folds.append({
                'train': df_train,
                'val': df_val,
                'scaler': scaler
            })

        resultados[coin] = folds

    return resultados

# folds_por_moeda = preparar_dados()

# for coin, folds in folds_por_moeda.items():
#     print(f"\nMoeda: {coin}")
#     for i, fold in enumerate(folds, start=1):
#         print(f"  Fold {i}: Train shape = {fold['train'].shape},  Val shape = {fold['val'].shape}")

