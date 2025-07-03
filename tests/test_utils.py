import pytest
import pandas as pd
from pathlib import Path
from app.utils import FeatureProcessor, load_and_validate_dataset

# ---
# Fixtures : petits jeux de données pour les tests
# ---
@pytest.fixture
def sample_dataset():
    # Jeu de données simple pour tester la validation
    return pd.DataFrame({
        'surface_bati': [100, 120],
        'nombre_pieces': [4, 4],
        'type_local': ['Appartement', 'Maison'],
        'surface_terrain': [0, 500],
        'nombre_lots': [1, 0],
        'prix_m2': [3500, 4200]
    })

@pytest.fixture
def feature_processor():
    # Crée un processeur de features pour les tests
    return FeatureProcessor()

# ---
# Tests sur la validation et la préparation des features
# ---
def test_validate_features_ok(feature_processor):
    # Test avec des données valides
    features = {
        "surface_bati": 100,
        "nombre_pieces": 4,
        "type_local": "Appartement",
        "surface_terrain": 0,
        "nombre_lots": 1
    }
    feature_processor.validate_features(features)

# Test d'erreur si un champ requis est manquant
def test_validate_features_missing(feature_processor):
    features = {
        "nombre_pieces": 4,
        "type_local": "Appartement",
        "surface_terrain": 0,
        "nombre_lots": 1
    }
    with pytest.raises(ValueError):
        feature_processor.validate_features(features)

# Test d'erreur si une valeur est négative
def test_validate_features_negative(feature_processor):
    features = {
        "surface_bati": -100,
        "nombre_pieces": 4,
        "type_local": "Appartement",
        "surface_terrain": 0,
        "nombre_lots": 1
    }
    with pytest.raises(ValueError):
        feature_processor.validate_features(features)

# Test de la préparation des features pour la prédiction
def test_prepare_features_for_prediction(feature_processor):
    features = {
        "surface_bati": 100,
        "nombre_pieces": 4,
        "type_local": "Appartement",
        "surface_terrain": 0,
        "nombre_lots": 1
    }
    X = feature_processor.prepare_features_for_prediction(features)
    assert isinstance(X, pd.DataFrame)
    assert X.shape == (1, 3)  # 1 ligne, 3 colonnes

# Test de la validation du type_local
def test_validate_type_local(feature_processor):
    feature_processor.validate_type_local("Appartement")
    feature_processor.validate_type_local("Maison")
    with pytest.raises(ValueError):
        feature_processor.validate_type_local("Bureau")

# Test de la validation de la ville
def test_validate_ville(feature_processor):
    feature_processor.validate_ville("lille")
    feature_processor.validate_ville("bordeaux")
    with pytest.raises(ValueError):
        feature_processor.validate_ville("paris")

# ---
# Test sur la fonction de chargement et validation d'un dataset CSV
# ---
def test_load_and_validate_dataset_ok(sample_dataset, tmp_path):
    # Sauvegarde le jeu de données dans un fichier temporaire
    file_path = tmp_path / "test.csv"
    sample_dataset.to_csv(file_path, index=False)
    df = load_and_validate_dataset(file_path)
    assert isinstance(df, pd.DataFrame)
    assert set(['surface_bati', 'nombre_pieces', 'type_local']).issubset(df.columns)

# Test d'erreur si une colonne est manquante
def test_load_and_validate_dataset_missing_col(sample_dataset, tmp_path):
    file_path = tmp_path / "test.csv"
    # On enlève une colonne
    sample_dataset.drop(columns=['surface_bati']).to_csv(file_path, index=False)
    with pytest.raises(ValueError):
        load_and_validate_dataset(file_path)