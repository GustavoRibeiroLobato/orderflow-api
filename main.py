from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from config import settings
import os

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl= "auth/login-form")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
#para executar o código no terminarl: uvicorn main:app --reload

# RestAPI
# get -> leitura/pegar
# post -> enviar/Criar
# put/path -> edição
# delete -> autoexplicativo 