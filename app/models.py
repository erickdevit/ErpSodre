from sqlalchemy import Column, Integer, String, Float, DateTime, func, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)  # Nome do produto, ex: "Óculos Ray-Ban"
    descricao = Column(String)         # Descrição detalhada
    preco = Column(Float)              # Preço de venda
    custo = Column(Float)              # Custo de aquisição
    estoque = Column(Integer)          # Quantidade em estoque
    fornecedor = Column(String)        # Nome do fornecedor
    created_at = Column(DateTime, default=func.now())  # Data de criação

class Cliente(Base):
    __tablename__ = "clientes"

    #=== INFORMAÇÕES PESSOAIS ===
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    telefone = Column(String)
    cpf = Column(String, unique=True, index=True)
    rg = Column(String, unique=True, index=True)
    data_nascimento = Column(Date)
    sexo = Column(String)

    # === ENDEREÇO DETALHADO ===
    cep = Column(String)          # ex: 01001-000
    logradouro = Column(String)   # Rua, Avenida, etc.
    numero = Column(String)       # Número ou "s/n"
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)       # Sigla: SP, RJ, MG...
    complemento = Column(String)  # Opcional: apto, bloco, etc.

    #=== INFORMAÇÕES ADICIONAIS ===
    pai = Column(String)
    mae = Column(String)
    observacoes = Column(String)
    responsavel_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)

    #=== RESPONSAVEIS LEGAIS ===
    responsavel = relationship("Cliente", remote_side=[id], backref="dependentes")
    created_at = Column(DateTime, default=func.now())