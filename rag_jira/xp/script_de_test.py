'''
Script de test pour récupérer les données de la base mariadb
'''
import os
import functools
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

row_to_content = functools.partial(
    SQLDatabaseLoader.page_content_default_mapper, column_names=["Description"]
)

row_to_metadata = functools.partial(
    SQLDatabaseLoader.metadata_default_mapper, column_names=["Title", "Type", "Status", "Resolution", "Last_Updated"]
)

loader = SQLDatabaseLoader(
    "SELECT * FROM Issue LIMIT 2",
    db,
    page_content_mapper=row_to_content,
    metadata_mapper=row_to_metadata,
)

documents = loader.load()

for doc in documents:
    print(doc.page_content)
    print(doc.metadata)
