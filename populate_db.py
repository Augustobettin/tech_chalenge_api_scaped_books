import os
from api import create_app, db
from api.models import Book
from api.routes_scape import scrape_books

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/livros.db'

with app.app_context():
    print("Contexto da aplicação carregado.")

    
    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    print(f"Verificando se a pasta '{instance_path}' existe.")

    db.create_all()
    print("Tabelas verificadas/criadas no banco de dados local.")

    print("\nIniciando o processo de scraping para popular o banco de dados...")
    books_df = scrape_books()

    if books_df.empty:
        print("Nenhum livro encontrado durante o scraping.")
    else:
        print(f"Scraping concluído. {len(books_df)} livros encontrados.")
        print("Inserindo livros no banco de dados local...")
        
        books_to_add = books_df.to_dict(orient='records')

        for book_data in books_to_add:
            # Cria um novo objeto 'Book' com os dados do scraping
            new_book = Book(
                title=book_data.get('title'),
                stars=book_data.get('stars'),
                category=book_data.get('category'),
                image=book_data.get('image'),
                upc=book_data.get('UPC'),
                product_type=book_data.get('product_type'),
                price_excl_tax=book_data.get('price_excl_tax'),
                price_incl_tax=book_data.get('price_incl_tax'),
                tax=book_data.get('tax'),
                availability=book_data.get('availability'),
                number_of_reviews=book_data.get('number_of_reviews'),
                in_stock=book_data.get('in_stock')
            )
            db.session.add(new_book)
        
        db.session.commit()
        print(f"\nSUCESSO! {len(books_to_add)} livros foram salvos no arquivo 'instance/livros.db'.")