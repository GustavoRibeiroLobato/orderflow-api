from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

# processo de migração: alembic revision --autogenerate -m "alteração que foi feita"
# para implementar a migração: alembic upgrade head

#cria a conexão no banco de dados
db = create_engine("sqlite:///banco.db")

#cria a base do banco de dados
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

    #STATUS_PEDIDOS = (
     #   ("PENDENTE", "PENDENTE"),
      #  ("CANCELADO", "CANCELADO"),
       # ("FINALIZADO", "FINALIZADO")
        #)
    
    id = Column("id", Integer, primary_key= True, autoincrement= True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    itens = relationship("ItemPedido", cascade= "all, delete")
    @hybrid_property
    def preco(self):
        """Calcula o preço total somando os itens em memória"""
        if self.itens:
            return sum(item.preco_unitario * item.quantidade for item in self.itens)
        return 0.0

    #itens
    def __init__(self, usuario, status = "PENDENTE", preco = 0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

#itens pedidos
class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key= True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
        