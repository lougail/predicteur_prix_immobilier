from fastapi import FastAPI

app = FastAPI(
    title="API Prédiction Prix Immobilier",
    description="API de prédiction des prix au m² pour les logements de 4 pièces",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de prédiction immobilière"}