import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import jsonify, Blueprint
import datetime

hoje = datetime.date.today()

from .models import db, Book

scrape_bp = Blueprint('scrape', __name__)

def scrape_books(pages = 50):
    """
    Fazendo o scraping dos livros 
    ---
    Parâmetros:
      - pages: número de páginas a serem raspadas (padrão é 50)
    Retorna:
      - DataFrame com os dados dos livros raspados
    """
    #Só para acompanhar o progresso
    print("Iniciando o scraping ...")

    # A melhorar: primeira etapa é obter os links de todas as 50 paginas do site
    url = 'https://books.toscrape.com/catalogue/'
    page = 'page-'
    final_url = '.html'

    # Instanciando lista para armazenar os links
    pool_link = []

    for i in range(1, pages + 1): #51
        print(f'Obtendo links da pagina {i}')
        response = requests.get(url + page + str(i) + final_url)
        content = response.content
        suop_books = BeautifulSoup(content, 'html.parser')
        bookshelf = suop_books.findAll("li",{"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})
        for books in bookshelf:
            link = books.select_one('a').get('href')
            pool_link.append(link)
    
    print(f'Foram encontrados {len(pool_link)} links de livros.')

    # Agora vamos fazer o scraping dos livros
    # Instanciando lista para armazenar as informações dos livros
    product_info = []

    for link in pool_link:
        response_book = requests.get(url + link)
        content_book = response_book.content
        suop_book = BeautifulSoup(content_book, 'html.parser')

        ###############
        # get information from page 
        informacoes_produto = {}
        # titulo
        informacoes_produto['title'] = suop_book.find('title').get_text().strip()
        # disponibilidade
        # informacoes_produto['availability'] = suop_book.find("p",{"class":"instock availability"}).get_text().strip()
        # stars
        informacoes_produto['stars'] = suop_book.find("p",{"class":"star-rating"}).get("class")[1]
        # categoria
        informacoes_produto['category'] = suop_book.select_one('ul.breadcrumb li:nth-last-child(2) a').get_text()
        # imagem
        informacoes_produto['image'] = suop_book.find('img').get('src')
        # infos tabela produto  
        temp_table = suop_book.find('table', class_='table-striped')

        for linha in temp_table.find_all('tr'):
            chave = linha.find('th').get_text()
            valor = linha.find('td').get_text()
            informacoes_produto[chave] = valor

        product_info.append(informacoes_produto)
    
    df_books = pd.DataFrame(product_info)
    # limpeza e transformação dos dados
    df_books.rename(columns={'Product Type':'product_type',
                             'Price (excl. tax)':'price_excl_tax',
                             'Price (incl. tax)':'price_incl_tax',
                             'Availability':'availability',
                             'Tax':'tax',
                             'Number of reviews':'number_of_reviews'},
                            inplace=True)
    
    df_books['in_stock'] = df_books['availability'].str.extract('(\d+)').astype(int)
    df_books["availability"] = df_books["availability"].str.extract(r'^(.*?)\s*\(')
    df_books['stars'] = df_books['stars'].map({'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5})
    df_books['price_excl_tax'] = df_books['price_excl_tax'].str.replace('£','').astype(float)
    df_books['price_incl_tax'] = df_books['price_incl_tax'].str.replace('£','').astype(float)
    df_books['tax'] = df_books['tax'].str.replace('£','').astype(float)
    df_books['number_of_reviews'] = df_books['number_of_reviews'].astype(int)
    df_books.to_csv(f'./data/books_{hoje}.csv', index=False)    

    return df_books
 