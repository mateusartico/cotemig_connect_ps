"""
Padrão Singleton para gerenciar conexão única com o banco de dados
"""
from flask_sqlalchemy import SQLAlchemy
import threading

class DatabaseSingleton:
    """
    Implementação do padrão Singleton para garantir uma única instância
    de conexão com o banco de dados em toda a aplicação.
    """
    _instance = None
    _lock = threading.Lock()
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                    cls._db = SQLAlchemy()
        return cls._instance
    
    @property
    def db(self):
        """Retorna a instância única do SQLAlchemy"""
        return self._db
    
    def init_app(self, app):
        """Inicializa a aplicação Flask com o banco de dados"""
        self._db.init_app(app)
    
    def create_all(self):
        """Cria todas as tabelas do banco"""
        self._db.create_all()
    
    def drop_all(self):
        """Remove todas as tabelas do banco"""
        self._db.drop_all()

# Instância global do singleton
database = DatabaseSingleton()
db = database.db