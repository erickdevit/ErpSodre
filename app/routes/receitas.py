from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/receitas", tags=["receitas"])

@router.post("/", response_model=schemas.ReceitaOftalmologica)
def create_receita(receita: schemas.ReceitaOftalmologicaCreate, db: Session = Depends(get_db)):
    return crud.create_receita(db=db, receita=receita)

@router.get("/cliente/{cliente_id}", response_model=list[schemas.ReceitaOftalmologica])
def read_receitas_by_cliente(cliente_id: int, db: Session = Depends(get_db)):
    receitas = crud.get_receitas_by_cliente(db, cliente_id=cliente_id)
    return receitas