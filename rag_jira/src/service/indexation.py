"""
Module de service d'indexation
"""
import csv
from typing import List

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from entrepot.jira_issues import IssueJira, EntrepotIssuesJira, Type, Status, Resolution
from entrepot.embeddings import EntrepotEmbeddings

class ServiceIndexation:
    """Service d'indexation"""

    def collecter_les_issues(self, path: str) -> EntrepotIssuesJira:
        """Collecte les issues depuis un fichier csv
        et les stocke dans l'entrepôt des issues Jira"""
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            entrepot_issues = EntrepotIssuesJira()
            for row in reader:
                print(row)
                issue = IssueJira(
                            row["ID"],
                            row["Title"],
                            row["Description"],
                            Type(row["Type"]),
                            Status(row["Status"]),
                            Resolution(row["Resolution"]),
                            row["Last_Updated"],
                            row["Comment"]
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

        entrepot_embeddings = EntrepotEmbeddings(
            embedding_model=HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        )
        entrepot_embeddings.ajout_documents(documents)

        return entrepot_embeddings
