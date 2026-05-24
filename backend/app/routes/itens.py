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
    dados: dict,
    db: Session = Depends(get_db),
    usuario=Depends(admin_ou_garcom)
):

    # procura produto
    produto = db.query(
        Produto
    ).filter(
        Produto.id == dados["produto_id"]
    ).first()

    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    # procura comanda
    comanda = db.query(
        Comanda
    ).filter(
        Comanda.id == dados["comanda_id"]
    ).first()

    if not comanda:

        raise HTTPException(
            status_code=404,
            detail="Comanda não encontrada"
        )


    # impede adicionar em comanda fechada
    if comanda.status == "FINALIZADA":

        raise HTTPException(
            status_code=400,
            detail="Comanda já fechada"
        )


    quantidade = dados["quantidade"]


    # verifica estoque
    if produto.estoque < quantidade:

        raise HTTPException(
            status_code=400,
            detail="Estoque insuficiente"
        )


    # baixa estoque
    produto.estoque -= quantidade


    # cria item
    item = ItemComanda(
        produto_id=dados["produto_id"],
        comanda_id=dados["comanda_id"],
        quantidade=quantidade
    )


    # atualiza total
    comanda.total += (
        produto.preco * quantidade
    )


    db.add(item)

    db.commit()

    db.refresh(item)

    return {

        "mensagem": "Item adicionado",

        "estoque_restante":
        produto.estoque
    }


@router.get("")
def listar_itens(
    db: Session = Depends(get_db)
):

    return db.query(
        ItemComanda
    ).all()