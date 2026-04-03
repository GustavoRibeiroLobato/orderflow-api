# 🚀 OrderFlow API

### API REST desenvolvida com FastAPI para gerenciamento de pedidos, usuários e autenticação, simulando o funcionamento de um sistema real de pedidos (ex: pizzaria, delivery ou restaurante).

### Este projeto foi desenvolvido com foco em boas práticas de desenvolvimento backend, organização em camadas e uso de tecnologias modernas.

# 📌 Sobre o projeto

### O OrderFlow API é uma aplicação backend que permite:

- Cadastro e autenticação de usuários
- Criação e gerenciamento de pedidos
- Associação de itens aos pedidos
- Controle de status dos pedidos
- Proteção de rotas com autenticação JWT

    


# 🚀 Funcionalidades Principais
- **Sistema de Autenticação JWT**: Implementação completa de segurança com OAuth2 e JOSE.

- **Access Token**: Tokens de curta duração para operações seguras.

- **Refresh Token**: Sistema de renovação de acesso independente, permitindo que o usuário permaneça logado com segurança sem reexpor as credenciais.

- **Gestão de Pedidos e Itens**.

- **Criação, listagem, cancelamento e finalização de pedidos**.

- **Adição e remoção dinâmica de itens com cálculo automático de valores**.

- **Cálculos Inteligentes (Hybrid Properties)**: Uso de propriedades híbridas no SQLAlchemy para garantir que o preço total do pedido seja sempre calculado em tempo real, evitando inconsistências no banco de dados.

- **Controle de Acesso (RBAC)**: Diferenciação entre usuários comuns e Administradores para rotas sensíveis.

- **Migrações de Banco de Dados**: Histórico de versões do banco controlado pelo Alembic, configurado com render_as_batch para suporte total ao SQLite.


# 📁 Estrutura do Projeto
    .
    ├── main.py              # Ponto de entrada e definição das rotas principais
    ├── auth_routes.py       # Endpoints de autenticação, login e tokens
    ├── order_routes.py      # Lógica de negócio para pedidos e itens
    ├── models.py            # Definição das tabelas do banco e relacionamentos
    ├── schemas.py           # Modelos Pydantic para validação (DTPs)
    ├── config.py            # Variáveis de ambiente e configurações globais
    └── dependencies.py      # Injeção de dependência (DB session e JWT)


# ⚙️ Tecnologias utilizadas
- ⚡ FastAPI
- 🐍 Python
- 🗄️ SQLAlchemy
- 🔐 JWT (JSON Web Token)
- 🔑 OAuth2PasswordBearer
- 🔒 Passlib (bcrypt)
- 📦 Uvicorn
- 🔐 Autenticação

# 🔐 Segurança
### A API utiliza autenticação baseada em JWT (Bearer Token). O fluxo de uso é:
- Usuário faz login
- Recebe um token JWT
- Usa o token para acessar rotas protegidas


# ▶️ Como executar o projeto
1. Clonar o repositório:
    
    - `git clone https://github.com/seu-usuario/orderflow-api.git`
    - `cd orderflow-api`


2. Criar ambiente virtual:
    `python -m venv venv`

3. Ativar o ambiente virtual:
    - Ativação Windows: `venv\Scripts\activate`
    - Linux/Mac: `source venv/bin/activate`


3. Instalar dependências: `pip install -r requirements.txt`

4. Executar a aplicação: `uvicorn main:app --reload`

5. Acessar documentação
    - [Swagger](http://127.0.0.1:8000/docs)
    - [Redoc](http://127.0.0.1:8000/redoc)


# 👨‍💻 Autor

### Desenvolvido por Gustavo Ribeiro Lobato
- [Acesse o meu GitHub](https://github.com/GustavoRibeiroLobato).
- [Me adicione no LinkedIn](www.linkedin.com/in/gustavo-ribeiro-lobato).

# 📄 Licença
### Este projeto está sob a licença MIT.