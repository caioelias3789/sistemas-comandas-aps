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