from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def pedidos():
    """
    Rota padrão de pedidos. Todas as rotas precisam ser autenticadas
    """
    return {"mensagem" : "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema:PedidoSchema, session:Session = Depends(pegar_sessao)):
    """
    Rota para criação de pedidos. Informe o ID do USUARIO que é dono pedido
    """
    novo_pedido = Pedido(usuario = pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Rota para cancelamento de pedido. É necessário ser o DONO do pedido ou usuário ADMIN para cancelar o pedido. É necessário informar o ID do PEDIDO
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail= "Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail = "Você não tem autorização para cancelar o pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {

        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso!",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Lista todos os pedidos. Apenas usuário ADMIN pode acessar essa rota
    """
    if not usuario.admin:
        raise HTTPException(status_code= 403, detail= "Você não tem autorização")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
    
@order_router.post("/pedido/adicionar_pedido/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema,
                                session : Session = Depends(pegar_sessao),
                                usuario : Usuario = Depends(verificar_token)):
    """
    Rota para adicionar pedido. É permitido adição caso exista o pedido.Apenas o DONO do pedido ou usuário ADMIN podem acessar ess rota.
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail= "Você não tem autorização")
    item_pedido = ItemPedido(item_pedido_schema.quantidade,
                             item_pedido_schema.sabor,
                             item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario,
                             id_pedido)
    
    session.add(item_pedido)
    session.commit()
    return {
        "mensagem" : "Item criado com sucesso",
        "item_id" : item_pedido.id,
        "preco_pedido" : pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                                session : Session = Depends(pegar_sessao),
                                usuario : Usuario = Depends(verificar_token)):
    """
    Rota para remover o pedido. É necessário fornecer o id do pedido para remover. O sistema informará caso o pedido não seja encontrado ou não exista. Apenas o DONO de ADMIN podem remover.
    """
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if item_pedido is None:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    
    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item no pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail= "Você não tem autorização")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem" : "item deletado com sucesso",
        "quantidade_itens_pedido" : len(pedido.itens),
        "pedido" : pedido
    }

#finalizar pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Rota para finalizar o pedido. Caso o pedido seja concluido é esta rota que será usada. Apenas usuário autenticado pode acessar
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail= "Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail = "Você não tem autorização para finalizar o pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido número: {pedido.id} finalizado com sucesso!",
        "pedido": pedido
    }

#VISUALIZAR 1 PEDIDO
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail= "Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail = "Você não tem autorização")
    return{
        "quantidade_itens_pedido" : len(pedido.itens),
        "pedido" : pedido
    }

# Visualizar todos os pedidos de 1 usuário
@order_router.get("/listar/pedidos-usuario", response_model= list[ResponsePedidoSchema])
async def listar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Rota para visualizar todos os pedidos de 1 usuário
    """
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return  pedidos
        