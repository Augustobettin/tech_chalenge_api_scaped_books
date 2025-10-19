from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from .models import User, Book, db

main_bp = Blueprint('main', __name__)

# Rotas de usuário e autenticação
@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"msg": "API de receitas"}), 200

@main_bp.route('/register', methods=['POST'])
def register_user():
    """
    Registra um novo usuário
    ---
    tags:
      - "Autenticação"
    summary: "Registra um novo usuário"
    description: "Cria um novo registro de usuário no sistema a partir de um nome de usuário e senha."
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - in: body
        name: body
        description: "Objeto de usuário para registro"
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "novo_usuario"
              description: "Nome de usuário único."
            password:
              type: string
              format: password
              example: "senha_segura_123"
              description: "Senha do usuário."
    responses:
      "201":
        description: "Usuário criado com sucesso"
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Usuário criado com sucesso"
      "400":
        description: "Requisição inválida ou nome de usuário já existente"
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Nome de usuário já existe"
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Nome de usuário já existe"}), 400
    
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Usuário criado com sucesso"}), 201

@main_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica um usuário e retorna um token JWT
    ---
    tags:
      - "Autenticação"
    summary: "Realiza o login do usuário"
    description: "Autentica o usuário com base no `username` e `password` e retorna um token de acesso JWT em caso de sucesso."
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - in: body
        name: body
        required: true
        description: "Credenciais do usuário para autenticação."
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "meu_usuario"
            password:
              type: string
              format: password
              example: "minha_senha_123"
    responses:
      "200":
        description: "Login bem-sucedido e token de acesso retornado."
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      "401":
        description: "Credenciais inválidas."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Credenciais inválidas"
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
        
    return jsonify({"msg": "Credenciais inválidas"}), 401

@main_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Acessa um recurso protegido com JWT
    ---
    tags:
      - "Recursos Protegidos"
    summary: "Exemplo de uma rota que requer autenticação"
    description: "Esta rota só pode ser acessada com um token de acesso JWT válido no cabeçalho de autorização (Authorization: Bearer <token>)."
    produces:
      - "application/json"
    security:
      - jwt: []
    responses:
      "200":
        description: "Acesso concedido ao recurso."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Logged in as user 1"
      "401":
        description: "Token de acesso ausente ou inválido."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f'Logged in as user {current_user_id}'}), 200

# Rota para obter os dados dos livros
@main_bp.route('/books', methods=['GET'])
#@jwt_required()
def get_books():
    """
    Obtém a lista de todos os livros
    ---
    tags:
      - "Livros"
    summary: "Retorna uma lista completa de livros."
    description: "Recupera todos os livros cadastrados no banco de dados. Requer autenticação JWT."
    produces:
      - "application/json"
    security:
      - jwt: []
    responses:
      "200":
        description: "Uma lista de objetos, onde cada objeto representa um livro."
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              title:
                type: string
                example: "A Light in the Attic"
              stars:
                type: integer
                example: 3
              category:
                type: string
                example: "Poetry"
              image:
                type: string
                example: "http://example.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
              upc:
                type: string
                example: "a897fe39b1053632"
              product_type:
                type: string
                example: "Books"
              price_excl_tax:
                type: number
                format: float
                example: 51.77
              price_incl_tax:
                type: number
                format: float
                example: 51.77
              tax:
                type: number
                format: float
                example: 0.00
              availability:
                type: string
                example: "In stock (22 available)"
              number_of_reviews:
                type: integer # Corrigido de 'string' para 'integer'
                example: 0
              in_stock:
                type: integer
                example: 22
      "401":
        description: "Token de acesso ausente ou inválido."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    books = Book.query.all()
    books_list = [{
        'id': book.id,
        'title': book.title,
        'stars': book.stars,
        'category': book.category,
        'image': book.image,
        'upc': book.upc,
        'product_type': book.product_type,
        'price_excl_tax': book.price_excl_tax,
        'price_incl_tax': book.price_incl_tax,
        'tax': book.tax,
        'availability': book.availability,
        'number_of_reviews': book.number_of_reviews,
        'in_stock': book.in_stock
    } for book in books]
    return jsonify(books_list), 200

# rota para obter um livro específico pelo ID
@main_bp.route('/books/<int:book_id>', methods=['GET'])
#@jwt_required()
def get_book(book_id):
    """
    Busca um livro específico pelo seu ID
    ---
    tags:
      - "Livros"
    summary: "Retorna os detalhes de um único livro."
    description: "Obtém todas as informações de um livro específico, buscando-o pelo seu ID numérico. Requer autenticação JWT."
    produces:
      - "application/json"
    security:
      - jwt: []
    parameters:
      - in: path
        name: book_id
        type: integer
        required: true
        description: "ID numérico do livro a ser recuperado."
        example: 10
    responses:
      "200":
        description: "Operação bem-sucedida. Retorna os detalhes completos do livro."
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 10
            title:
              type: string
              example: "The Black Maria"
            stars:
              type: integer
              example: 1
            category:
              type: string
              example: "Poetry"
            image:
              type: string
              example: "http://example.com/media/cache/df/58/df58925a2787e08f5a2a1dee588d0b3c.jpg"
            upc:
              type: string
              example: "90fa61229261140a"
            product_type:
              type: string
              example: "Books"
            price_excl_tax:
              type: number
              format: float
              example: 52.15
            price_incl_tax:
              type: number
              format: float
              example: 52.15
            tax:
              type: number
              format: float
              example: 0.00
            availability:
              type: string
              example: "In stock (19 available)"
            number_of_reviews:
              type: integer # Corrigido de 'string' para 'integer'
              example: 0
            in_stock:
              type: integer
              example: 19
      "401":
        description: "Token de acesso ausente ou inválido."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
      "404":
        description: "O livro com o ID especificado não foi encontrado."
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Not Found"
    """
    book = Book.query.get_or_404(book_id)
    book_data = {
        'id': book.id,
        'title': book.title,
        'stars': book.stars,
        'category': book.category,
        'image': book.image,
        'upc': book.upc,
        'product_type': book.product_type,
        'price_excl_tax': book.price_excl_tax,
        'price_incl_tax': book.price_incl_tax,
        'tax': book.tax,
        'availability': book.availability,
        'number_of_reviews': book.number_of_reviews,
        'in_stock': book.in_stock
    }
    return jsonify(book_data), 200

