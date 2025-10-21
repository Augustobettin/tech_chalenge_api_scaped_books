# Tech Challenge API Scraped Books

## Descrição do Projeto e Arquitetura

Este projeto consiste em uma API RESTful desenvolvida em Flask para gerenciar uma coleção de livros obtidos através de web scraping do site 'books.toscrape.com'. A arquitetura da aplicação segue uma estrutura modular, separando a lógica da aplicação, rotas, modelos de banco de dados e configurações em diferentes arquivos, promovendo um código mais limpo e de fácil manutenção.

A aplicação utiliza as seguintes tecnologias:

-   **Flask:** Um microframework web para Python, utilizado como base para a construção da API.
-   **SQLAlchemy:** Um ORM (Object-Relational Mapper) que facilita a interação com o banco de dados.
-   **Flask-JWT-Extended:** Para gerenciamento de autenticação via tokens JWT (JSON Web Tokens).
-   **Flasgger:** Para a geração automática de uma documentação interativa da API no formato Swagger UI.
-   **requests e BeautifulSoup4:** Utilizados para realizar o web scraping e extrair os dados dos livros.
-   **pandas:** Para a manipulação e transformação dos dados extraídos.

A arquitetura da API é composta por:

-   **`app.py`**: Ponto de entrada da aplicação, responsável por criar e executar a instância do Flask.
-   **`config.py`**: Arquivo de configuração que armazena chaves secretas, configurações do banco de dados e outras variáveis de ambiente.
-   **`api/`**: Módulo que contém a lógica da aplicação, incluindo:
    -   **`__init__.py`**: Inicializa a aplicação Flask, extensões e registra os blueprints.
    -   **`routes.py`**: Define as rotas da API para autenticação, consulta de livros, categorias e estatísticas.
    -   **`routes_scape.py`**: Contém a rota e a lógica para o processo de web scraping.
    -   **`models.py`**: Define os modelos de dados (tabelas `User` e `Book`) utilizando SQLAlchemy.
-   **`requirements.txt`**: Lista todas as dependências do projeto.
-   **Scripts de Suporte**:
    -   **`populate_db.py`**: Script para popular o banco de dados local com os dados do scraping.
    -   **`migrate_db.py`**: Script para migrar os dados do banco de dados local (SQLite) para um banco de dados PostgreSQL em nuvem.
    -   **`validacao_query.py`**: Script para validar a conexão e realizar consultas no banco de dados em nuvem.

