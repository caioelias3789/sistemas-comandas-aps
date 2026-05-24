from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ItemComanda, Produto, Comanda
from app.permissoes import admin_ou_garcom

router = APIRouter(
    prefix="/itens",
    tags=["Itens"]
)

@router.post("")
def adicionar_item(
    dados:dict,
    db:Session=Depends(get_db),
    usuario=Depends(admin_ou_garcom)
):

    produto=db.query(
        Produto
    ).filter(
        Produto.id==dados["produto_id"]
    ).first()

    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    comanda=db.query(
        Comanda
    ).filter(
        Comanda.id==dados["comanda_id"]
    ).first()

    if not comanda:

        raise HTTPException(
            status_code=404,
            detail="Comanda não encontrada"
        )

    item=ItemComanda(
        produto_id=dados["produto_id"],
        comanda_id=dados["comanda_id"],
        quantidade=dados["quantidade"]
    )

    comanda.total += (
        produto.preco *
        dados["quantidade"]
    )

    db.add(item)

    db.commit()

    return{
        "mensagem":"Item adicionado"
    }


@router.get("")
def listar_itens(
    db:Session=Depends(get_db)
):

    return db.query(
        ItemComanda
    ).all()