from app.repositories.base_repository import BaseRepository
from app.models.entities import HistoricoBusca
from sqlalchemy import desc

class HistoricoBuscaRepository(BaseRepository):
    def __init__(self):
        super().__init__(HistoricoBusca)
    
    def get_by_usuario(self, usuario_id, limit=10):
        """Busca histórico por usuário com limite"""
        return self.model.query.filter_by(usuario_id=usuario_id)\
                   .order_by(desc(self.model.created_at))\
                   .limit(limit).all()
    
    def get_termos_populares(self, limit=5):
        """Busca termos mais pesquisados"""
        from sqlalchemy import func
        return self.model.query.with_entities(
            self.model.termo_busca,
            func.count(self.model.id).label('count')
        ).group_by(self.model.termo_busca)\
         .order_by(desc('count'))\
         .limit(limit).all()
    
    def limpar_historico_usuario(self, usuario_id):
        """Remove histórico de um usuário"""
        self.model.query.filter_by(usuario_id=usuario_id).delete()
        from app.core.database_singleton import db
        db.session.commit()