from flask import Flask
from config.config import Config
from app.core.database_singleton import database, db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    database.init_app(app)
    

    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.monitoria_controller import monitoria_bp
    from app.controllers.busca_controller import busca_bp
    from app.controllers.avaliacao_controller import avaliacao_bp
    from app.controllers.suporte_controller import suporte_bp
    from app.controllers.notificacao_controller import notificacao_bp
    from app.controllers.favorito_controller import favorito_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(monitoria_bp)
    app.register_blueprint(busca_bp)
    app.register_blueprint(avaliacao_bp)
    app.register_blueprint(suporte_bp)
    app.register_blueprint(notificacao_bp)
    app.register_blueprint(favorito_bp)
    

    with app.app_context():
        database.create_all()
    
    return app