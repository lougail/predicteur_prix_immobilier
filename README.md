# 🏠 Prédicteur de Prix Immobilier - API REST

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com)
[![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org)

## 📋 Description

API REST développée avec FastAPI pour prédire le **prix au m²** des biens immobiliers à **Lille** et **Bordeaux** basée sur les données réelles de transactions immobilières françaises (DVF 2022).

Cette API utilise des modèles de Machine Learning (Random Forest, XGBoost) entraînés sur les données des logements de 4 pièces pour fournir des estimations fiables du prix au m².

## 🎯 Fonctionnalités

- **Prédiction pour Lille** : `/predict/lille`
- **Prédiction pour Bordeaux** : `/predict/bordeaux` 
- **Prédiction dynamique** : `/predict` (choix de la ville)
- **Modèles séparés** : Appartements et Maisons
- **Validation automatique** des données d'entrée
- **Documentation interactive** : `/docs`
- **Tests unitaires** complets

## 🏗️ Structure du Projet

```
├── app/                      # Code source de l'API FastAPI
│   ├── main.py              # Point d'entrée de l'application
│   ├── models/              # Chargement des modèles ML
│   ├── routes/              # Endpoints de l'API
│   ├── schemas/             # Validation Pydantic
│   └── utils.py             # Utilitaires et preprocessing
├── models/                   # Modèles ML et scalers sauvegardés
│   ├── model_appartements.pkl
│   ├── model_maisons.pkl
│   └── scaler_*.pkl
├── notebooks/               # Études et modélisation
│   ├── phase_1_lille.ipynb
│   └── phase_2_bordeaux.ipynb
├── tests/                   # Tests unitaires
├── data/                    # Données (non versionnées)
└── requirements.txt         # Dépendances Python
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.13+
- pip

### Installation
```bash
# Cloner le repository
git clone <votre-repo-url>
cd Projet_Individuel-Prediction_du_prix_immobilier_en_France

# Créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement de l'API
```bash
# Démarrer le serveur FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible à : `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

## 📊 Utilisation de l'API

### Prédiction pour Lille
```bash
curl -X POST "http://localhost:8000/predict/lille" \
     -H "Content-Type: application/json" \
     -d '{
       "surface_bati": 100,
       "nombre_pieces": 4,
       "type_local": "Appartement",
       "surface_terrain": 0,
       "nombre_lots": 1
     }'
```

### Prédiction dynamique
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "ville": "bordeaux",
       "features": {
         "surface_bati": 120,
         "nombre_pieces": 4,
         "type_local": "Maison",
         "surface_terrain": 300,
         "nombre_lots": 2
       }
     }'
```

### Réponse type
```json
{
  "prix_m2_estime": 3850.42,
  "ville_modele": "Lille",
  "model": "RandomForestRegressor"
}
```

## 🧪 Tests

```bash
# Lancer tous les tests
python -m pytest

# Tests avec couverture
python -m pytest --cov=app

# Tests verbeux
python -m pytest -v
```

## 📈 Modèles Utilisés

- **Algorithmes** : Random Forest, XGBoost, Decision Tree, Linear Regression
- **Données d'entraînement** : DVF 2022 (Lille et Bordeaux)
- **Filtrage** : Logements 4 pièces uniquement
- **Preprocessing** : StandardScaler pour features et target
- **Évaluation** : MSE (Mean Squared Error)

## 🔍 Variables d'Entrée

| Variable | Type | Description | Validation |
|----------|------|-------------|------------|
| `surface_bati` | float | Surface bâtie (m²) | > 0, ≤ 10000 |
| `nombre_pieces` | int | Nombre de pièces | > 0, ≤ 50 |
| `type_local` | str | Type de bien | "Appartement" ou "Maison" |
| `surface_terrain` | float | Surface terrain (m²) | ≥ 0, ≤ 10000 |
| `nombre_lots` | int | Nombre de lots | ≥ 0, ≤ 100 |

## 📊 Performances des Modèles

### Appartements (Lille)
- Random Forest: MSE optimal
- Performances testées sur données de validation

### Maisons (Lille)
- Random Forest: Meilleure généralisation
- Adapté aux spécificités des maisons

## 🔧 Configuration

L'API utilise les modèles pré-entraînés stockés dans le dossier `models/`. 
Les paramètres de l'API peuvent être modifiés dans `app/main.py`.

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Projet sous licence MIT. Voir `LICENSE` pour plus d'informations.

## 👨‍💻 Auteur

Développé dans le cadre d'un projet de formation en Data Science & Machine Learning.

---

**Note** : Les données DVF ne sont pas incluses dans le repository pour des raisons de taille et de confidentialité.
