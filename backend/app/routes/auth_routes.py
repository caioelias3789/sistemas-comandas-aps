from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.auth import verificar
from app.schemas import Login

router = APIRouter(
    tags=["Autenticação"]
)

@router.post("/login")
def login(
    dados: Login,
    db: Session = Depends(get_db)
):

    usuario = db.query(
        Usuario
    ).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário inválido"
        )

    senha_valida = verificar(
        dados.senha,
        usuario.senha
    )

    if not senha_valida:

        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    return {
        "nome": usuario.nome,
        "tipo": usuario.tipo
    }