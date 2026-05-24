from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comanda

router = APIRouter(
    prefix="/comandas",
    tags=["Comandas"]
)

@router.get("")
def listar_comandas(
    db: Session = Depends(get_db)
):
    return db.query(
        Comanda
    ).all()


@router.post("")
def criar_comanda(
    dados: dict,
    db: Session = Depends(get_db)
):

    nova = Comanda(
        mesa=dados["mesa"],
        status="ABERTA",
        total=0
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova