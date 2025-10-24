from app.repositories.base_repository import BaseRepository
from app.models.entities import Suporte

class SuporteRepository(BaseRepository):
    def __init__(self):
        super().__init__(Suporte)
    
    def get_by_usuario(self, usuario_id):
        """Busca tickets por usuário"""
        return self.find_by(usuario_id=usuario_id)
    
    def get_by_status(self, status):
        """Busca tickets por status"""
        return self.find_by(status=status)
    
    def get_tickets_abertos(self):
        """Busca tickets em aberto"""
        return self.model.query.filter(self.model.status.in_(['aberto', 'em_andamento'])).all()
    
    def contar_por_status(self):
        """Conta tickets por status"""
        from sqlalchemy import func
        return dict(self.model.query.with_entities(
            self.model.status, 
            func.count(self.model.id)
        ).group_by(self.model.status).all())