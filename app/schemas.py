from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: str | None = None  # Opcional
    preco: float
    custo: float
    estoque: int
    fornecedor: str | None = None

class ProdutoCreate(ProdutoBase):
    pass  # Herda de ProdutoBase para criação

class Produto(ProdutoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permite converter de ORM para schema



class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None

    # Endereço detalhado
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

    
    pai: Optional[str] = None
    mae: Optional[str] = None
    observacoes: Optional[str] = None
    responsavel_id: Optional[int] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True