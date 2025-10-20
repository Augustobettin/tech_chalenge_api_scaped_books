import os
from sqlalchemy import create_engine
from api import db
from api.models import Book, User
from sqlalchemy.orm import sessionmaker

# --- CONFIGURAÇÃO ---
# Cole aqui a URL de conexão EXTERNA do seu banco de dados no Render
POSTGRES_URL = "postgresql://livros_db_pl7h_user:6Zuh8WHPR5Loq8ivTd7Z20voqY5z6Dtw@dpg-d3r67jodl3ps73ceqalg-a.oregon-postgres.render.com/livros_db_pl7h"

# Caminho para o seu arquivo de banco de dados SQLite local
SQLITE_DB_PATH = 'instance/livros.db'
# --- FIM DA CONFIGURAÇÃO ---

print("--- Iniciando Script de Migração Definitivo ---")

# 1. VERIFICAR ARQUIVO DE ORIGEM
if not os.path.exists(SQLITE_DB_PATH):
    print(f"\nERRO: O arquivo SQLite não foi encontrado em '{SQLITE_DB_PATH}'.")
    exit()
print(f"\n[PASSO 1/4] Arquivo SQLite encontrado.")

# Motores de conexão
sqlite_engine = create_engine(f'sqlite:///{SQLITE_DB_PATH}')
postgres_engine = create_engine(POSTGRES_URL)
SessionSQLite = sessionmaker(bind=sqlite_engine)
SessionPostgres = sessionmaker(bind=postgres_engine)

# 2. DELETAR E RECRIAR TABELAS NO RENDER (PARA APLICAR MUDANÇAS)
print("\n[PASSO 2/4] Conectando ao Render para recriar as tabelas com os novos tamanhos...")
try:
    # Drop all tables to ensure schema changes are applied
    db.Model.metadata.drop_all(postgres_engine)
    # Create all tables based on the updated models.py
    db.Model.metadata.create_all(postgres_engine)
    print(" -> Sucesso! Tabelas recriadas no Render.")
except Exception as e:
    print(f"\nERRO CRÍTICO ao recriar tabelas no Render: {e}")
    exit()

# 3. LER DADOS DO SQLITE
print("\n[PASSO 3/4] Lendo dados do banco de dados local...")
session_sqlite = SessionSQLite()
try:
    local_books = session_sqlite.query(Book).all()
    if not local_books:
        print("\nAVISO: Nenhum livro encontrado no banco de dados local. Encerrando.")
        exit()
    print(f" -> Sucesso! {len(local_books)} livros encontrados.")
finally:
    session_sqlite.close()

# 4. INSERIR DADOS NO POSTGRESQL
print("\n[PASSO 4/4] Inserindo dados no banco de dados do Render...")
session_postgres = SessionPostgres()
try:
    for book in local_books:
        new_book = Book(
            title=book.title, stars=book.stars, category=book.category, image=book.image,
            upc=book.upc, product_type=book.product_type, price_excl_tax=book.price_excl_tax,
            price_incl_tax=book.price_incl_tax, tax=book.tax, availability=book.availability,
            number_of_reviews=book.number_of_reviews, in_stock=book.in_stock
        )
        session_postgres.add(new_book)
    
    session_postgres.commit()
    print(f"\n\n🎉 SUCESSO! 🎉\nTodos os {len(local_books)} livros foram migrados para o Render!")

except Exception as e:
    print(f"\nERRO CRÍTICO durante a inserção de dados. A transação foi revertida: {e}")
    session_postgres.rollback()
finally:
    session_postgres.close()

print("\n--- Script de Migração Finalizado ---")