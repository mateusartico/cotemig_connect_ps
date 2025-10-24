from app.repositories.base_repository import BaseRepository
from app.models.entities import Monitoria, Reserva, Presenca, Disciplina
from datetime import datetime
from sqlalchemy import or_, and_, desc

class MonitoriaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Monitoria)
    
    def get_by_monitor(self, monitor_id):
        """Busca monitorias por monitor"""
        return self.model.query.filter_by(monitor_id=monitor_id)\
                   .order_by(desc(self.model.data_hora)).all()
    
    def get_proximas(self):
        """Busca próximas monitorias agendadas"""
        return self.model.query.filter(
            self.model.data_hora >= datetime.now(),
            self.model.status == 'agendada'
        ).order_by(self.model.data_hora).all()
    
    def get_by_codigo_presenca(self, codigo):
        """Busca monitoria por código de presença"""
        return self.find_one_by(codigo_presenca=codigo)
    
    def buscar(self, termo=None, categoria=None, avaliacao_min=None):
        """Busca avançada de monitorias"""
        query = self.model.query.filter(self.model.status == 'agendada')
        
        if termo:
            termo_lower = f"%{termo.lower()}%"
            query = query.filter(or_(
                self.model.titulo.ilike(termo_lower),
                self.model.descricao.ilike(termo_lower),
                self.model.tags.ilike(termo_lower)
            ))
        
        if categoria:
            query = query.join(Disciplina).filter(Disciplina.categoria == categoria)
        
        return query.order_by(self.model.data_hora).all()
    
    def get_com_vagas(self):
        """Busca monitorias com vagas disponíveis"""
        return self.model.query.filter(
            self.model.vagas_ocupadas < self.model.vagas_total,
            self.model.status == 'agendada'
        ).all()

class ReservaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Reserva)
    
    def get_by_aluno(self, aluno_id):
        return self.model.query.filter_by(aluno_id=aluno_id, status='confirmada').all()
    
    def get_by_monitoria(self, monitoria_id):
        return self.model.query.filter_by(monitoria_id=monitoria_id, status='confirmada').all()
    
    def existe_reserva(self, aluno_id, monitoria_id):
        return self.model.query.filter_by(
            aluno_id=aluno_id, 
            monitoria_id=monitoria_id,
            status='confirmada'
        ).first() is not None

class PresencaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Presenca)
    
    def get_by_monitoria(self, monitoria_id):
        return self.model.query.filter_by(monitoria_id=monitoria_id).all()
    
    def existe_presenca(self, aluno_id, monitoria_id):
        return self.model.query.filter_by(
            aluno_id=aluno_id,
            monitoria_id=monitoria_id
        ).first() is not None

class DisciplinaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Disciplina)
    
    def get_ativas(self):
        return self.model.query.filter_by(ativa=True).all()