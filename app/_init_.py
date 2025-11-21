# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    # Cria a instância do Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o banco de dados
    db.init_app(app)

    # Importa os modelos (para que o SQLAlchemy reconheça)
    from . import models

    # Registrar rotas via função init_routes
    from .routes import auth_routes
    auth_routes.init_routes(app)

    return app
