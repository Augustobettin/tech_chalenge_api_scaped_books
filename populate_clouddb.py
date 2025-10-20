import os
from api import create_app, db
from api.models import Book
from api.routes_scape import scrape_books  

database_url = os.environ.get('DATABASE_URL')

if not database_url:
    print("Erro: A variável de ambiente DATABASE_URL não está configurada.")
else:
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    with app.app_context():
        print("Conectado ao banco de dados. Iniciando o scraping...")
        
        try:
            books_df = scrape_books(pages=1)
            
            if books_df.empty:
                print("Nenhum livro encontrado durante o scraping.")
            else:
                books_data_list = books_df.to_dict(orient='records')

                new_books_count = 0
                for book_item in books_data_list:
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
                
                db.session.commit()
                print(f"Scraping concluído! {new_books_count} novos livros adicionados.")

        except Exception as e:
            db.session.rollback()
            print(f"Ocorreu um erro durante o scraping: {str(e)}")