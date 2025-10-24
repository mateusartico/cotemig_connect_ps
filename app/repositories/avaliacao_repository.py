from app.repositories.base_repository import BaseRepository
from app.models.entities import Avaliacao
from sqlalchemy import func

class AvaliacaoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Avaliacao)
    
    def get_by_monitoria(self, monitoria_id):
        """Busca avaliações por monitoria"""
        return self.find_by(monitoria_id=monitoria_id)
    
    def get_by_aluno(self, aluno_id):
        """Busca avaliações por aluno"""
        return self.find_by(aluno_id=aluno_id)
    
    def get_media_monitoria(self, monitoria_id):
        """Calcula média de avaliações de uma monitoria"""
        result = self.model.query.filter_by(monitoria_id=monitoria_id).with_entities(func.avg(self.model.nota)).scalar()
        return round(result, 2) if result else 0
    
    def ja_avaliou(self, aluno_id, monitoria_id):
        """Verifica se aluno já avaliou a monitoria"""
        return self.exists(aluno_id=aluno_id, monitoria_id=monitoria_id)