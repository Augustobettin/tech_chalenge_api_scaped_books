import os
from dotenv import load_dotenv

load_dotenv() 

print("Iniciando script para popular o banco de dados...")

from api import create_app, db
from api.models import Book
from api.routes_scape import scrape_books # Importamos sua função de scraping

app = create_app()

def seed_database():
    """
    Função principal que faz o scraping e salva os livros no banco de dados.
    """
    with app.app_context():
        print("Criando todas as tabelas (se não existirem)...")
        # Garante que todas as tabelas estão criadas no banco de dados do Neon
        db.create_all()

        print("Iniciando o processo de scraping...")
        # Chama sua função para obter o DataFrame de livros
        books_df = scrape_books()

        if books_df.empty:
            print("Nenhum livro encontrado durante o scraping. O script será encerrado.")
            return

        print(f"{len(books_df)} livros encontrados. Inserindo no banco de dados...")
        
        books_data_list = books_df.to_dict(orient='records')
        
        new_books_count = 0
        for book_item in books_data_list:
            # Verifica se o livro já existe pelo UPC (código de barras), que deve ser único
            existing_book = Book.query.filter_by(upc=book_item.get('UPC')).first()
            if existing_book:
                continue # Pula para o próximo se o livro já existir

            new_book = Book(
                title=book_item.get('title'),
                stars=book_item.get('stars'),
                category=book_item.get('category'),
                image=book_item.get('image'),
                upc=book_item.get('UPC'),
                product_type=book_item.get('product_type'),
                price_excl_tax=book_item.get('price_excl_tax'),
                price_incl_tax=book_item.get('price_incl_tax'),
                tax=book_item.get('tax'),
                availability=book_item.get('availability'),
                number_of_reviews=book_item.get('number_of_reviews'),
                in_stock=book_item.get('in_stock')
            )
            db.session.add(new_book)
            new_books_count += 1
        
        print(f"Adicionando {new_books_count} novos livros à sessão...")
        db.session.commit()
        print("Dados salvos no banco de dados com sucesso!")

# Executa a função quando o script é chamado diretamente
if __name__ == '__main__':
    seed_database()