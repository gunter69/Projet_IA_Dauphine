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
    entrepot_embeddings = EntrepotEmbeddings(
        embedding_model=HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    )
    entrepot_issues = EntrepotIssuesJira()

    def collecter_les_issues(self, path: str) -> EntrepotIssuesJira:
        """Collecte les issues depuis un fichier csv
        et les stocke dans l'entrepôt des issues Jira"""
        csv.field_size_limit(10**7)
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
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
                self.entrepot_issues.ajouter_issue(issue)

        return self.entrepot_issues

    def stocker_les_documents_dans_vector_store(self) -> EntrepotEmbeddings:
        """Stocke les documents langchain dans l'entrepôt d'embeddings"""
        documents: List[Document] = []
        issues: List[IssueJira] = self.entrepot_issues.obtenir_toutes_les_issues()

        for issue in issues:
            documents.append(issue.transforme_en_document_langchain())

        self.entrepot_embeddings = EntrepotEmbeddings(
            embedding_model=HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        )
        self.entrepot_embeddings.ajout_documents(documents)

        return self.entrepot_embeddings

if __name__ == "__main__":
    ## Indexation
    service_indexation = ServiceIndexation()
    service_indexation.collecter_les_issues("xp/jira_issues.csv")
    service_indexation.stocker_les_documents_dans_vector_store()
