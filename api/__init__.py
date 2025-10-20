from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config

# Cria instâncias das extensões SEM associá-las a uma aplicação ainda
db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()

def create_app(config_class=Config):
    """
    Função que cria e configura a aplicação Flask (Application Factory).
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Associa as instâncias das extensões com a aplicação 'app'
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    # Importa e registra as rotas (Blueprints)
    from .routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/api/v1')
    
    from .routes_scape import scrape_bp
    app.register_blueprint(scrape_bp)

    # Importa os modelos para que o SQLAlchemy saiba sobre eles
    with app.app_context():
        from . import models
        


    return app