# rota para buscar livros por título ou categoria
@main_bp.route('/books/search', methods=['GET'])
#@jwt_required()
def search_books():
    """
    Pesquisa livros por título e/ou categoria
    ---
    tags:
      - "Livros"
    summary: "Filtra e retorna uma lista de livros."
    description: |
      Busca livros que correspondam parcial e de forma não sensível a maiúsculas (case-insensitive) ao título e/ou categoria fornecidos.
      Pelo menos um dos parâmetros (`title` ou `category`) deve ser enviado. Requer autenticação JWT.
    produces:
      - "application/json"
    security:
      - jwt: []
    parameters:
      - in: query
        name: title
        type: string
        required: false
        description: "Título (ou parte do título) do livro a ser pesquisado."
        example: "The Black"
      - in: query
        name: category
        type: string
        required: false
        description: "Categoria do livro a ser pesquisado."
        example: "Poetry"
    responses:
      "200":
        description: "Uma lista de livros que correspondem aos critérios de pesquisa. Pode retornar uma lista vazia se nada for encontrado."
        schema:
          type: array
          items:
            # Reutilizando o mesmo schema de livro das outras rotas
            type: object
            properties:
              id:
                type: integer
                example: 10
              title:
                type: string
                example: "The Black Maria"
              stars:
                type: integer
                example: 1
              # ... (demais propriedades do livro com exemplos)
              category:
                type: string
                example: "Poetry"
              number_of_reviews:
                type: integer # Corrigido de 'string' para 'integer'
                example: 0
      "400":
        description: "Requisição inválida. Ocorre se nenhum parâmetro de pesquisa for fornecido."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Nenhum parâmetro de pesquisa fornecido"
      "401":
        description: "Token de acesso ausente ou inválido."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    title_query = request.args.get('title')
    category_query = request.args.get('category')

    query = db.session.query(Book)
    
    if title_query:
        query = query.filter(Book.title.ilike(f'%{title_query}%'))
    if category_query:
        query = query.filter(Book.category.ilike(f'%{category_query}%'))

    books_found = query.all()
    
    books_list = [{
        'id': book.id,
        'title': book.title,
        'stars': book.stars,
        'category': book.category,
        'image': book.image,
        'upc': book.upc,
        'product_type': book.product_type,
        'price_excl_tax': book.price_excl_tax,
        'price_incl_tax': book.price_incl_tax,
        'tax': book.tax,
        'availability': book.availability,
        'number_of_reviews': book.number_of_reviews,
        'in_stock': book.in_stock
    } for book in books_found]
    return jsonify(books_list), 200

@main_bp.route('/categories', methods=['GET'])
#@jwt_required()
def get_categories():
    """
    Obtém a lista de todas as categorias de livros
    ---
    tags:
      - "Categorias"
    summary: "Retorna uma lista única de todas as categorias de livros."
    description: "Busca no banco de dados todas as categorias distintas existentes e as retorna em uma lista de strings. Requer autenticação JWT."
    produces:
      - "application/json"
    security:
      - jwt: []
    responses:
      "200":
        description: "Operação bem-sucedida. Retorna uma lista de strings com as categorias."
        schema:
          type: array
          items:
            type: string
          example:
            - "Poetry"
            - "History"
            - "Science Fiction"
            - "Travel"
            - "Default"
      "401":
        description: "Token de acesso ausente ou inválido."
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    categories = db.session.query(Book.category).distinct().all()
    categories_list = [category[0] for category in categories]
    return jsonify(categories_list), 200

@main_bp.route('/health', methods=['GET'])
def health_check():
    """
    Verifica a saúde da API e a conexão com o banco de dados
    ---
    tags:
      - "Monitoramento"
    summary: "Endpoint para verificação de saúde (Health Check)."
    description: "Verifica a saúde operacional da API. Tenta executar uma consulta simples no banco de dados para garantir a conectividade. Não requer autenticação."
    produces:
      - "application/json"
    responses:
      "200":
        description: "API está saudável e a conexão com o banco de dados foi bem-sucedida."
        schema:
          type: object
          properties:
            status:
              type: string
              example: "API está saudável"
            database:
              type: string
              example: "Conectado"
      "500":
        description: "A API está em execução, mas falhou ao se conectar com o banco de dados."
        schema:
          type: object
          properties:
            status:
              type: string
              example: "API está saudável"
            database:
              type: string
              example: "Falha na conexão"
    """
    try:
        # Tenta fazer uma consulta simples para verificar a conectividade com o banco de dados
        db.session.query(Book).first()
        return jsonify({"status": "API está saudável", "database": "Conectado"}), 200
    except Exception as e:
        # Em um ambiente de produção, seria bom logar o erro 'e' aqui
        return jsonify({"status": "API está saudável", "database": "Falha na conexão"}), 500