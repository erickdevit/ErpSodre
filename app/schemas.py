from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


# ===================== PRODUTO =====================
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    custo: float
    estoque: int
    fornecedor: Optional[str] = None


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ===================== CLIENTE =====================
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


# ===================== RECEITA OFTALMOLÓGICA =====================
# ← DEFINIMOS PRIMEIRO o Create
class ReceitaOftalmologicaCreate(BaseModel):
    cliente_id: int
    data_emissao: date

    medico: Optional[str] = None
    crm: Optional[str] = None

    # Longe (obrigatórios)
    od_esf_long: str
    od_cil_long: Optional[str] = None
    od_eixo_long: Optional[str] = None

    oe_esf_long: str
    oe_cil_long: Optional[str] = None
    oe_eixo_long: Optional[str] = None

    # Adição e medidas
    adicao: Optional[str] = None
    dnp_od: Optional[str] = None
    dnp_oe: Optional[str] = None
    altura_od: Optional[str] = None
    altura_oe: Optional[str] = None

    observacoes: Optional[str] = None


# podemos herdar dela
class ReceitaOftalmologica(ReceitaOftalmologicaCreate):
    id: int
    validade_em: date
    od_esf_perto: Optional[str] = None
    oe_esf_perto: Optional[str] = None
    esta_valida: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== ITEM DA OS ====================
class ItemOSResponse(BaseModel):
    id: int
    produto_id: int
    produto_nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float

    class Config:
        from_attributes = True


# ==================== ORDEM DE SERVIÇO ====================
class OrdemServicoCreate(BaseModel):
    numero_os: str                          # ← manual
    cliente_id: int
    receita_id: Optional[int] = None
    funcionario_id: Optional[int] = None
    tipo_lente: str                         # "surfaçada" ou "pronta"
    observacoes: Optional[str] = None

    itens: list[dict] = []                  # [{"produto_id": 1, "quantidade": 1, "preco_unitario": 450.00}]


class OrdemServicoResponse(BaseModel):
    id: int
    numero_os: str
    cliente_nome: str                       # ← nome do cliente
    data_registro: datetime                 # ← data e hora
    funcionario_nome: Optional[str] = None  # ← nome do funcionário
    tipo_lente: str
    valor_total: float
    status: str
    observacoes: Optional[str] = None

    # Receita completa (se tiver)
    receita: Optional[ReceitaOftalmologica] = None

    # Todos os itens com nome do produto
    itens: list[ItemOSResponse]

    class Config:
        from_attributes = True