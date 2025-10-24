from app.repositories.base_repository import BaseRepository
from app.models.entities import Disciplina

class DisciplinaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Disciplina)
    
    def get_ativas(self):
        """Busca disciplinas ativas"""
        return self.find_by(ativa=True)
    
    def get_by_categoria(self, categoria):
        """Busca disciplinas por categoria"""
        return self.find_by(categoria=categoria, ativa=True)
    
    def get_by_codigo(self, codigo):
        """Busca disciplina por código"""
        return self.find_one_by(codigo=codigo)