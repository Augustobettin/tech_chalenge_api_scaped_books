# /migrate_db.py
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# --- CONFIGURAÇÃO ---
# Cole aqui a URL de conexão EXTERNA do seu banco de dados no Render
POSTGRES_URL = "postgresql://bookdb_x3tc_user:6TdR9gSFdmZ2MDHA4g7MJL53p9tmhmeI@dpg-d3r42gs9c44c73d65icg-a.oregon-postgres.render.com/bookdb_x3tc"

# Caminho para o seu arquivo de banco de dados SQLite local
SQLITE_DB_PATH = 'instance/livros.db'

# --- NÃO ALTERE ABAIXO DESTA LINHA ---

print("Iniciando o script de migração...")

# Motores (Engines) de conexão para os dois bancos de dados
try:
    sqlite_engine = create_engine(f'sqlite:///{SQLITE_DB_PATH}')
    postgres_engine = create_engine(POSTGRES_URL)
    print("Motores de banco de dados criados com sucesso.")
except Exception as e:
    print(f"Erro ao criar os motores de banco de dados: {e}")
    exit()

# Criando sessões para interagir com os bancos
SessionSQLite = sessionmaker(bind=sqlite_engine)
SessionPostgres = sessionmaker(bind=postgres_engine)

@contextmanager
def session_scope(session_class):
    """Provide a transactional scope around a series of operations."""
    session = session_class()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro na sessão: {e}")
        raise
    finally:
        session.close()

def migrate_table(table_name):
    """Lê dados do SQLite e insere no PostgreSQL."""
    print(f"\nIniciando migração da tabela: '{table_name}'...")
    
    try:
        # Lê todos os dados da tabela do SQLite para um DataFrame do Pandas
        with session_scope(SessionSQLite) as s:
            df = pd.read_sql_table(table_name, s.bind)
        
        if df.empty:
            print(f"Tabela '{table_name}' está vazia no banco de dados de origem. Pulando.")
            return

        print(f"Encontrados {len(df)} registros na tabela '{table_name}'.")

        # Insere os dados do DataFrame na tabela correspondente no PostgreSQL
        # 'if_exists="append"' adiciona os dados sem apagar os existentes
        # 'index=False' evita que o índice do DataFrame seja salvo como uma coluna
        df.to_sql(table_name, postgres_engine, if_exists='append', index=False)
        
        print(f"Tabela '{table_name}' migrada com sucesso!")

    except Exception as e:
        print(f"ERRO ao migrar a tabela '{table_name}': {e}")


if __name__ == '__main__':
    # Antes de migrar, precisamos criar as tabelas no PostgreSQL.
    # Usaremos o contexto da sua aplicação Flask para isso.
    from api import create_app, db
    
    print("\nCriando o contexto da aplicação para garantir que as tabelas existam no destino...")
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Cria todas as tabelas (se ainda não existirem) no banco PostgreSQL
        db.create_all()
        print("Verificação de tabelas no destino concluída.")

    # Lista das tabelas a serem migradas (geralmente as que estão no seu models.py)
    # A ordem pode ser importante se houver chaves estrangeiras.
    tables_to_migrate = ['user', 'book']
    
    for table in tables_to_migrate:
        migrate_table(table)
        
    print("\nMigração de dados concluída!")