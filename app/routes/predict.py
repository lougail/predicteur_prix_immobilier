import numpy as np
from fastapi import APIRouter, HTTPException
from ..models.model_loader import ModelLoader
from ..schemas.schemas import PredictionRequest, DynamicPredictionRequest, PredictionResponse
from ..utils import FeatureProcessor
import logging

# On configure le logger pour afficher les messages de debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Création du routeur FastAPI pour regrouper les routes de prédiction
router = APIRouter()

# On crée une seule instance de ModelLoader et FeatureProcessor pour tout le module
model_loader = ModelLoader()
feature_processor = FeatureProcessor()

# Endpoint pour prédire le prix à Lille
@router.post(
    "/predict/lille",
    response_model=PredictionResponse,
    summary="Prédiction du prix au m² à Lille",
    description="Prédit le prix au m² pour un bien immobilier à Lille à partir des caractéristiques fournies.",
)
async def predict_lille(
    request: PredictionRequest
):
    """
    Prédit le prix au m² pour un bien à Lille.

    **Paramètres**:
    - **request**: PredictionRequest
        - surface_bati: float — Surface bâtie du bien en m²
        - surface_terrain: float — Surface du terrain en m²
        - nombre_lots: int — Nombre de lots
        - type_local: str — Type de bien (Maison, Appartement, etc.)
    """
    try:
        # On vérifie que le type de bien est correct
        feature_processor.validate_type_local(request.type_local)
        
        # On vérifie que les données sont valides
        features_dict = request.model_dump()
        feature_processor.validate_features(features_dict)
        
        # On fait la prédiction
        prediction = predict_price(request, "lille")
        
        # On retourne la réponse formatée
        return {
            "prix_m2_estime": round(prediction, 2),
            "ville_modele": "Lille",
            "model": "RandomForestRegressor"
        }
    except ValueError as ve:
        # Erreur de validation utilisateur
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        # Erreur inattendue
        logger.error(f"Error in Lille prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint pour prédire le prix à Bordeaux
@router.post(
    "/predict/bordeaux",
    response_model=PredictionResponse,
    summary="Prédiction du prix au m² à Bordeaux",
    description="Prédit le prix au m² pour un bien immobilier à Bordeaux à partir des caractéristiques fournies.",
)
async def predict_bordeaux(
    request: PredictionRequest
):
    """
    Prédit le prix au m² pour un bien à Bordeaux.

    **Paramètres**:
    - **request**: PredictionRequest
        - surface_bati: float — Surface bâtie du bien en m²
        - surface_terrain: float — Surface du terrain en m²
        - nombre_lots: int — Nombre de lots
        - type_local: str — Type de bien (Maison, Appartement, etc.)
    """
    try:
        # On vérifie que le type de bien est correct
        feature_processor.validate_type_local(request.type_local)
        
        # On vérifie que les données sont valides
        features_dict = request.model_dump()
        feature_processor.validate_features(features_dict)
        
        # On fait la prédiction
        prediction = predict_price(request, "bordeaux")
        return {
            "prix_m2_estime": round(prediction, 2),
            "ville_modele": "Bordeaux",
            "model": "RandomForestRegressor"
        }
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in Bordeaux prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint dynamique pour choisir la ville
@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Prédiction dynamique du prix au m²",
    description="Prédit le prix au m² pour un bien immobilier en fonction de la ville et des caractéristiques fournies.",
)
async def predict_dynamic(
    request: DynamicPredictionRequest
):
    """
    Prédit le prix au m² pour un bien, ville au choix (Lille ou Bordeaux).

    **Paramètres**:
    - **request**: DynamicPredictionRequest
        - ville: str — Ville pour laquelle effectuer la prédiction ('lille' ou 'bordeaux')
        - features: PredictionRequest — Caractéristiques du bien :
            - surface_bati: float — Surface bâtie du bien en m²
            - surface_terrain: float — Surface du terrain en m²
            - nombre_lots: int — Nombre de lots
            - type_local: str — Type de bien (Maison, Appartement, etc.)
    """
    try:
        # On vérifie que la ville est bien supportée
        if request.ville.lower() not in ["lille", "bordeaux"]:
            raise HTTPException(
                status_code=400,
                detail="Ville must be either 'lille' or 'bordeaux'"
            )

        # On fait la prédiction
        prediction = predict_price(request.features, request.ville)
        
        return {
            "prix_m2_estime": round(prediction, 2),
            "ville_modele": request.ville.capitalize(),
            "model": "RandomForestRegressor"
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Fonction utilitaire pour faire la prédiction
# Elle est utilisée par tous les endpoints ci-dessus
# Elle prend les données de l'utilisateur et la ville, et retourne le prix prédit

def predict_price(features: PredictionRequest, ville: str) -> float:
    """Fonction utilitaire pour la prédiction"""
    try:
        # Vérifie que la ville est correcte
        feature_processor.validate_ville(ville)
        
        logger.debug(f"Starting prediction for {ville} with features: {features}")

        # Récupère le bon modèle/scaler selon la ville et le type de bien
        logger.debug("Getting model and scalers...")
        model, scaler_x, scaler_y, _ = model_loader.get_model_and_scalers(
            ville=ville,
            type_local=features.type_local
        )
        
        # Prépare les données utilisateur pour le modèle
        logger.debug("Preparing features...")
        X = feature_processor.prepare_features_for_prediction(features.model_dump())
        logger.debug(f"Prepared features shape: {X.shape}")

        # Met à l'échelle les données comme lors de l'entraînement
        logger.debug("Scaling features...")
        x_scaled = scaler_x.transform(X)
        logger.debug(f"Scaled features shape: {x_scaled.shape}")

        # Fait la prédiction (prix au m², mais encore à l'échelle du modèle)
        logger.debug("Making prediction...")
        y_scaled = model.predict(x_scaled).reshape(-1, 1)
        logger.debug(f"Raw prediction: {y_scaled}")

        # Remet la prédiction à l'échelle réelle
        logger.debug("Inverse transforming prediction...")
        final_prediction = float(scaler_y.inverse_transform(y_scaled)[0][0])
        logger.debug(f"Final prediction: {final_prediction}")

        return final_prediction

    except Exception as e:
        logger.error(f"Error in predict_price: {str(e)}")
        raise