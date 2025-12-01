from sqlalchemy.orm import Session
from .models import (
    Produto, Cliente, ReceitaOftalmologica,
    Funcionario, OrdemServico, ItemOS, StatusOS
)
from .schemas import (
    ProdutoCreate, ClienteCreate, ReceitaOftalmologicaCreate, OrdemServicoCreate
)
from fastapi import HTTPException
from decimal import Decimal
from datetime import date, timedelta
from typing import Optional


# ===================== PRODUTO =====================
def create_produto(db: Session, produto: ProdutoCreate):
    db_produto = Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def get_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).offset(skip).limit(limit).all()

def get_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()


# ===================== CLIENTE =====================
def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


# ===================== RECEITA OFTALMOLÓGICA =====================
def calcular_perto(esf_long: str, adicao: Optional[str]) -> Optional[str]:
    if not adicao or not esf_long:
        return None
    try:
        esf = Decimal(esf_long.replace(",", "."))
        adi = Decimal(adicao.replace("+", "").replace(",", "."))
        resultado = esf + adi
        return f"{resultado:.2f}".replace(".", ",")
    except:
        return None


def calcular_validade(data_emissao: date, data_nascimento: Optional[date]) -> date:
    if data_nascimento:
        idade = data_emissao.year - data_nascimento.year
        if (data_emissao.month, data_emissao.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        if idade < 16:
            return data_emissao + timedelta(days=180)
    return data_emissao + timedelta(days=365)


def create_receita(db: Session, receita: ReceitaOftalmologicaCreate):
    cliente = db.query(Cliente).filter(Cliente.id == receita.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    validade = calcular_validade(receita.data_emissao, cliente.data_nascimento)
    od_perto = calcular_perto(receita.od_esf_long, receita.adicao)
    oe_perto = calcular_perto(receita.oe_esf_long, receita.adicao)

    db_receita = ReceitaOftalmologica(
        cliente_id=receita.cliente_id,
        data_emissao=receita.data_emissao,
        validade_em=validade,
        medico=receita.medico,
        crm=receita.crm,
        od_esf_long=receita.od_esf_long,
        od_cil_long=receita.od_cil_long,
        od_eixo_long=receita.od_eixo_long,
        oe_esf_long=receita.oe_esf_long,
        oe_cil_long=receita.oe_cil_long,
        oe_eixo_long=receita.oe_eixo_long,
        od_esf_perto=od_perto,
        oe_esf_perto=oe_perto,
        adicao=receita.adicao,
        dnp_od=receita.dnp_od,
        dnp_oe=receita.dnp_oe,
        altura_od=receita.altura_od,
        altura_oe=receita.altura_oe,
        observacoes=receita.observacoes
    )
    db.add(db_receita)
    db.commit()
    db.refresh(db_receita)
    return db_receita


def get_receitas_by_cliente(db: Session, cliente_id: int):
    return db.query(ReceitaOftalmologica).filter(ReceitaOftalmologica.cliente_id == cliente_id).all()


# ===================== ORDEM DE SERVIÇO =====================
def create_ordem_servico(db: Session, os_data: OrdemServicoCreate):
    # Verifica número duplicado
    if db.query(OrdemServico).filter(OrdemServico.numero_os == os_data.numero_os).first():
        raise HTTPException(status_code=400, detail="Número da OS já existe")

    # Busca cliente
    cliente = db.query(Cliente).filter(Cliente.id == os_data.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Busca funcionário (opcional)
    funcionario = None
    if os_data.funcionario_id:
        funcionario = db.query(Funcionario).filter(Funcionario.id == os_data.funcionario_id).first()

    # Cria OS
    db_os = OrdemServico(
        numero_os=os_data.numero_os,
        cliente_id=os_data.cliente_id,
        receita_id=os_data.receita_id,
        funcionario_id=os_data.funcionario_id,
        tipo_lente=os_data.tipo_lente,
        observacoes=os_data.observacoes,
        status=StatusOS.ORCAMENTO
    )
    db.add(db_os)
    db.flush()

    valor_total = Decimal("0.0")
    itens_lista = []

    for item in os_data.itens:
        produto = db.query(Produto).filter(Produto.id == item["produto_id"]).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {item['produto_id']} não encontrado")

        qty = item.get("quantidade", 1)
        preco = Decimal(str(item["preco_unitario"]))
        subtotal = preco * qty
        valor_total += subtotal

        db_item = ItemOS(
            ordem_id=db_os.id,
            produto_id=produto.id,
            quantidade=qty,
            preco_unitario=float(preco),
            subtotal=float(subtotal)
        )
        db.add(db_item)

        itens_lista.append({
            "id": db_item.id,
            "produto_id": produto.id,
            "produto_nome": produto.nome,
            "quantidade": qty,
            "preco_unitario": float(preco),
            "subtotal": float(subtotal)
        })

    db_os.valor_total = float(valor_total)
    db.commit()
    db.refresh(db_os)

    return {
        "id": db_os.id,
        "numero_os": db_os.numero_os,
        "cliente_nome": cliente.nome,
        "data_registro": db_os.data_registro,
        "funcionario_nome": funcionario.nome if funcionario else None,
        "tipo_lente": db_os.tipo_lente.value,
        "valor_total": db_os.valor_total,
        "status": db_os.status.value,
        "observacoes": db_os.observacoes,
        "receita": db_os.receita,
        "itens": itens_lista
    }