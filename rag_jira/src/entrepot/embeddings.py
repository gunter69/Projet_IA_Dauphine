"""
Module d'entrepôt des embeddings
"""
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

class EntrepotEmbeddings:
    """Classe représentant l'entrepôt des embeddings"""
    def __init__(self, embedding_model: Embeddings):
        self.client_chroma = Chroma(
            persist_directory="./chromadb",
            embedding_function=embedding_model
        )
        self.embedding = embedding_model

    def ajout_documents(self, documents: List[Document]) -> None:
        """Ajoute des documents à l'entrepôt"""
        self.client_chroma.from_documents(documents=documents)

    def recherche_embeddings(self, query: str) -> List[Document]:
        """Recherche des documents dans l'entrepôt"""
        return self.client_chroma.similarity_search(query=query, k=3)

