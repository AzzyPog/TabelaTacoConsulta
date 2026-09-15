import json
import os
from pymongo import MongoClient
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'atlas-credentials.env'))

def popular_mongodb():
    caminho_json = 'taco.json'
    
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            alimentos = json.load(f)
            print(f"JSON carregado. Encontrados {len(alimentos)} alimentos.")
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_json} não foi encontrado.")
        sys.exit(1)

    uri_conexao = os.getenv("MONGODB_URI")
    if not uri_conexao:
        print("Erro: MONGODB_URI não encontrada no arquivo atlas-credentials.env")
        sys.exit(1)
    
    try:
        print(f"Conectando ao MongoDB em {uri_conexao}...")
        client = MongoClient(uri_conexao, serverSelectionTimeoutMS=5000)
        
        client.server_info() 
        print("Conectado com sucesso!")
        
    except Exception as e:
        print("\nErro ao conectar no MongoDB!")
        print("Certifique-se de que o MongoDB está rodando no seu computador (se for local).")
        print(f"Detalhes do erro: {e}")
        sys.exit(1)

    db = client["tabela_taco"]
    colecao = db["alimentos"]

    print("Limpando a coleção antiga (se houver)...")
    colecao.delete_many({})

    print("Inserindo novos dados...")
    resultado = colecao.insert_many(alimentos)
    
    print(f"\nSucesso! {len(resultado.inserted_ids)} itens foram populados no MongoDB.")
    print("Banco: 'tabela_taco' | Coleção: 'alimentos'")

if __name__ == '__main__':
    popular_mongodb()

