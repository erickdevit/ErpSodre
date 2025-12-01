from sqlalchemy import Column, Integer, String, Float, DateTime, func, Date, ForeignKey, Boolean
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




from datetime import date, timedelta

class ReceitaOftalmologica(Base):
    __tablename__ = "receitas_oftalmologicas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False, index=True)

    data_emissao = Column(Date, nullable=False)
    validade_em = Column(Date, nullable=False)   # ← NOVO: data de validade
    medico = Column(String)
    crm = Column(String)

    # Longe
    od_esf_long = Column(String, nullable=False)
    od_cil_long = Column(String)
    od_eixo_long = Column(String)
    oe_esf_long = Column(String, nullable=False)
    oe_cil_long = Column(String)
    oe_eixo_long = Column(String)

    # Perto (calculado)
    od_esf_perto = Column(String)
    oe_esf_perto = Column(String)

    adicao = Column(String)
    dnp_od = Column(String)
    dnp_oe = Column(String)
    altura_od = Column(String)
    altura_oe = Column(String)

    observacoes = Column(String)
    created_at = Column(DateTime, default=func.now())

    cliente = relationship("Cliente", backref="receitas")

    # ← Campo calculado: True se ainda válida
    @property
    def esta_valida(self) -> bool:
        return date.today() <= self.validade_em
    

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# Enums
class TipoLente(str, enum.Enum):
    SURFACADA = "surfaçada"
    PRONTA = "pronta"

class StatusOS(str, enum.Enum):
    ORCAMENTO = "Orçamento"
    PRODUCAO = "Em produção"
    PRONTO = "Pronto"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"

# Tabela Funcionários (se ainda não tiver)
class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cargo = Column(String)
    telefone = Column(String)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Ordem de Serviço
class OrdemServico(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)
    numero_os = Column(String, unique=True, nullable=False, index=True)  # manual
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False)
    receita_id = Column(Integer, ForeignKey("receitas_oftalmologicas.id", ondelete="SET NULL"), nullable=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id", ondelete="SET NULL"), nullable=True)

    data_registro = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo_lente = Column(Enum(TipoLente), nullable=False)
    valor_total = Column(Numeric(10, 2), default=0.0)
    status = Column(Enum(StatusOS), default=StatusOS.ORCAMENTO)
    observacoes = Column(Text)

    # Relacionamentos
    cliente = relationship("Cliente", backref="ordens")
    receita = relationship("ReceitaOftalmologica")
    funcionario = relationship("Funcionario")
    itens = relationship("ItemOS", back_populates="ordem", cascade="all, delete-orphan")

# Itens da OS
class ItemOS(Base):
    __tablename__ = "itens_os"

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("ordens_servico.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    quantidade = Column(Integer, default=1, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    ordem = relationship("OrdemServico", back_populates="itens")
    produto = relationship("Produto")