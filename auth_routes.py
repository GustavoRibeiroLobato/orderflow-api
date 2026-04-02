from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from config import settings, bcrypt_context
from schemas import UsuarioSchema, LoginSchema, RefreshTokenSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=None):
    if duracao_token is None:
        duracao_token = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, settings.SECRET_KEY, settings.ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def home():
    """
    Rota da padrão de autenticação
    """
    return {"mensagem": "você acessou a rota padrão de autenticação", "autenticação": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    Rota para criar conta. Apenas para novos usuários. É necessário informar o nome, email, senha. Caso não seja usuário ADMIN informar como FALSE
    """
    
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return{"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}
    

@auth_router.post("/login")
async def login(login_schemas: LoginSchema, session:Session = Depends(pegar_sessao)): 
    """
    Rota para Login. É necessário informar email usado no cadastrado e senha.
    """
    usuario = autenticar_usuario(login_schemas.email, login_schemas.senha, session )
    if not usuario:
        raise HTTPException(status_code=404, detail="usuário não encontrato")
    
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) 
        return {
            "access_token":access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session:Session = Depends(pegar_sessao)): 
    """
    Rota para autenticação de usuário
    """
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session )
    if not usuario:
        raise HTTPException(status_code=404, detail="usuário não encontrato")
    
    else:
        access_token = criar_token(usuario.id) 
        return {
            "access_token":access_token,
            "token_type": "Bearer"
        }
    
@auth_router.post("/refresh")
async def use_refresh_token(dados: RefreshTokenSchema, session: Session = Depends(pegar_sessao)):
    """
    Gera um novo access_token usando um refresh_token válido.
    """
    try:
        # Decodifica o token manualmente para validar se é legítimo
        payload = jwt.decode(dados.refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        usuario = session.query(Usuario).filter(Usuario.id == int(user_id)).first()
        if not usuario or not usuario.ativo:
            raise HTTPException(status_code=401, detail="Usuário inválido ou inativo")
            
        novo_access_token = criar_token(usuario.id)
        
        return {
            "access_token": novo_access_token,
            "token_type": "Bearer"
        }
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expirado ou inválido")