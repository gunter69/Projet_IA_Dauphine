"""
Module de service d'indexation
"""
import csv
from typing import List

from langchain_core.documents import Document
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from entrepot.jira_issues import IssueJira, EntrepotIssuesJira, Type, Status, Resolution
from entrepot.embeddings import EntrepotEmbeddings


class ServiceIndexation:
    """Service d'indexation"""

    def collecter_les_issues(self, path: str) -> EntrepotIssuesJira:
        """Collecte les issues depuis un fichier csv et les stocke dans l'entrepôt des issues Jira"""
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            entrepot_issues = EntrepotIssuesJira()
            for row in reader:
                issue = IssueJira(
                            row["id"],
                            row["title"],
                            row["description"],
                            Type(row["type"]),
                            Status(row["status"]),
                            Resolution(row["resolution"]),
                            row["last_updated"],
                            row["comment"]
                        )
                entrepot_issues.ajouter_issue(issue)

        return entrepot_issues

    def stocker_les_documents_dans_vector_store(
            self, entrepot_issues: EntrepotIssuesJira) -> EntrepotEmbeddings:
        """Stocke les documents langchain dans l'entrepôt d'embeddings"""
        documents: List[Document] = []
        issues: List[IssueJira] = entrepot_issues.obtenir_toutes_les_issues()

        for issue in issues:
            documents.append(issue.transforme_en_document_langchain())

        entrepot_embeddings = EntrepotEmbeddings(embedding_model=HuggingFaceEmbeddings())
        entrepot_embeddings.ajout_documents(documents)

        return entrepot_embeddings