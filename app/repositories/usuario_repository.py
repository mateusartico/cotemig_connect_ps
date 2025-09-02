from app.repositories.base_repository import BaseRepository
from app.models.entities import Usuario

class UsuarioRepository(BaseRepository):
    def __init__(self):
        super().__init__(Usuario)
    
    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
    def get_by_codigo_verificacao(self, codigo):
        return self.model.query.filter_by(codigo_verificacao=codigo).first()
    
    def get_by_reset_token(self, token):
        return self.model.query.filter_by(reset_token=token).first()
    
    def get_monitores(self):
        return self.model.query.filter_by(tipo='monitor', ativo=True).all()
    
    def get_alunos(self):
        return self.model.query.filter_by(tipo='aluno', ativo=True).all()