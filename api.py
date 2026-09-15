import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('atlas-credentials.env')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["tabela_taco"]
colecao = db["alimentos"]

@app.get("/api/buscar")
def buscar_alimento(q: str = ""):
    if not q:
        return []
    
    filtro = {"descricao": {"$regex": q, "$options": "i"}}
    resultados = list(colecao.find(filtro, {"_id": 0}).limit(10))
    return resultados
