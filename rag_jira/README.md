# RAG JIRA

Mise en place d'un RAG pour l'analyse et la résolution de tickets JIRA.

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

Documentation : https://python.langchain.com/v0.2/docs/integrations/vectorstores/redis/

Déployer redis localement :
```console
docker run --name redis-jira -d -p 6379:6379 redis/redis-stack:latest
```

Arrêter le container :
```console
docker stop redis-jira
```

Redémarrer le container :
```console
docker start redis-jira
```

## DEMO

Question utilisateur :
```
I'm unable to successfully connect to the server and I get the following error message.   {code:java} server-unknown:>admin config server --uri http://localhost:9393 --username bob --password bobspwd Unable to contact XD Admin Server at 'http://localhost:9393'. {code}
```