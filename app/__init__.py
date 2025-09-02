from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Registrar blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.monitoria_controller import monitoria_bp
    from app.controllers.busca_controller import busca_bp
    from app.controllers.avaliacao_controller import avaliacao_bp
    from app.controllers.suporte_controller import suporte_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(monitoria_bp)
    app.register_blueprint(busca_bp)
    app.register_blueprint(avaliacao_bp)
    app.register_blueprint(suporte_bp)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app