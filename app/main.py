from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import predict
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="API Prédiction Prix Immobilier",
    description="API de prédiction des prix au m² pour les logements de 4 pièces",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware pour logguer chaque requête HTTP
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Autoriser toutes les origines (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes de prédiction
app.include_router(predict.router, prefix="", tags=["predictions"])

# Route racine pour vérifier que l'API fonctionne
@app.get("/", tags=["default"])
async def root():
    return {
        "message": "Bienvenue sur l'API de prédiction immobilière",
        "documentation": "/docs"
    }