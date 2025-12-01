from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/clientes", tags=["clientes"])  # Prefixo para URLs: /clientes/

@router.post("/", response_model=schemas.Cliente)  # POST para criar
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db=db, cliente=cliente)

@router.get("/", response_model=list[schemas.Cliente])  # GET para listar
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=schemas.Cliente)  # GET por ID
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")  # Erro se não achar
    return cliente