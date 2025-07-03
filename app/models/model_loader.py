import joblib
from pathlib import Path

# Classe pour charger les modèles et scalers
class ModelLoader:
    def __init__(self):
        # Chemin vers le dossier models à la racine du projet
        self.root_path = Path(__file__).parent.parent.parent
        self.models_path = self.root_path / "models"
        self.load_models()

    def load_models(self):
        # Charge tous les modèles et scalers nécessaires
        required_files = [
            "model_appartements.pkl", "model_maisons.pkl",
            "scaler_x_appartements.pkl", "scaler_x_maisons.pkl",
            "scaler_y_appartements.pkl", "scaler_y_maisons.pkl"
        ]
        if not self.models_path.exists():
            raise RuntimeError(f"Le dossier models n'existe pas : {self.models_path}")
        missing_files = [f for f in required_files if not (self.models_path / f).exists()]
        if missing_files:
            raise RuntimeError(f"Fichiers manquants : {', '.join(missing_files)}")
        # Chargement des modèles et scalers
        self.model_appartements = joblib.load(self.models_path / "model_appartements.pkl")
        self.model_maisons = joblib.load(self.models_path / "model_maisons.pkl")
        self.scaler_x_appartements = joblib.load(self.models_path / "scaler_x_appartements.pkl")
        self.scaler_y_appartements = joblib.load(self.models_path / "scaler_y_appartements.pkl")
        self.scaler_x_maisons = joblib.load(self.models_path / "scaler_x_maisons.pkl")
        self.scaler_y_maisons = joblib.load(self.models_path / "scaler_y_maisons.pkl")

    def get_model_and_scalers(self, type_local: str):
        # Retourne le modèle et les scalers selon le type de bien
        if type_local == "Appartement":
            return (
                self.model_appartements,
                self.scaler_x_appartements,
                self.scaler_y_appartements,
                "RandomForestRegressor"
            )
        elif type_local == "Maison":
            return (
                self.model_maisons,
                self.scaler_x_maisons,
                self.scaler_y_maisons,
                "RandomForestRegressor"
            )
        else:
            raise ValueError(f"Type de bien non reconnu: {type_local}")