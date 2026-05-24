from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produto
from app.permissoes import somente_admin

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post("")
def criar_produto(
    produto: dict,
    db: Session = Depends(get_db),
    usuario=Depends(somente_admin)
):

    novo = Produto(
        nome=produto["nome"],
        preco=produto["preco"],
        estoque=produto["estoque"],
        unidade=produto["unidade"]
    )

    db.add(novo)

    db.commit()

    db.refresh(novo)

    return {
        "mensagem": "Produto criado",
        "id": novo.id
    }


@router.get("")
def listar_produtos(
    db: Session = Depends(get_db)
):

    return db.query(
        Produto
    ).all()


@router.delete("/{id}")
def excluir_produto(
    id: int,
    db: Session = Depends(get_db),
    usuario=Depends(somente_admin)
):

    produto = db.query(
        Produto
    ).filter(
        Produto.id == id
    ).first()

    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(produto)

    db.commit()

    return {
        "mensagem": "Produto removido"
    }