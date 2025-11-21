import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_qualquer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração do banco SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'

    # Configurações adicionais para estabilidade
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
