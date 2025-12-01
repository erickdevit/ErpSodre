from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco SQLite (arquivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./erp_otica.db"

# Engine para conectar ao banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Função para obter uma sessão (usaremos em dependências)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()