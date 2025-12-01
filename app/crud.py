from sqlalchemy.orm import Session
from .models import Produto
from .schemas import ProdutoCreate

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


from .models import Cliente
from .schemas import ClienteCreate

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())  # Converte schema para modelo do banco
    db.add(db_cliente)  # Adiciona ao banco
    db.commit()  # Salva mudanças
    db.refresh(db_cliente)  # Atualiza com dados gerados (ex: ID)
    return db_cliente

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()  # Lista com paginação (ex: pule 0, limite 100)

def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()  # Busca por ID