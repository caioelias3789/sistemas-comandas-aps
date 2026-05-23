from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models import Usuario
from app.auth import gerar_hash

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

# ==========================
# SCHEMA
# ==========================

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: str


# ==========================
# Criar usuário
# ==========================

@router.post("")
def criar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):

    existe = db.query(
        Usuario
    ).filter(
        Usuario.email == dados.email
    ).first()

    if existe:

        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=gerar_hash(
            dados.senha
        ),
        tipo=dados.tipo
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "id": novo.id,
        "nome": novo.nome,
        "email": novo.email,
        "tipo": novo.tipo
    }


# ==========================
# Listar usuários
# ==========================

@router.get("")
def listar_usuarios(
    db: Session = Depends(get_db)
):

    usuarios = db.query(
        Usuario
    ).all()

    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "tipo": u.tipo
        }
        for u in usuarios
    ]


# ==========================
# Buscar usuário
# ==========================

@router.get("/{id}")
def buscar_usuario(
    id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(
        Usuario
    ).filter(
        Usuario.id == id
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    }


# ==========================
# Excluir usuário
# ==========================

@router.delete("/{id}")
def excluir_usuario(
    id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(
        Usuario
    ).filter(
        Usuario.id == id
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "mensagem": "Usuário removido"
    }