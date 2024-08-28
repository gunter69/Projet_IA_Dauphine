# RAG JIRA

Mise en place d'un RAG pour l'analyse et la résolution de tickets JIRA.

## Installation

- Créer un environnement virtuel.

- Activer l'environnement virtuel avec `source venv/bin/activate` pour linux ou `venv\Scripts\activate` pour windows.

- Aller dans `rag_jira`.

- Puis installer les dépendances avec `pip install -e .`.

## Redis VectorStore

📖 **Documentation :** https://python.langchain.com/v0.2/docs/integrations/vectorstores/redis/

Déployer redis localement :
```console
docker run --name redis-jira -d -p 6379:6379 redis/redis-stack:latest
```

Arrêter / Rédémarrer le container :
```console
docker stop redis-jira
docker start redis-jira
```

💡 Installer [Redis Insight](https://redis.io/insight/) pour visualiser le contenu de la base.

## DEMO

- Avant de lancer le chatbot, faire une indexation des tickets jira :
```console
python src/service/indexation.py
```

- Pour lancer l'application streamlit :
```console
streamlit run src/app.py
```

### Questions pour la démo

___
I'm unable to successfully connect to the server and I get the following error message.
```java
server-unknown:>admin config server --uri http://localhost:9393 --username bob --password bobspwd Unable to contact XD Admin Server at 'http://localhost:9393'.
```
___
