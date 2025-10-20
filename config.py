import os

class Config:
    SECRET_KEY = 'fiab_ml_engineer'
    CACHE_TYPE = 'simple'
    SWAGGER = {
        'title': 'API de scrapping de livros',
        'uiversion': 3
    }
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///livros.db')
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///livros.db'
    SQKLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'fiap_ml_engineer_jwt'