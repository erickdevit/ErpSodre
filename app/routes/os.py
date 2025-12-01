from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/os", tags=["Ordens de Serviço"])

@router.post("/", response_model=schemas.OrdemServicoResponse)
def criar_os(os: schemas.OrdemServicoCreate, db: Session = Depends(get_db)):
    return crud.create_ordem_servico(db=db, os_data=os)

@router.get("/{numero_os}", response_model=schemas.OrdemServicoResponse)
def buscar_os(numero_os: str, db: Session = Depends(get_db)):
    os = db.query(models.OrdemServico).filter(models.OrdemServico.numero_os == numero_os).first()
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")
    # Aqui você pode montar a resposta completa igual no create
    return os