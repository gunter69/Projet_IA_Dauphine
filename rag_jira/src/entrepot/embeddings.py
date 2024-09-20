"""
Module d'entrepôt des embeddings
"""
from typing import List
from langchain_community.vectorstores.redis import Redis
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

class EntrepotEmbeddings:
    """Classe représentant l'entrepôt des embeddings"""
    def __init__(self, embedding_model: Embeddings):
        self.client_redis = Redis(
            redis_url="redis://localhost:6379",
            embedding=embedding_model,
            index_name="jira",
            index_schema="src/entrepot/redis_schema.yaml"
        )
        self.embeddings = embedding_model

    def ajout_documents(self, documents: List[Document]) -> None:
        """Ajoute des documents à l'entrepôt"""
        self.client_redis.add_documents(documents=documents)

    def recherche_embeddings(self, query: str) -> List[Document]:
        """Recherche des documents dans l'entrepôt"""
        return self.client_redis.similarity_search(query=query, k=1)
