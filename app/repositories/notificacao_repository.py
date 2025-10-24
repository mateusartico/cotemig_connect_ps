from app.repositories.base_repository import BaseRepository
from app.models.entities import Notificacao
from datetime import datetime, timedelta

class NotificacaoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Notificacao)
    
    def get_by_usuario(self, usuario_id, limit=10):
        return self.model.query.filter_by(usuario_id=usuario_id)\
                   .order_by(self.model.created_at.desc())\
                   .limit(limit).all()
    
    def get_nao_lidas(self, usuario_id):
        return self.model.query.filter_by(usuario_id=usuario_id, lida=False)\
                   .order_by(self.model.created_at.desc()).all()
    
    def marcar_como_lida(self, notificacao_id, usuario_id):
        notificacao = self.model.query.filter_by(id=notificacao_id, usuario_id=usuario_id).first()
        if notificacao:
            notificacao.lida = True
            self.save(notificacao)
        return notificacao
    
    def marcar_todas_como_lidas(self, usuario_id):
        notificacoes = self.model.query.filter_by(usuario_id=usuario_id, lida=False).all()
        for notificacao in notificacoes:
            notificacao.lida = True
            self.save(notificacao)
        return len(notificacoes)
    
    def criar_notificacao(self, usuario_id, titulo, mensagem, tipo):
        return self.create(
            usuario_id=usuario_id,
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo
        )