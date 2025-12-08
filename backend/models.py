from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import pandas as pd

class ForecastRequest(BaseModel):
    """Modèle pour les requêtes de prédiction"""
    start_date: str
    periods: int = 90  # 3 mois par défaut
    include_history: bool = False
    
class CSVForecastRequest(BaseModel):
    """Modèle pour les prédictions à partir de CSV"""
    file_content: str  # Contenu du fichier en base64

class ForecastResponse(BaseModel):
    """Modèle pour les réponses"""
    success: bool
    message: str
    predictions: Optional[List[dict]] = None
    plot_data: Optional[dict] = None
    error: Optional[str] = None