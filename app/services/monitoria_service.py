from app.repositories.monitoria_repository import MonitoriaRepository, ReservaRepository, PresencaRepository
from app.core.observer import monitoria_subject
from app.core.factory import EntityFactoryProvider

class MonitoriaService:
    def __init__(self):
        self.monitoria_repo = MonitoriaRepository()
        self.reserva_repo = ReservaRepository()
        self.presenca_repo = PresencaRepository()
    
    def criar_monitoria(self, dados_monitoria):
        monitoria = EntityFactoryProvider.create_entity('monitoria', **dados_monitoria)
        monitoria = self.monitoria_repo.save(monitoria)
        
        monitoria_subject.criar_monitoria({
            'id': monitoria.id,
            'titulo': monitoria.titulo,
            'monitor_id': monitoria.monitor_id
        })
        
        return monitoria
    
    def reservar_vaga(self, aluno_id, monitoria_id):
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        
        if not monitoria:
            raise ValueError("Monitoria não encontrada")
        
        if monitoria.vagas_disponiveis <= 0:
            raise ValueError("Não há vagas disponíveis")
        
        if self.reserva_repo.existe_reserva(aluno_id, monitoria_id):
            raise ValueError("Você já tem reserva nesta monitoria")
        
        reserva = self.reserva_repo.create(aluno_id=aluno_id, monitoria_id=monitoria_id)
        
        monitoria.vagas_ocupadas += 1
        self.monitoria_repo.save(monitoria)
        
        return reserva
    
    def cancelar_reserva(self, aluno_id, monitoria_id):
        reserva = self.reserva_repo.find_one_by(
            aluno_id=aluno_id, 
            monitoria_id=monitoria_id, 
            status='confirmada'
        )
        
        if not reserva:
            raise ValueError("Reserva não encontrada")
        
        reserva.status = 'cancelada'
        self.reserva_repo.save(reserva)
        
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        monitoria.vagas_ocupadas -= 1
        self.monitoria_repo.save(monitoria)
        
        return reserva
    
    def iniciar_monitoria(self, monitor_id, monitoria_id):
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        
        if not monitoria or monitoria.monitor_id != monitor_id:
            raise ValueError("Monitoria não encontrada")
        
        if monitoria.status != 'agendada':
            raise ValueError("Monitoria não pode ser iniciada")
        
        codigo = monitoria.gerar_codigo_presenca()
        monitoria.status = 'em_andamento'
        self.monitoria_repo.save(monitoria)
        
        return codigo
    
    def finalizar_monitoria(self, monitor_id, monitoria_id):
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        
        if not monitoria or monitoria.monitor_id != monitor_id:
            raise ValueError("Monitoria não encontrada")
        
        if monitoria.status != 'em_andamento':
            raise ValueError("Monitoria não está em andamento")
        
        monitoria.status = 'finalizada'
        self.monitoria_repo.save(monitoria)
        
        monitoria_subject.finalizar_monitoria({'id': monitoria_id})
        
        return monitoria
    
    def registrar_presenca(self, aluno_id, codigo_presenca):
        monitoria = self.monitoria_repo.get_by_codigo_presenca(codigo_presenca)
        
        if not monitoria:
            raise ValueError("Código inválido")
        
        if not self.reserva_repo.existe_reserva(aluno_id, monitoria.id):
            raise ValueError("Você não tem reserva nesta monitoria")
        
        if self.presenca_repo.existe_presenca(aluno_id, monitoria.id):
            raise ValueError("Presença já registrada")
        
        presenca = self.presenca_repo.create(
            aluno_id=aluno_id, 
            monitoria_id=monitoria.id
        )
        
        return presenca