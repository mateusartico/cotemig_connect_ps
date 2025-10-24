from app.repositories.notificacao_repository import NotificacaoRepository
from app.repositories.monitoria_repository import MonitoriaRepository, ReservaRepository
from app.repositories.usuario_repository import UsuarioRepository
from datetime import datetime, timedelta

class NotificacaoService:
    def __init__(self):
        self.notificacao_repo = NotificacaoRepository()
        self.monitoria_repo = MonitoriaRepository()
        self.reserva_repo = ReservaRepository()
        self.usuario_repo = UsuarioRepository()
    
    def gerar_notificacoes_automaticas(self):
        self._notificar_monitorias_proximas()
        self._notificar_vagas_limitadas()
        self._notificar_avaliacoes_pendentes()
    
    def _notificar_monitorias_proximas(self):
        amanha = datetime.now() + timedelta(days=1)
        inicio_dia = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_dia = amanha.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        monitorias = self.monitoria_repo.model.query.filter(
            self.monitoria_repo.model.data_hora.between(inicio_dia, fim_dia),
            self.monitoria_repo.model.status == 'agendada'
        ).all()
        
        for monitoria in monitorias:
            reservas = self.reserva_repo.find_by(monitoria_id=monitoria.id, status='confirmada')
            for reserva in reservas:
                self.notificacao_repo.criar_notificacao(
                    usuario_id=reserva.aluno_id,
                    titulo="Monitoria amanhã",
                    mensagem=f"Você tem a monitoria '{monitoria.titulo}' agendada para amanhã às {monitoria.data_hora.strftime('%H:%M')}",
                    tipo="lembrete_monitoria"
                )
    
    def _notificar_vagas_limitadas(self):
        monitorias = self.monitoria_repo.model.query.filter(
            self.monitoria_repo.model.status == 'agendada',
            self.monitoria_repo.model.data_hora > datetime.now()
        ).all()
        
        for monitoria in monitorias:
            if monitoria.vagas_disponiveis <= 2 and monitoria.vagas_disponiveis > 0:
                alunos = self.usuario_repo.get_alunos()
                for aluno in alunos[:5]:
                    if not self.reserva_repo.existe_reserva(aluno.id, monitoria.id):
                        self.notificacao_repo.criar_notificacao(
                            usuario_id=aluno.id,
                            titulo="Poucas vagas disponíveis",
                            mensagem=f"A monitoria '{monitoria.titulo}' tem apenas {monitoria.vagas_disponiveis} vagas restantes!",
                            tipo="vagas_limitadas"
                        )
    
    def _notificar_avaliacoes_pendentes(self):
        ontem = datetime.now() - timedelta(days=1)
        monitorias_finalizadas = self.monitoria_repo.model.query.filter(
            self.monitoria_repo.model.status == 'finalizada',
            self.monitoria_repo.model.data_hora >= ontem
        ).all()
        
        for monitoria in monitorias_finalizadas:
            presencas = monitoria.presencas
            for presenca in presencas:
                avaliacoes = [a for a in monitoria.avaliacoes if a.aluno_id == presenca.aluno_id]
                if not avaliacoes:
                    self.notificacao_repo.criar_notificacao(
                        usuario_id=presenca.aluno_id,
                        titulo="Avalie a monitoria",
                        mensagem=f"Que tal avaliar a monitoria '{monitoria.titulo}' que você participou?",
                        tipo="avaliacao_pendente"
                    )
    
    def notificar_nova_monitoria(self, monitoria_id):
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        if monitoria:
            alunos = self.usuario_repo.get_alunos()
            for aluno in alunos[:10]:
                self.notificacao_repo.criar_notificacao(
                    usuario_id=aluno.id,
                    titulo="Nova monitoria disponível",
                    mensagem=f"Nova monitoria '{monitoria.titulo}' foi criada por {monitoria.monitor.nome}",
                    tipo="nova_monitoria"
                )
    
    def notificar_reserva_confirmada(self, aluno_id, monitoria_id):
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        if monitoria:
            self.notificacao_repo.criar_notificacao(
                usuario_id=aluno_id,
                titulo="Reserva confirmada",
                mensagem=f"Sua reserva para '{monitoria.titulo}' foi confirmada para {monitoria.data_hora.strftime('%d/%m/%Y às %H:%M')}",
                tipo="reserva_confirmada"
            )
    
    def notificar_monitoria_iniciada(self, monitoria_id):
        monitoria = self.monitoria_repo.get_by_id(monitoria_id)
        if monitoria:
            reservas = self.reserva_repo.find_by(monitoria_id=monitoria_id, status='confirmada')
            for reserva in reservas:
                self.notificacao_repo.criar_notificacao(
                    usuario_id=reserva.aluno_id,
                    titulo="Monitoria iniciada",
                    mensagem=f"A monitoria '{monitoria.titulo}' foi iniciada. Código de presença disponível!",
                    tipo="monitoria_iniciada"
                )