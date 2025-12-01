from fastapi import FastAPI
from .database import Base, engine
from .routes import produtos

# Cria as tabelas no banco (rode uma vez)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Óticas")

app.include_router(produtos.router)

from .routes import clientes  # Importe o router de clientes

app.include_router(clientes.router)  # Adicione ao app