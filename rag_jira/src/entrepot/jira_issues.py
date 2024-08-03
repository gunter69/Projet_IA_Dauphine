"""
Module d'entrepot pour les issues JIRA
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional
from langchain_core.documents import Document

class Type(Enum):
    """Classe représentant le type d'une issue Jira"""
    BUG = "Bug"
    SUPPORT_REQUEST = "Support Request"
    QUESTION = "Question"
    PROBLEM_TICKET = "Problem Ticket"
    INCIDENT = "Incident"

class Status(Enum):
    """Classe représentant le status d'une issue Jira"""
    CLOSED = "Closed"
    RESOLVED = "Resolved"
    DONE = "Done"
    COMPLETE = "Complete"

class Resolution(Enum):
    """Classe représentant la résolution d'une issue Jira"""
    FIXED = "Fixed"
    DONE = "Done"
    SUPPORT_REQUEST = "Support Request"
    COMPLETE = "Complete"
    ANSWERED = "Answered"
    COMPLETED = "Completed"
    COMMUNITY_ANSWERED = "Community Answered"
    RESOLVED = "Resolved"

@dataclass
class IssueJira:
    """Classe représentant une issue Jira"""
    id: str
    title: str
    description: str
    type: Type
    status: Status
    resolution: Resolution
    last_updated: date
    comment: str

    def transforme_en_document_langchain(self) -> Document:
        """Transforme une issue en document langchain"""
        return Document(
            page_content = self.description,
            metadata = {
                "id": self.id,
                "title": self.title,
                "type": self.type,
                "status": self.status,
                "resolution": self.resolution,
                "last_updated": self.last_updated,
                "comment": self.comment
            }
        )

class EntrepotIssuesJira:
    """Classe représentant l'entrepôt des issues Jira"""

    def __init__(self):
        self.issues : List[IssueJira] = []

    def obtenir_toutes_les_issues(self) -> List[IssueJira]:
        """Retourne toutes les issues"""
        return self.issues

    def ajouter_issue(self, issue: IssueJira):
        """Ajoute une issue à l'entrepôt"""
        self.issues.append(issue)

    def obtenir_issue_par_id(self, id_issue: str) -> Optional[IssueJira]:
        """Retourne une issue par son id"""
        for issue in self.issues:
            if issue.id == id_issue:
                return issue
        return None

    def obtenir_issues_par_type(self, type_issue: Type) -> List[IssueJira]:
        """Retourne les issues d'un type donné"""
        issues_par_type = []
        for issue in self.issues:
            if issue.type == type_issue:
                issues_par_type.append(issue)
        return issues_par_type

    def obtenir_issues_par_status(self, status: Status) -> List[IssueJira]:
        """Retourne les issues d'un status donné"""
        issues_par_status = []
        for issue in self.issues:
            if issue.status == status:
                issues_par_status.append(issue)
        return issues_par_status

    def obtenir_issues_par_resolution(self, resolution: Resolution) -> List[IssueJira]:
        """Retourne les issues d'une résolution donnée"""
        issues_par_resolution = []
        for issue in self.issues:
            if issue.resolution == resolution:
                issues_par_resolution.append(issue)
        return issues_par_resolution

    def supprimer_issue_par_id(self, id_issue: str) -> None:
        """Supprime une issue par son id"""
        self.issues = [issue for issue in self.issues if issue.id != id_issue]
