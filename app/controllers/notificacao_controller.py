from flask import Blueprint, jsonify, session
from app.repositories.usuario_repository import UsuarioRepository
from app.core.decorator import login_required
from datetime import datetime, timedelta

notificacao_bp = Blueprint('notificacao', __name__, url_prefix='/api/notificacoes')
usuario_repo = UsuarioRepository()

@notificacao_bp.route('/recentes')
@login_required
def get_notificacoes():
    """API para buscar notificações do usuário"""
    user_id = session.get('user_id')
    user_tipo = session.get('user_tipo')
    
    # Simulação de notificações baseadas no tipo de usuário
    notificacoes = []
    
    if user_tipo == 'aluno':
        notificacoes = [
            {
                'id': 1,
                'titulo': 'Nova monitoria disponível',
                'mensagem': 'Monitoria de Python Básico foi criada',
                'tipo': 'info',
                'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
                'lida': False
            },
            {
                'id': 2,
                'titulo': 'Lembrete de monitoria',
                'mensagem': 'Sua monitoria de SQL começa em 1 hora',
                'tipo': 'warning',
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                'lida': False
            }
        ]
    elif user_tipo == 'monitor':
        notificacoes = [
            {
                'id': 3,
                'titulo': 'Nova reserva',
                'mensagem': 'Um aluno se inscreveu na sua monitoria',
                'tipo': 'success',
                'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat(),
                'lida': False
            }
        ]
    
    return jsonify(notificacoes)

@notificacao_bp.route('/marcar-lida/<int:notificacao_id>', methods=['POST'])
@login_required
def marcar_como_lida(notificacao_id):
    """Marca notificação como lida"""
    # Simulação - em produção salvaria no banco
    return jsonify({'success': True})