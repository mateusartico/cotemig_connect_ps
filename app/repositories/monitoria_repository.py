from app.repositories.base_repository import BaseRepository
from app.models.entities import Monitoria, Reserva, Presenca, Disciplina
from datetime import datetime

class MonitoriaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Monitoria)
    
    def get_by_monitor(self, monitor_id):
        return self.model.query.filter_by(monitor_id=monitor_id).order_by(Monitoria.data_hora.desc()).all()
    
    def get_proximas(self):
        return self.model.query.filter(
            Monitoria.data_hora >= datetime.now(),
            Monitoria.status == 'agendada'
        ).order_by(Monitoria.data_hora).all()
    
    def get_by_codigo_presenca(self, codigo):
        return self.model.query.filter_by(codigo_presenca=codigo).first()

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