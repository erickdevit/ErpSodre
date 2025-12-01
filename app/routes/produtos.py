from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.post("/", response_model=schemas.Produto)
def create_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.create_produto(db=db, produto=produto)

@router.get("/", response_model=list[schemas.Produto])
def read_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = crud.get_produtos(db, skip=skip, limit=limit)
    return produtos

@router.get("/{produto_id}", response_model=schemas.Produto)
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.get_produto(db, produto_id=produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto