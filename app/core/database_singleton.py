from flask_sqlalchemy import SQLAlchemy
import threading

class DatabaseSingleton:
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
        return self._db
    
    def init_app(self, app):
        self._db.init_app(app)
    
    def create_all(self):
        self._db.create_all()
    
    def drop_all(self):
        self._db.drop_all()

database = DatabaseSingleton()
db = database.db