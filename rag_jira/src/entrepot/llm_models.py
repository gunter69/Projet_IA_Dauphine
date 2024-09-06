"""
Module d'entrepot des LLMs
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Parametres:
    """Classe représentant les paramètres à passer au modèle LLM"""
    temperature: float = 0.0
    top_p: float = 0.9
    top_k: int = 50
    max_new_tokens: int = 500
    repetition_penalty: float = 1.2

@dataclass
class LLM:
    """Classe représentant un LLM"""
    nom: str
    url: str
    parametres: Parametres

    def description(self):
        """Retourne une description du LLM"""
        return (
            f"Modèle: {self.nom}\n"
            f"URL: {self.url}\n"
            f"Paramètres: {self.parametres}"
        )

class EntrepotLLM:
    """Classe représentant l'entrepôt des LLMs"""

    def __init__(self):
        self.models = []

    def ajouter_modele(self, llm: LLM) -> None:
        """Ajoute un LLM à l'entrepôt"""
        self.models.append(llm)

    def supprimer_modele(self, nom: str) -> None:
        """Supprime un LLM de l'entrepôt"""
        self.models = [model for model in self.models if model.nom != nom]

    def obtenir_modele(self, nom: str) -> LLM:
        """Retourne un LLM de l'entrepôt"""
        for model in self.models:
            if model.nom == nom:
                return model
        raise ValueError(f"Le modèle {nom} n'existe pas")

    def lister_modeles(self) -> List[LLM]:
        """Retourne la liste des LLMs de l'entrepôt"""
        return self.models
