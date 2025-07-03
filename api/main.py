from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from typing import Optional, Literal
import os

# Définition du chemin du dossier models
MODEL_DIR = os.path.join(os.getcwd(), "models")

# Chargement du modèle de prédiction pour les appartements sur Lille et de ses scalers
model_appartements = joblib.load(os.path.join(MODEL_DIR, "model_appartements.pkl"))
scaler_x_appartements = joblib.load(os.path.join(MODEL_DIR, "scaler_x_appartements.pkl"))
scaler_y_appartements = joblib.load(os.path.join(MODEL_DIR, "scaler_y_appartements.pkl"))

# Chargement du modèle de prédiction pour les maisons sur Lille et de ses scalers
model_maisons = joblib.load(os.path.join(MODEL_DIR, "model_maisons.pkl"))
scaler_x_maisons = joblib.load(os.path.join(MODEL_DIR, "scaler_x_maisons.pkl"))
scaler_y_maisons = joblib.load(os.path.join(MODEL_DIR, "scaler_y_maisons.pkl"))

# Création d'un modèle Pydantic pour la validation des requètes POST
class PredictionRequest(BaseModel):
    '''Schema pour les predictions directes: /predict/lille et /predict/bordeaux'''
    surface_bati: float = Field(..., gt=0, le=10000, description="Surface Batie (float entre 0 et 10000m²)")
    nombre_pieces: int = Field(..., gt=0, le=50, description="Nombre de pièces (int entre 0 et 50)")
    type_local: Literal["Appartement", "Maison"] = Field(..., description="Type de local (str : 'Appartement' ou 'Maison')")
    surface_terrain: float = Field(0.0, ge=0, le=10000, description="Surface du terrain (float entre 0 et 10000)")
    nombre_lots: int = Field(..., gt=0, le=100, description="Nombre de lots (int entre 0 et 100)")

class DynamicPredictionRequest(BaseModel):
    ville: Literal["lille", "bordeaux"] = Field(..., description="Nom de la ville (lille ou bordeaux)")
    features: PredictionRequest

def predict_price(request: PredictionRequest, ville_modele: str):
    # Vérification du type_local
    if request.type_local not in ["Appartement", "Maison"]:
        raise HTTPException(
            status_code=400,
            detail="Le champ 'type_local' doit être 'Appartement' ou 'Maison'"
        )
    if request.type_local == "Appartement":
        model = model_appartements
        scaler_x = scaler_x_appartements
        scaler_y = scaler_y_appartements
    else:
        model = model_maisons
        scaler_x = scaler_x_maisons
        scaler_y = scaler_y_maisons
        
    features = [[request.surface_bati, request.surface_terrain, request.nombre_lots]]
    features_scaled = scaler_x.transform(features)
    pred_scaled = model.predict(features_scaled)
    prix_m2 = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))[0, 0]
    return {
        "estimation_prix_m2": float(prix_m2),
        "ville": ville_modele,
        "model": type(model).__name__
    }
    
app = FastAPI()

@app.post("/predict/lille")
async def predict_lille(request: PredictionRequest):
    return predict_price(request, ville_modele="Lille")

@app.post("/predict/bordeaux")
async def predict_bordeaux(request: PredictionRequest):
    return predict_price(request, ville_modele="Bordeaux")

@app.post("/predict")
def predict(features: DynamicPredictionRequest):
    if features.ville not in ["lille", "bordeaux"]:
        raise HTTPException(status_code=400, detail="Ville non reconnue")
    if features.ville == "lille":
        return predict_price(features.features, ville_modele="Lille")
    else:
        return predict_price(features.features, ville_modele="Bordeaux")