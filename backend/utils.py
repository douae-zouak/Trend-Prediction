import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_future_dates(start_date: str, periods: int = 90):
    """
    Créer des dates futures pour la prédiction
    """
    start = pd.to_datetime(start_date)
    dates = pd.date_range(start=start, periods=periods, freq='D')
    return pd.DataFrame({'ds': dates})

def add_regressors(df, include_target=False):
    """
    Ajouter les régresseurs temporels
    """
    df = df.copy()
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['day_of_month'] = df['ds'].dt.day
    df['week_of_year'] = df['ds'].dt.isocalendar().week
    df['month'] = df['ds'].dt.month
    df['quarter'] = df['ds'].dt.quarter
    df['is_weekend'] = (df['ds'].dt.dayofweek >= 5).astype(int)
    df['is_month_start'] = (df['ds'].dt.day <= 7).astype(int)
    df['is_month_end'] = (df['ds'].dt.day >= 24).astype(int)
    
    # Ces colonnes nécessitent la variable cible : Moving Averages & Lags
    if include_target and 'y' in df.columns:
        # Lissent la série
        # Réduisent les pics/bruits
        # la tendance courte durée
        df['ma_7'] = df['y'].rolling(7, min_periods=1).mean()
        # la tendance long terme
        df['ma_30'] = df['y'].rolling(30, min_periods=1).mean()
        # Permet au modèle de comprendre les patterns mensuels.
        # Donne la valeur d’il y a 7 jours.
        df['lag_7'] = df['y'].shift(7)
        df['lag_30'] = df['y'].shift(30)
        
        # Remplir les valeurs manquantes
        for col in ["ma_7", "ma_30", "lag_7", "lag_30"]:
            if col in df.columns:
                df[col].fillna(df[col].mean(), inplace=True)
    
    # Saisons et événements
    df['is_summer'] = df['month'].isin([6, 7, 8]).astype(int)
    df['is_christmas_season'] = df['month'].isin([11, 12]).astype(int)
    df['is_back_to_school'] = (
        (df['month'] == 8) | 
        ((df['month'] == 9) & (df['day_of_month'] <= 15))
    ).astype(int)
    
    return df

def calculate_metrics(y_true, y_pred):
    """
    Calculer les métriques de performance
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    return {
        'MAE': float(mae),
        'RMSE': float(rmse),
        'R2': float(r2)
    }