## Instruções de Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local:

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/augustobettin/tech_chalenge_api_scaped_books.git](https://github.com/augustobettin/tech_chalenge_api_scaped_books.git)
    cd tech_chalenge_api_scaped_books
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Popule o banco de dados local (SQLite):**

    Execute o script `populate_db.py` para realizar o scraping e salvar os dados em um arquivo `livros.db` na pasta `instance`.

    ```bash
    python populate_db.py
    ```

## Documentação das Rotas da API

A documentação completa e interativa da API está disponível na rota `/apidocs` quando a aplicação está em execução. Abaixo estão alguns exemplos das principais rotas.

---

### Autenticação

#### `POST /register`

Registra um novo usuário.

-   **Request:**

    ```json
    {
      "username": "novo_usuario",
      "password": "senha_segura_123"
    }
    ```

-   **Response (201):**

    ```json
    {
      "msg": "Usuário criado com sucesso"
    }
    ```

#### `POST /login`

Autentica um usuário e retorna um token de acesso.

-   **Request:**

    ```json
    {
      "username": "novo_usuario",
      "password": "senha_segura_123"
    }
    ```

-   **Response (200):**

    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

---

### Livros

#### `GET /books`

Retorna a lista de todos os livros.

-   **Response (200):**
    ```json
    [
      {
        "id": 1,
        "title": "A Light in the Attic",
        "stars": 3,
        "category": "Poetry",
        "image": "[http://example.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg](http://example.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg)",
        "upc": "a897fe39b1053632",
        "product_type": "Books",
        "price_excl_tax": 51.77,
        "price_incl_tax": 51.77,
        "tax": 0.00,
        "availability": "In stock (22 available)",
        "number_of_reviews": 0,
        "in_stock": 22
      }
    ]
    ```

#### `GET /books/<int:book_id>`

Busca um livro específico pelo ID.

-   **Response (200):**
    ```json
    {
      "id": 10,
      "title": "The Black Maria",
      "stars": 1,
      "category": "Poetry",
      "image": "[http://example.com/media/cache/df/58/df58925a2787e08f5a2a1dee588d0b3c.jpg](http://example.com/media/cache/df/58/df58925a2787e08f5a2a1dee588d0b3c.jpg)",
      "upc": "90fa61229261140a",
      "product_type": "Books",
      "price_excl_tax": 52.15,
      "price_incl_tax": 52.15,
      "tax": 0.00,
      "availability": "In stock (19 available)",
      "number_of_reviews": 0,
      "in_stock": 19
    }
    ```

#### `GET /books/search`

Pesquisa livros por título e/ou categoria.

-   **Exemplo de Chamada:** `/books/search?title=The Black&category=Poetry`
-   **Response (200):**
    ```json
    [
      {
        "id": 10,
        "title": "The Black Maria",
        "stars": 1,
        "category": "Poetry",
        // ... demais campos
      }
    ]
    ```

#### `GET /books/top-rated`

Retorna os 10 livros mais bem avaliados.

-   **Response (200):**
    ```json
    [
      {
        "id": 805,
        "title": "The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull",
        "stars": 5,
        "category": "Default",
        "price_incl_tax": 17.97
        // ... demais campos
      }
    ]
    ```

#### `GET /books/price-range`

Busca livros dentro de um intervalo de preços.

-   **Exemplo de Chamada:** `/books/price-range?min=20&max=50`
-   **Response (200):**
    ```json
    [
        {
            "id": 1,
            "title": "A Light in the Attic",
            "price_incl_tax": 51.77,
            // ... demais campos
        }
    ]
    ```

---

### Categorias

#### `GET /categories`

Retorna a lista de todas as categorias de livros.

-   **Response (200):**
    ```json
    [
      "Poetry",
      "History",
      "Science Fiction",
      "Travel",
      "Default"
    ]
    ```

---

### Estatísticas

#### `GET /stats/overview`

Retorna estatísticas gerais sobre os livros.

-   **Response (200):**
    ```json
    {
      "total_books": 1000,
      "average_price_incl_tax": 35.67,
      "average_stars": 3.25
    }
    ```

#### `GET /stats/categories`

Retorna estatísticas agrupadas por categoria.

-   **Response (200):**
    ```json
    [
      {
        "category": "Poetry",
        "total_books": 48,
        "average_price_incl_tax": 40.31,
        "average_stars": 2.85
      }
    ]
    ```

---

### Monitoramento

#### `GET /health`

Verifica a saúde da API e a conexão com o banco de dados.

-   **Response (200):**
    ```json
    {
      "status": "API está saudável",
      "database": "Conectado"
    }
    ```

## Instruções para Execução

Para executar a aplicação Flask localmente, utilize o seguinte comando no terminal, na raiz do projeto:

```bash
flask run

A API estará disponível em `http://1227.0.0.1:5000`.

### Scripts de Gerenciamento do Banco de Dados

Os seguintes scripts foram criados para facilitar a criação e o gerenciamento dos bancos de dados local e em nuvem:

-   **`populate_db.py`**: Este script executa o processo de web scraping, coleta os dados dos livros e os insere em um banco de dados **SQLite local** (`instance/livros.db`). É ideal para criar rapidamente uma base de dados para desenvolvimento e testes locais sem a necessidade de uma conexão externa.

-   **`migrate_db.py`**: Utilizado para migrar os dados do banco de dados SQLite local para um banco de dados **PostgreSQL na nuvem** (hospedado no Render). O script lê todos os livros do arquivo local e os insere na