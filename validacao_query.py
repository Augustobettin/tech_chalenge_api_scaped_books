import pandas as pd
from sqlalchemy import create_engine, text

# 1. COLE A SUA URL DE CONEXÃO EXTERNA AQUI
#    (Lembre-se de substituir 'seu_usuario', 'sua_senha', etc.)
POSTGRES_URL = "postgresql://livros_db_pl7h_user:6Zuh8WHPR5Loq8ivTd7Z20voqY5z6Dtw@dpg-d3r67jodl3ps73ceqalg-a.oregon-postgres.render.com/livros_db_pl7h"

# 2. ESCREVA A SUA QUERY SQL AQUI
#    (Você pode alterar este comando para qualquer select que quiser)
sql_query = text("SELECT * FROM book LIMIT 10;")

# --- O script abaixo se conecta e executa a query ---

print("Tentando conectar ao banco de dados no Render...")

try:
    # Cria o motor de conexão com o banco de dados
    engine = create_engine(POSTGRES_URL)

    # Usa o motor para se conectar e executar a query
    with engine.connect() as connection:
        # Usa o Pandas para ler o resultado da query e transformá-lo em uma tabela (DataFrame)
        df = pd.read_sql(sql_query, connection)

        print("\nConsulta executada com sucesso! Resultados:")
        
        # Imprime a tabela de resultados
        print(df.to_string())

except Exception as e:
    print(f"\nOcorreu um erro ao tentar conectar ou executar a query: {e}")
    print("Por favor, verifique se a sua 'External Connection String' está correta.")