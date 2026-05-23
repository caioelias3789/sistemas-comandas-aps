from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Comanda

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/comandas")
def listar_comandas(
    db: Session = Depends(get_db)
):

    return db.query(
        Comanda
    ).all()


@router.post("/comandas")
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

    db.refresh(
        nova
    )

    return nova


@router.put("/comandas/{id}")
def atualizar_comanda(
    id: int,
    dados: dict,
    db: Session = Depends(get_db)
):

    comanda = db.query(
        Comanda
    ).filter(
        Comanda.id == id
    ).first()

    if not comanda:

        return {
            "erro":
            "Comanda não encontrada"
        }

    comanda.status = dados["status"]

    db.commit()

    db.refresh(
        comanda
    )

    return comanda


@router.put("/comandas/{id}/fechar")
def fechar_comanda(
    id:int,
    db: Session = Depends(get_db)
):

    comanda = db.query(
        Comanda
    ).filter(
        Comanda.id == id
    ).first()

    if not comanda:

        return {
            "erro":
            "Comanda não encontrada"
        }

    comanda.status = "FINALIZADA"

    db.commit()

    return {

        "mensagem":
        "Comanda fechada"
    }


# ROTA FALTANDO
@router.post("/comandas/{id}/itens")
def adicionar_item(
    id:int,
    dados:dict,
    db:Session=Depends(get_db)
):

    comanda=db.query(
        Comanda
    ).filter(
        Comanda.id==id
    ).first()

    if not comanda:

        return {
            "erro":"Comanda não encontrada"
        }

    # temporário
    quantidade=dados["quantidade"]

    comanda.total += quantidade*10

    db.commit()

    db.refresh(
        comanda
    )

    return {

        "mensagem":"Item adicionado",
        "novo_total":comanda.total
    }

@router.delete("/comandas/{id}")
def excluir_comanda(
    id:int,
    db: Session = Depends(get_db)
):

    comanda = db.query(
        Comanda
    ).filter(
        Comanda.id == id
    ).first()

    if not comanda:

        return {
            "erro":"Comanda não encontrada"
        }

    db.delete(
        comanda
    )

    db.commit()

    return {
        "mensagem":"Comanda excluída"
    }