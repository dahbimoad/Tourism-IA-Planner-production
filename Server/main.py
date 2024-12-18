from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuration de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # On autorise l'accès depuis localhost:5173
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permet tous les types d'en-têtes
)


@app.get("/")
def read_root():
    return {"message": "salam 3alaykummmmm"}
