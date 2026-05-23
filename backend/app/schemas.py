from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    nome:str
    preco:float
    estoque:int
    unidade:str

class Login(BaseModel):
    email:str
    senha:str