import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# Logger pour afficher les informations et erreurs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction utilitaire pour charger et valider un dataset CSV
def load_and_validate_dataset(file_path: Path) -> pd.DataFrame:
    required_columns = [
        'surface_bati', 'nombre_pieces', 'type_local',
        'surface_terrain', 'nombre_lots', 'prix_m2'
    ]
    try:
        df = pd.read_csv(file_path)
        # Vérifie la présence des colonnes nécessaires
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Colonnes manquantes: {missing_cols}")
        # Conversion des types
        for col in ['surface_bati', 'nombre_pieces', 'surface_terrain', 'nombre_lots', 'prix_m2']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement du dataset: {str(e)}")
        raise

# Classe pour prétraiter les features avant la prédiction
class FeatureProcessor:
    def __init__(self):
        self.required_features = ["surface_bati", "type_local", "nombre_lots"]
        self.optional_features = ["nombre_pieces", "surface_terrain"]
        self.max_values = {
            "surface_bati": 10000, "nombre_pieces": 50,
            "surface_terrain": 10000, "nombre_lots": 100
        }

    def validate_features(self, features: Dict[str, Any]) -> None:
        # Vérifie la présence des features requises
        missing = [f for f in self.required_features if f not in features]
        if missing:
            raise ValueError(f"Features requises manquantes : {', '.join(missing)}")
        # Ajoute les valeurs par défaut pour les optionnelles
        for feature in self.optional_features:
            features.setdefault(feature, 0)
        # Vérifie les types et valeurs
        for field in ["surface_bati", "surface_terrain", "nombre_lots"]:
            if not isinstance(features[field], (int, float)):
                raise TypeError(f"Le champ {field} doit être un nombre")
            if features.get(field, 0) < 0:
                raise ValueError("Les valeurs ne peuvent pas être négatives")
        if features["surface_bati"] == 0:
            raise ValueError("La surface bâtie ne peut pas être nulle")
        for field, max_value in self.max_values.items():
            if field in features and features[field] > max_value:
                raise ValueError(f"La valeur de {field} ne peut pas dépasser {max_value}")

    def prepare_features_for_prediction(self, features: Dict[str, Any]) -> pd.DataFrame:
        self.validate_features(features)
        features.setdefault("surface_terrain", 0)
        features.setdefault("nombre_pieces", 0)
        # Retourne un DataFrame prêt pour le modèle
        return pd.DataFrame([[
            float(features["surface_bati"]),
            float(features["surface_terrain"]),
            float(features["nombre_lots"])
        ]], columns=['Surface reelle bati', 'Surface terrain', 'Nombre de lots'])

    def validate_type_local(self, type_local: str) -> None:
        if type_local not in ["Appartement", "Maison"]:
            raise ValueError("Type de local invalide. Valeurs acceptées : Appartement, Maison")

    def validate_ville(self, ville: str) -> None:
        if ville.lower() not in ["lille", "bordeaux"]:
            raise ValueError("Ville invalide. Valeurs acceptées : lille, bordeaux")