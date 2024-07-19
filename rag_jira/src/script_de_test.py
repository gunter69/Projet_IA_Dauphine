'''
Script de test pour récupérer les données de la base mariadb
'''
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from langchain_community.document_loaders.sql_database import SQLDatabaseLoader
from langchain_community.utilities import SQLDatabase

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

engine = create_engine(
    f"mariadb+mysqldb://{user}:{password}@{host}:{port}/{database}"
)
db = SQLDatabase(engine)

loader = SQLDatabaseLoader(
    "SELECT Title, Description FROM Issue LIMIT 2",
    db
)

documents = loader.load()

for doc in documents:
    print(doc)
