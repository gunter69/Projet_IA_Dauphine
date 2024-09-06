# RAG JIRA

> Mise en place d'un RAG pour l'analyse et la résolution de tickets JIRA.

- [RAG JIRA](#rag-jira)
  - [ℹ️ À propos](#ℹ️-à-propos)
    - [🧱 Structure du projet](#-structure-du-projet)
  - [🛠️ Exécution en local](#️-exécution-en-local)
    - [✅ Prérequis](#-prérequis)
    - [📦 Installation des dépendances](#-installation-des-dépendances)
  - [🚀 Utilisation](#-utilisation)
    - [Analyse des tickets JIRA](#analyse-des-tickets-jira)
    - [Questions pour la démo](#questions-pour-la-démo)
  - [📚 Liens utiles](#-liens-utiles)


## ℹ️ À propos

Ce projet propose une application chatbot avec RAG pour l'analyse et la résolution de tickets JIRA.

Ce projet est basé sur le jeu de données [TAWOS](https://rdr.ucl.ac.uk/articles/dataset/The_TAWOS_dataset/21308124) ...

Les tickets jira servant de base de connaissance ont été filtré pour ne récupérer que ceux pouvant servir à la résolution de problème.

[TODO]

### 🧱 Structure du projet

```bash
rag_jira
├─ src
│   ├─ entrepot                     # Package contenant tous les entrepots de données / modèles
│   │    ├─ __init__.py
│   │    ├─ embeddings.py
│   │    ├─ jira_issues.py
│   │    ├─ llm_models.py
│   │    └─ redis_schema.yaml
│   ├─ service
│   │    ├─ __init__.py
│   │    └─ indexation.py           # Service d'indexation de la base Redis
│   │
│   ├─ __init__.py
│   └─ app.py                       # Application streamlit
│
├─ tests
│   └─ ..
├─ xp
│   ├─ analyse.ipynb                # Analyse des tickets jira
│   └─ script_de_test.py
.
.
.
├─ pyproject.toml                   # Dépendances du package rag_jira
└─ README.md
```

## 🛠️ Exécution en local

1. Déployer redis localement.
```console
docker run --name redis-jira -d -p 6379:6379 redis/redis-stack:latest
```

2. Installer [Redis Insight](https://redis.io/insight/) pour visualiser le contenu de la base. Et ajouter une nouvelle base de données Redis avec les informations suivantes :
   - **host**: 127.0.0.1
   - **port**: 6379

💡 Arrêter / Rédémarrer la base :
```console
docker stop redis-jira
docker start redis-jira
```

3. Installer les dépendances de l'application (voir [📦 Installation des dépendances](#-installation-des-dépendances)).

4. Avant de lancer le chatbot, faire une indexation des tickets jira.
```console
python src/service/indexation.py
```

💡 Pour vider la base, à l'aide du CLI de Redis Insight :
```
FLUSHDB
```

5. Lancer l'application streamlit.
```console
streamlit run src/app.py
```

L'application est disponible [ici](http://localhost:8501/).

### ✅ Prérequis

- **Langage :** Python
- **Base de données :** SQL, Redis
- **Outils :** DBeaver ou autre, Redis Insight
- **Framework :** Langchain
- [**Dépendances**](./pyproject.toml)

### 📦 Installation des dépendances

- Créer un environnement virtuel.
  ```console
  cd rag_jira
  python -m venv venv
  ```

- Activer l'environnement virtuel avec `source venv/bin/activate` pour linux ou `venv\Scripts\activate` pour windows.

- Installer les dépendances du package `rag_jira`.
  ```console
  pip install -e '.[dev]'
  ```

## 🚀 Utilisation

### Analyse des tickets JIRA

Pour savoir quels tickets jira vont être indexés dans notre base Redis, nous avons fait une [analyse du jeu de données TAWOS](./xp/analyse.ipynb).

[TODO]

### Questions pour la démo
___
I'm unable to successfully connect to the server and I get the following error message.
```java
server-unknown:>admin config server --uri http://localhost:9393 --username bob --password bobspwd Unable to contact XD Admin Server at 'http://localhost:9393'.
```
___

## 📚 Liens utiles

- [TAWOS Dataset](https://rdr.ucl.ac.uk/articles/dataset/The_TAWOS_dataset/21308124)
- [Répertoire Github TAWOS](https://github.com/SOLAR-group/TAWOS)
- [A Versatile Dataset of Agile Open Source Software Projects](https://solar.cs.ucl.ac.uk/pdf/tawosi2022msr.pdf)
- [Langchain](https://python.langchain.com/v0.2/docs/introduction/)
- [Redis VectorStore](https://python.langchain.com/v0.2/docs/integrations/vectorstores/redis/)