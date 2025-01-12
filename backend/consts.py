import os

RAG_ADDR = os.getenv("rag_addr", "localhost")
RAG_PORT = os.getenv("rag_port", "50001")
MODEL_ADDR = os.getenv("model_addr", "localhost")
MODEL_PORT = os.getenv("model_port", "50001")
DATABASE_NAME = os.getenv("database_name", "database")
DATABASE_URL = os.getenv("database_url", "localhost")
DATABASE_PORT = os.getenv("database_port", "3306")
DATABASE_USER = os.getenv("database_user", "root")
DATABASE_PASSWORD = os.getenv("database_password")