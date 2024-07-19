# RAG JIRA

Mise en place d'un RAG pour l'analyse de tickets JIRA.

## Installation

- Créer un environnement virtuel

- Activer l'environnement virtuel avec `source venv/bin/activate` pour linux ou `venv\Scripts\activate` pour windows

- Aller dans `rag_jira`

- Puis installer les dépendances avec `pip install -e .`

- Ajouter un fichier d'environnements `.env` à la racine du projet avec les informations de connexion à la base de données.

```
DB_HOST=<db_host>
DB_PORT=<db_port>
DB_USER=<db_user>
DB_PASSWORD=<db_password>
DB_DATABASE=<db_database>
```