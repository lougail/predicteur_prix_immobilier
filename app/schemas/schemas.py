from pydantic import BaseModel, Field, field_validator
from typing import Literal

# Schéma pour les requêtes de prédiction directe
class PredictionRequest(BaseModel):
    surface_bati: float = Field(..., gt=0, le=10000, description="Surface bâtie (entre 0 et 10000 m²)")
    nombre_pieces: int = Field(..., gt=0, le=50, description="Nombre de pièces (entre 1 et 50)")
    type_local: str
    surface_terrain: float = Field(..., ge=0, le=10000, description="Surface terrain (entre 0 et 10000 m²)")
    nombre_lots: int = Field(..., ge=0, le=100, description="Nombre de lots (entre 0 et 100)")

    @field_validator('type_local')
    def validate_type_local(cls, v):
        if v not in ['Appartement', 'Maison']:
            raise ValueError('Type local must be either Appartement or Maison')
        return v

# Schéma pour les features imbriquées dans la requête dynamique
class PredictionFeatures(PredictionRequest):
    pass

# Schéma pour la requête dynamique (choix de la ville)
class DynamicPredictionRequest(BaseModel):
    ville: Literal["lille", "bordeaux"]
    features: PredictionFeatures

# Schéma pour la réponse de prédiction
class PredictionResponse(BaseModel):
    prix_m2_estime: float
    ville_modele: str
    model: str