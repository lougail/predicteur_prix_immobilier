from fastapi.testclient import TestClient
from app.main import app

# Création d'un client de test pour simuler des requêtes à l'API
client = TestClient(app)

# Test de la route racine (GET /)
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200  # Vérifie que la réponse est OK
    assert "message" in response.json()  # Vérifie que le message de bienvenue est présent

# Test de la prédiction pour Lille (POST /predict/lille)
def test_predict_lille():
    response = client.post(
        "/predict/lille",
        json={
            "surface_bati": 100,
            "nombre_pieces": 4,
            "type_local": "Appartement",
            "surface_terrain": 0,
            "nombre_lots": 1
        }
    )
    assert response.status_code == 200  # La prédiction doit réussir
    data = response.json()
    assert data["ville_modele"] == "Lille"  # Vérifie la ville dans la réponse

# Test de la prédiction pour Bordeaux (POST /predict/bordeaux)
def test_predict_bordeaux():
    response = client.post(
        "/predict/bordeaux",
        json={
            "surface_bati": 120,
            "nombre_pieces": 4,
            "type_local": "Maison",
            "surface_terrain": 500,
            "nombre_lots": 0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ville_modele"] == "Bordeaux"

# Test de la prédiction dynamique (POST /predict)
def test_predict_dynamic():
    response = client.post(
        "/predict",
        json={
            "ville": "lille",
            "features": {
                "surface_bati": 110,
                "nombre_pieces": 4,
                "type_local": "Maison",
                "surface_terrain": 300,
                "nombre_lots": 2
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ville_modele"] == "Lille"

# Test d'erreur si le type_local est invalide
def test_invalid_type_local():
    response = client.post(
        "/predict/lille",
        json={
            "surface_bati": 100,
            "nombre_pieces": 4,
            "type_local": "Bureau",  # Type non accepté
            "surface_terrain": 0,
            "nombre_lots": 1
        }
    )
    assert response.status_code == 422  # Erreur de validation attendue

# Test d'erreur si un champ requis est manquant
def test_missing_fields():
    response = client.post(
        "/predict/lille",
        json={
            "surface_bati": 100,
            # "nombre_pieces" manquant
            "type_local": "Appartement",
            "surface_terrain": 0,
            "nombre_lots": 1
        }
    )
    assert response.status_code == 422  # Erreur de validation attendue

# Test d'erreur si la ville n'est pas supportée dans la prédiction dynamique
def test_invalid_ville():
    response = client.post(
        "/predict",
        json={
            "ville": "paris",  # Ville non supportée
            "features": {
                "surface_bati": 100,
                "nombre_pieces": 4,
                "type_local": "Appartement",
                "surface_terrain": 0,
                "nombre_lots": 1
            }
        }
    )
    assert response.status_code == 422  # Erreur de validation attendue