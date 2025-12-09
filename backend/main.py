from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import joblib
import pandas as pd
import base64
import io
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

from models import ForecastRequest, ForecastResponse, CSVForecastRequest
from utils import create_future_dates, add_regressors, calculate_metrics

# Initialiser l'application
app = FastAPI(
    title="API de Prédiction des Ventes",
    description="API pour prédire les ventes des 3 prochains mois",
    version="1.0.0"
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle
try:
    model = joblib.load("prophet_model.pkl")
    print("Modèle chargé avec succès")
except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    model = None

@app.get("/")
async def root():
    return {
        "message": "API de Prédiction des Ventes",
        "status": "online",
        "endpoints": {
            "/predict": "POST - Prédire les ventes futures",
            "/predict-csv": "POST - Prédire à partir d'un CSV",
            "/health": "GET - Vérifier l'état de l'API"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=ForecastResponse)
async def predict_sales(request: ForecastRequest):
    """
    Prédire les ventes pour les périodes futures
    """
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Modèle non chargé")
        
        # Créer les dates futures
        future_df = create_future_dates(request.start_date, request.periods)
        
        # Ajouter les régresseurs
        future_enriched = add_regressors(future_df, include_target=False)
        
        # Faire la prédiction
        forecast = model.predict(future_enriched)
        
        # Préparer les résultats
        predictions = []
        for _, row in forecast.iterrows():
            predictions.append({
                "date": row['ds'].strftime('%Y-%m-%d'),
                "predicted_sales": float(row['yhat']),
                "predicted_lower": float(row['yhat_lower']) if 'yhat_lower' in row else None,
                "predicted_upper": float(row['yhat_upper']) if 'yhat_upper' in row else None
            })
        
        # Générer un graphique
        plt.figure(figsize=(12, 6))
        plt.plot(forecast['ds'], forecast['yhat'], label='Prédiction', color='blue', linewidth=2)
        
        if 'yhat_lower' in forecast.columns and 'yhat_upper' in forecast.columns:
            plt.fill_between(
                forecast['ds'], 
                forecast['yhat_lower'], 
                forecast['yhat_upper'],
                alpha=0.2, 
                color='blue',
                label='Intervalle de confiance'
            )
        
        plt.title(f'Prédiction des ventes pour les {request.periods} prochains jours', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Ventes prédites', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        # Convertir le graphique en base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return ForecastResponse(
            success=True,
            message=f"Prédiction générée pour {request.periods} jours",
            predictions=predictions,
            plot_data={"plot": plot_base64}
        )
        
    except Exception as e:
        return ForecastResponse(
            success=False,
            message="Erreur lors de la prédiction",
            error=str(e)
        )

@app.post("/predict-csv")
async def predict_from_csv(file: UploadFile = File(...)):
    """
    Prédire à partir d'un fichier CSV
    """
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Modèle non chargé")
        
        # Lire le fichier CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Renommer les colonnes si nécessaire
        column_mapping = {
            "Date Order was placed": "ds",
            "Total Retail Price for This Order": "y",
            "date": "ds",
            "sales": "y"
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        if 'ds' not in df.columns:
            raise ValueError("Colonne de date introuvable. Noms acceptés: 'Date Order was placed', 'date'")
        
        if 'y' not in df.columns:
            raise ValueError("Colonne de ventes introuvable. Noms acceptés: 'Total Retail Price for This Order', 'sales'")
        
        # Convertir les dates
        df['ds'] = pd.to_datetime(df['ds'])
        
        # Ajouter les régresseurs
        df_enriched = add_regressors(df, include_target=True)
        
        # Prédire
        forecast = model.predict(df_enriched)
        
        # Calculer les métriques si on a les vraies valeurs
        metrics = None
        if 'y' in df_enriched.columns and not df_enriched['y'].isna().all():
            metrics = calculate_metrics(
                df_enriched['y'].values, 
                forecast['yhat'].values[:len(df_enriched)]
            )
        
        # Préparer les résultats
        results = []
        for i, (_, row) in enumerate(forecast.iterrows()):
            result_item = {
                "date": row['ds'].strftime('%Y-%m-%d'),
                "predicted_sales": float(row['yhat']),
            }
            
            if i < len(df):
                result_item["actual_sales"] = float(df_enriched.iloc[i]['y']) if 'y' in df_enriched.columns else None
            
            results.append(result_item)
        
        # Générer un graphique comparatif
        plt.figure(figsize=(14, 7))
        
        # Tracer les prédictions
        plt.plot(forecast['ds'], forecast['yhat'], label='Prédictions', color='blue', linewidth=2)
        
        # Tracer les valeurs réelles si disponibles
        if 'y' in df_enriched.columns and not df_enriched['y'].isna().all():
            plt.scatter(df_enriched['ds'], df_enriched['y'], 
                       label='Ventes réelles', color='green', alpha=0.6, s=30)
        
        plt.title('Comparaison des ventes réelles et prédites', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Ventes', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        # Convertir en base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return {
            "success": True,
            "message": "Prédiction effectuée avec succès",
            "predictions": results[-10:],  # Dernières 10 prédictions
            "plot": plot_base64,
            "metrics": metrics,
            "total_predictions": len(results)
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.post("/predict-next-months")
async def predict_next_three_months():
    """
    Prédire automatiquement les 3 prochains mois à partir d'aujourd'hui
    """
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Modèle non chargé")
        
        # Date d'aujourd'hui
        start_date = datetime.now().strftime('%Y-%m-%d')
        
        # 3 mois = environ 90 jours
        future_df = create_future_dates(start_date, 90)
        future_enriched = add_regressors(future_df, include_target=False)
        
        # Prédiction
        forecast = model.predict(future_enriched)
        
        # Agréger par mois
        forecast['month'] = forecast['ds'].dt.to_period('M')
        monthly_forecast = forecast.groupby('month').agg({
            'yhat': 'sum',
            'yhat_lower': 'sum',
            'yhat_upper': 'sum'
        }).reset_index()
        
        monthly_forecast['month'] = monthly_forecast['month'].dt.strftime('%Y-%m')
        
        # Préparer la réponse
        predictions = []
        for _, row in monthly_forecast.iterrows():
            predictions.append({
                "month": row['month'],
                "predicted_sales": float(row['yhat']),
                "predicted_range": {
                    "lower": float(row['yhat_lower']),
                    "upper": float(row['yhat_upper'])
                }
            })
        
        return {
            "success": True,
            "message": "Prédiction des 3 prochains mois",
            "start_date": start_date,
            "monthly_predictions": predictions
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(e)
            }
        )