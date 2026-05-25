from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comanda, ItemComanda
from app.permissoes import (
    admin_ou_garcom,
    admin_ou_caixa,
    somente_admin
)

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
    db: Session = Depends(get_db),
    usuario=Depends(admin_ou_garcom)
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


@router.put("/{comanda_id}/fechar")
def fechar_comanda(
    comanda_id:int,
    db:Session=Depends(get_db),
    usuario=Depends(admin_ou_caixa)
):

    comanda=db.query(
        Comanda
    ).filter(
        Comanda.id==comanda_id
    ).first()

    if not comanda:

        raise HTTPException(
            status_code=404,
            detail="Comanda não encontrada"
        )

    comanda.status="FINALIZADA"

    db.commit()

    return{
        "mensagem":"Comanda fechada"
    }


@router.delete("/{comanda_id}")
def excluir_comanda(
    comanda_id:int,
    db:Session=Depends(get_db),
    usuario=Depends(somente_admin)
):

    comanda=db.query(
        Comanda
    ).filter(
        Comanda.id==comanda_id
    ).first()

    if not comanda:

        raise HTTPException(
            status_code=404,
            detail="Comanda não encontrada"
        )

    if comanda.status!="FINALIZADA":

        raise HTTPException(
            status_code=400,
            detail="Só é possível apagar comandas finalizadas"
        )

    itens=db.query(
        ItemComanda
    ).filter(
        ItemComanda.comanda_id==comanda_id
    ).all()

    for item in itens:

        db.delete(item)

    db.delete(comanda)

    db.commit()

    return{
        "mensagem":"Comanda removida"
    }