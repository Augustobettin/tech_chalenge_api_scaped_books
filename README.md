# API de Receitas e Livros (Tech Challenge)

## Sumário
- [Descrição do Projeto e Arquitetura](#descrição-do-projeto-e-arquitetura)
- [Instruções de Instalação e Configuração](#instruções-de-instalação-e-configuração)
- [Documentação das Rotas da API](#documentação-das-rotas-da-api)
- [Exemplos de Chamadas com Requests/Responses](#exemplos-de-chamadas-com-requestsresponses)
- [Instruções para Execução](#instruções-para-execução)

## Descrição do Projeto e Arquitetura

### Descrição
Esta é uma API RESTful desenvolvida em Python com o framework Flask. A aplicação permite o gerenciamento completo de receitas e livros, incluindo um sistema de autenticação de usuários via JWT (JSON Web Tokens). Uma das funcionalidades centrais é a capacidade de popular o banco de dados de livros através de um processo de web scraping, que pode ser acionado por um endpoint específico.

As principais funcionalidades incluem:
-   Autenticação de usuários (registro e login).
-   CRUD (Criar, Ler, Atualizar, Deletar) completo para receitas.
-   Ingestão de dados de livros via web scraping.
-   Busca avançada de livros por título e/ou categoria.
-   Endpoint de Health Check para monitoramento da saúde da aplicação e do banco de dados.

### Arquitetura
O projeto foi estruturado utilizando o padrão **Application Factory** para promover modularidade, testabilidade e escalabilidade. As rotas foram separadas em **Blueprints** para uma melhor organização do código (Separação de Preocupações).

-   **Linguagem:** Python 3.11+
-   **Framework Principal:** Flask
-   **Banco de Dados:** Flask-SQLAlchemy (com SQLite para desenvolvimento)
-   **Migrações de DB:** Flask-Migrate
-   **Autenticação:** Flask-JWT-Extended
-   **Documentação da API:** Flasgger (Swagger UI)
-   **Web Scraping:** Requests e BeautifulSoup4
-   **Manipulação de Dados:** Pandas
-   **Servidor WSGI (Produção):** Gunicorn

#### Estrutura de Diretórios
```
/seu_projeto/
├── app/
│   ├── __init__.py      # Fábrica da aplicação (create_app)
│   ├── models.py        # Definição das tabelas (User, Recipe, Book)
│   ├── routes.py        # Rotas principais (User, Recipe, Search)
│   └── routes_scrape.py # Rota de scraping
│
├── migrations/          # Arquivos de migração do Flask-Migrate
├── config.py            # Configurações da aplicação
├── run.py               # Ponto de entrada para executar a aplicação
├── requirements.txt     # Dependências do projeto
└── vercel.json          # Configuração de deploy para a Vercel
```

## Instruções de Instalação e Configuração

### Pré-requisitos
-   Python 3.10 ou superior
-   `pip` (gerenciador de pacotes do Python)
-   `git`

### Passos para Instalação

1.  **Clone o repositório:**
    ```sh
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_SEU_PROJETO>
    ```

2.  **Crie e ative um ambiente virtual:**
    -   **Windows:**
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   **macOS / Linux:**
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis. Este arquivo não deve ser enviado para o repositório git.
    ```env
    # .env
    SECRET_KEY='uma-chave-secreta-bem-forte-para-flask'
    JWT_SECRET_KEY='outra-chave-secreta-forte-para-jwt'
    # DATABASE_URL='sqlite:///app.db' # (Opcional, já é o padrão no config.py)
    ```

5.  **Aplique as Migrações do Banco de Dados:**
    Este comando criará o arquivo de banco de dados (`app.db` ou `recipes.db`) e todas as tabelas necessárias.
    ```sh
    # Certifique-se de definir a variável FLASK_APP
    # Windows: set FLASK_APP=run.py
    # Linux/macOS: export FLASK_APP=run.py

    flask db upgrade
    ```

## Documentação das Rotas da API
A documentação completa e interativa da API é gerada automaticamente pelo Flasgger e pode ser acessada após iniciar o servidor.

**URL da Documentação:** [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

### Resumo dos Endpoints

| Método HTTP | Endpoint                                    | Descrição                                         | Autenticação Necessária |
| :---------- | :------------------------------------------ | :------------------------------------------------ | :---------------------- |
| `POST`      | `/register`                                 | Registra um novo usuário.                         | Não                     |
| `POST`      | `/login`                                    | Autentica um usuário e retorna um token JWT.      | Não                     |
| `GET`       | `/api/v1/health`                            | Verifica a saúde da API e do banco de dados.      | Não                     |
| `POST`      | `/recipes`                                  | Cria uma nova receita.                            | Sim (JWT)               |
| `GET`       | `/recipes`                                  | Lista todas as receitas.                          | Sim (JWT)               |
| `PUT`       | `/recipes/<int:recipe_id>`                  | Atualiza uma receita existente.                   | Sim (JWT)               |
| `DELETE`    | `/recipes/<int:recipe_id>`                  | Deleta uma receita.                               | Sim (JWT)               |
| `POST`      | `/scrape-books`                             | Aciona o scraping e salva novos livros no DB.     | Sim (JWT)               |
| `GET`       | `/api/v1/books/search`                      | Busca livros por título e/ou categoria.           | Sim (JWT)               |


## Exemplos de Chamadas com Requests/Responses

### 1. Registrar um Novo Usuário
**Request (`curl`):**
```sh
curl -X POST [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register) \
-H "Content-Type: application/json" \
-d '{"username": "augusto", "password": "senha123"}'
```
**Response (201 Created):**
```json
{
  "msg": "Usuário criado com sucesso"
}
```

### 2. Realizar Login
**Request (`curl`):**
```sh
curl -X POST [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) \
-H "Content-Type: application/json" \
-d '{"username": "augusto", "password": "senha123"}'
```
**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
**Guarde o `access_token` para as próximas requisições.**

### 3. Buscar Livros por Categoria (Rota Protegida)
**Request (`curl`):**
```sh
# Substitua <SEU_TOKEN> pelo token obtido no login
curl -X GET "[http://127.0.0.1:5000/api/v1/books/search?category=Poetry](http://127.0.0.1:5000/api/v1/books/search?category=Poetry)" \
-H "Authorization: Bearer <SEU_TOKEN>"
```
**Response (200 OK):**
```json
[
  {
    "availability": "In stock",
    "category": "Poetry",
    "id": 1,
    "price_incl_tax": 51.77,
    "stars": 3,
    "title": "A Light in the Attic"
  }
]
```

## Instruções para Execução

### Executando em Ambiente de Desenvolvimento
1.  Certifique-se de que seu ambiente virtual (`venv`) está ativado.
2.  Verifique se o arquivo `.env` está configurado.
3.  Execute o seguinte comando no terminal:
    ```sh
    python run.py
    ```
4.  A API estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Gerenciando o Banco de Dados
Ao modificar os modelos em `app/models.py` (adicionar/remover tabelas ou colunas), você precisa gerar uma nova migração.
```sh
# 1. Defina a variável de ambiente do Flask
# Windows: set FLASK_APP=run.py
# Linux/macOS: export FLASK_APP=run.py
# API de Receitas e Livros (Tech Challenge)

## Sumário
- [Descrição do Projeto e Arquitetura](#descrição-do-projeto-e-arquitetura)
- [Instruções de Instalação e Configuração](#instruções-de-instalação-e-configuração)
- [Documentação das Rotas da API](#documentação-das-rotas-da-api)
- [Exemplos de Chamadas com Requests/Responses](#exemplos-de-chamadas-com-requestsresponses)
- [Instruções para Execução](#instruções-para-execução)

## Descrição do Projeto e Arquitetura

### Descrição
Esta é uma API RESTful desenvolvida em Python com o framework Flask. A aplicação permite o gerenciamento completo de receitas e livros, incluindo um sistema de autenticação de usuários via JWT (JSON Web Tokens). Uma das funcionalidades centrais é a capacidade de popular o banco de dados de livros através de um processo de web scraping, que pode ser acionado por um endpoint específico.

As principais funcionalidades incluem:
-   Autenticação de usuários (registro e login).
-   CRUD (Criar, Ler, Atualizar, Deletar) completo para receitas.
-   Ingestão de dados de livros via web scraping.
-   Busca avançada de livros por título e/ou categoria.
-   Endpoint de Health Check para monitoramento da saúde da aplicação e do banco de dados.

### Arquitetura
O projeto foi estruturado utilizando o padrão **Application Factory** para promover modularidade, testabilidade e escalabilidade. As rotas foram separadas em **Blueprints** para uma melhor organização do código (Separação de Preocupações).

-   **Linguagem:** Python 3.11+
-   **Framework Principal:** Flask
-   **Banco de Dados:** Flask-SQLAlchemy (com SQLite para desenvolvimento)
-   **Migrações de DB:** Flask-Migrate
-   **Autenticação:** Flask-JWT-Extended
-   **Documentação da API:** Flasgger (Swagger UI)
-   **Web Scraping:** Requests e BeautifulSoup4
-   **Manipulação de Dados:** Pandas
-   **Servidor WSGI (Produção):** Gunicorn

#### Estrutura de Diretórios
```
/seu_projeto/
├── app/
│   ├── __init__.py      # Fábrica da aplicação (create_app)
│   ├── models.py        # Definição das tabelas (User, Recipe, Book)
│   ├── routes.py        # Rotas principais (User, Recipe, Search)
│   └── routes_scrape.py # Rota de scraping
│
├── migrations/          # Arquivos de migração do Flask-Migrate
├── config.py            # Configurações da aplicação
├── run.py               # Ponto de entrada para executar a aplicação
├── requirements.txt     # Dependências do projeto
└── vercel.json          # Configuração de deploy para a Vercel
```

## Instruções de Instalação e Configuração

### Pré-requisitos
-   Python 3.10 ou superior
-   `pip` (gerenciador de pacotes do Python)
-   `git`

### Passos para Instalação

1.  **Clone o repositório:**
    ```sh
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_SEU_PROJETO>
    ```

2.  **Crie e ative um ambiente virtual:**
    -   **Windows:**
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   **macOS / Linux:**
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis. Este arquivo não deve ser enviado para o repositório git.
    ```env
    # .env
    SECRET_KEY='uma-chave-secreta-bem-forte-para-flask'
    JWT_SECRET_KEY='outra-chave-secreta-forte-para-jwt'
    # DATABASE_URL='sqlite:///app.db' # (Opcional, já é o padrão no config.py)
    ```

5.  **Aplique as Migrações do Banco de Dados:**
    Este comando criará o arquivo de banco de dados (`app.db` ou `recipes.db`) e todas as tabelas necessárias.
    ```sh
    # Certifique-se de definir a variável FLASK_APP
    # Windows: set FLASK_APP=run.py
    # Linux/macOS: export FLASK_APP=run.py

    flask db upgrade
    ```

## Documentação das Rotas da API
A documentação completa e interativa da API é gerada automaticamente pelo Flasgger e pode ser acessada após iniciar o servidor.

**URL da Documentação:** [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

### Resumo dos Endpoints

| Método HTTP | Endpoint                                    | Descrição                                         | Autenticação Necessária |
| :---------- | :------------------------------------------ | :------------------------------------------------ | :---------------------- |
| `POST`      | `/register`                                 | Registra um novo usuário.                         | Não                     |
| `POST`      | `/login`                                    | Autentica um usuário e retorna um token JWT.      | Não                     |
| `GET`       | `/api/v1/health`                            | Verifica a saúde da API e do banco de dados.      | Não                     |
| `POST`      | `/recipes`                                  | Cria uma nova receita.                            | Sim (JWT)               |
| `GET`       | `/recipes`                                  | Lista todas as receitas.                          | Sim (JWT)               |
| `PUT`       | `/recipes/<int:recipe_id>`                  | Atualiza uma receita existente.                   | Sim (JWT)               |
| `DELETE`    | `/recipes/<int:recipe_id>`                  | Deleta uma receita.                               | Sim (JWT)               |
| `POST`      | `/scrape-books`                             | Aciona o scraping e salva novos livros no DB.     | Sim (JWT)               |
| `GET`       | `/api/v1/books/search`                      | Busca livros por título e/ou categoria.           | Sim (JWT)               |


## Exemplos de Chamadas com Requests/Responses

### 1. Registrar um Novo Usuário
**Request (`curl`):**
```sh
curl -X POST [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register) \
-H "Content-Type: application/json" \
-d '{"username": "augusto", "password": "senha123"}'
```
**Response (201 Created):**
```json
{
  "msg": "Usuário criado com sucesso"
}
```

### 2. Realizar Login
**Request (`curl`):**
```sh
curl -X POST [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) \
-H "Content-Type: application/json" \
-d '{"username": "augusto", "password": "senha123"}'
```
**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
**Guarde o `access_token` para as próximas requisições.**

### 3. Buscar Livros por Categoria (Rota Protegida)
**Request (`curl`):**
```sh
# Substitua <SEU_TOKEN> pelo token obtido no login
curl -X GET "[http://127.0.0.1:5000/api/v1/books/search?category=Poetry](http://127.0.0.1:5000/api/v1/books/search?category=Poetry)" \
-H "Authorization: Bearer <SEU_TOKEN>"
```
**Response (200 OK):**
```json
[
  {
    "availability": "In stock",
    "category": "Poetry",
    "id": 1,
    "price_incl_tax": 51.77,
    "stars": 3,
    "title": "A Light in the Attic"
  }
]
```

## Instruções para Execução

### Executando em Ambiente de Desenvolvimento
1.  Certifique-se de que seu ambiente virtual (`venv`) está ativado.
2.  Verifique se o arquivo `.env` está configurado.
3.  Execute o seguinte comando no terminal:
    ```sh
    python run.py
    ```
4.  A API estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Gerenciando o Banco de Dados
Ao modificar os modelos em `app/models.py` (adicionar/remover tabelas ou colunas), você precisa gerar uma nova migração.
```sh
# 1. Defina a variável de ambiente do Flask
# Windows: set FLASK_APP=run.py
# Linux/macOS: export FLASK_APP=run.py

# 2. Gere o arquivo de migração automático
flask db migrate -m "Uma breve descrição da sua mudança"

# 3. Aplique a mudança ao banco de dados
flask db upgrade
```# API de Receitas e Livros (Tech Challenge)

## Sumário
- [Descrição do Projeto e Arquitetura](#descrição-do-projeto-e-arquitetura)
- [Instruções de Instalação e Configuração](#instruções-de-instalação-e-configuração)
- [Documentação das Rotas da API](#documentação-das-rotas-da-api)
- [Exemplos de Chamadas com Requests/Responses](#exemplos-de-chamadas-com-requestsresponses)
- [Instruções para Execução](#instruções-para-execução)

## Descrição do Projeto e Arquitetura

### Descrição
Esta é uma API RESTful desenvolvida em Python com o framework Flask. A aplicação permite o gerenciamento completo de receitas e livros, incluindo um sistema de autenticação de usuários via JWT (JSON Web Tokens). Uma das funcionalidades centrais é a capacidade de popular o banco de dados de livros através de um processo de web scraping, que pode ser acionado por um endpoint específico.

As principais funcionalidades incluem:
-   Autenticação de usuários (registro e login).
-   CRUD (Criar, Ler, Atualizar, Deletar) completo para receitas.
-   Ingestão de dados de livros via web scraping.
-   Busca avançada de livros por título e/ou categoria.
-   Endpoint de Health Check para monitoramento da saúde da aplicação e do banco de dados.

### Arquitetura
O projeto foi estruturado utilizando o padrão **Application Factory** para promover modularidade, testabilidade e escalabilidade. As rotas foram separadas em **Blueprints** para uma melhor organização do código (Separação de Preocupações).

-   **Linguagem:** Python 3.11+
-   **Framework Principal:** Flask
-   **Banco de Dados:** Flask-SQLAlchemy (com SQLite para desenvolvimento)
-   **Migrações de DB:** Flask-Migrate
-   **Autenticação:** Flask-JWT-Extended
-   **Documentação da API:** Flasgger (Swagger UI)
-   **Web Scraping:** Requests e BeautifulSoup4
-   **Manipulação de Dados:** Pandas
-   **Servidor WSGI (Produção):** Gunicorn

#### Estrutura de Diretórios
```
/seu_projeto/
├── app/
│   ├── __init__.py      # Fábrica da aplicação (create_app)
│   ├── models.py        # Definição das tabelas (User, Recipe, Book)
│   ├── routes.py        # Rotas principais (User, Recipe, Search)
│   └── routes_scrape.py # Rota de scraping
│
├── migrations/          # Arquivos de migração do Flask-Migrate
├── config.py            # Configurações da aplicação
├── run.py               # Ponto de entrada para executar a aplicação
├── requirements.txt     # Dependências do projeto
└── vercel.json          # Configuração de deploy para a Vercel
```

## Instruções de Instalação e Configuração

### Pré-requisitos
-   Python 3.10 ou superior
-   `pip` (gerenciador de pacotes do Python)
-   `git`

### Passos para Instalação

1.  **Clone o repositório:**
    ```sh
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_SEU_PROJETO>
    ```

2.  **Crie e ative um ambiente virtual:**
    -   **Windows:**
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   **macOS / Linux:**
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis. Este arquivo não deve ser enviado para o repositório git.
    ```env
    # .env
    SECRET_KEY='uma-chave-secreta-bem-forte-para-flask'
    JWT_SECRET_KEY='outra-chave-secreta-forte-para-jwt'
    # DATABASE_URL='sqlite:///app.db' # (Opcional, já é o padrão no config.py)
    ```

5.  **Aplique as Migrações do Banco de Dados:**
    Este comando criará o arquivo de banco de dados (`app.db` ou `recipes.db`) e todas as tabelas necessárias.
    ```sh
    # Certifique-se de definir a variável FLASK_APP
    # Windows: set FLASK_APP=run.py
    # Linux/macOS: export FLASK_APP=run.py

    flask db upgrade
    ```

## Documentação das Rotas da API
A documentação completa e interativa da API é gerada automaticamente pelo Flasgger e pode ser acessada após iniciar o servidor.

**URL da Documentação:** [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

### Resumo dos Endpoints

| Método HTTP | Endpoint                                    | Descrição                                         | Autenticação Necessária |
| :---------- | :------------------------------------------ | :------------------------------------------------ | :---------------------- |
| `POST`      | `/register`                                 | Registra um novo usuário.                         | Não                     |
| `POST`      | `/login`                                    | Autentica um usuário e retorna um token JWT.      | Não                     |
| `GET`       | `/api/v1/health`                            | Verifica a saúde da API e do banco de dados.      | Não                     |
| `POST`      | `/recipes`                                  | Cria uma nova receita.                            | Sim (JWT)               |
| `GET`       | `/recipes`                                  | Lista todas as receitas.                          | Sim (JWT)               |
| `PUT`       | `/recipes/<int:recipe_id>`                  | Atualiza uma receita existente.                   | Sim (JWT)               |
| `DELETE`    | `/recipes/<int:recipe_id>`                  | Deleta uma receita.                               | Sim (JWT)               |
| `POST`      | `/scrape-books`                             | Aciona o scraping e salva novos livros no DB.     | Sim (JWT)               |
| `GET`       | `/api/v1/books/search`                      | Busca livros por título e/ou categoria.           | Sim (JWT)               |


## Exemplos de Chamadas com Requests/Responses

### 1. Registrar um Novo Usuário
**Request (`curl`):**
```sh
curl -X POST [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register) \
-H "Content-Type: application/json" \
-d '{"username": "augusto", "password": "senha123"}'
```
**Response (201 Created):**
```json
{
  "msg": "Usuário criado com sucesso"
}
```

### 2. Realizar Login
**Request (`curl`):**
```sh
curl -X POST [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) \
-H "Content-Type: application/json" \
-d '{"username": "augusto", "password": "senha123"}'
```
**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
**Guarde o `access_token` para as próximas requisições.**

### 3. Buscar Livros por Categoria (Rota Protegida)
**Request (`curl`):**
```sh
# Substitua <SEU_TOKEN> pelo token obtido no login
curl -X GET "[http://127.0.0.1:5000/api/v1/books/search?category=Poetry](http://127.0.0.1:5000/api/v1/books/search?category=Poetry)" \
-H "Authorization: Bearer <SEU_TOKEN>"
```
**Response (200 OK):**
```json
[
  {
    "availability": "In stock",
    "category": "Poetry",
    "id": 1,
    "price_incl_tax": 51.77,
    "stars": 3,
    "title": "A Light in the Attic"
  }
]
```

## Instruções para Execução

### Executando em Ambiente de Desenvolvimento
1.  Certifique-se de que seu ambiente virtual (`venv`) está ativado.
2.  Verifique se o arquivo `.env` está configurado.
3.  Execute o seguinte comando no terminal:
    ```sh
    python run.py
    ```
4.  A API estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Gerenciando o Banco de Dados
Ao modificar os modelos em `app/models.py` (adicionar/remover tabelas ou colunas), você precisa gerar uma nova migração.
```sh
# 1. Defina a variável de ambiente do Flask
# Windows: set FLASK_APP=run.py
# Linux/macOS: export FLASK_APP=run.py

# 2. Gere o arquivo de migração automático
flask db migrate -m "Uma breve descrição da sua mudança"

# 3. Aplique a mudança ao banco de dados
flask db upgrade
```
# 2. Gere o arquivo de migração automático
flask db migrate -m "Uma breve descrição da sua mudança"

# 3. Aplique a mudança ao banco de dados
flask db upgrade
```