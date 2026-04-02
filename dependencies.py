from fastapi import Depends, HTTPException
from main import oauth2_schema 
from config import settings
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
def pegar_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verificar_token(token : str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Acesso Negado! Verifique a validade do Token")
    #verifica se o token é válido
    #extrair o ID do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail= "Acesso inválido")
    return usuario