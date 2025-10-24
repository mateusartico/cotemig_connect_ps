from flask import Blueprint, render_template, request, jsonify, session
from app.core.decorator import login_required
from app.repositories.notificacao_repository import NotificacaoRepository
from app.services.notificacao_service import NotificacaoService

notificacao_bp = Blueprint('notificacao', __name__, url_prefix='/api/notificacoes')
notificacao_repo = NotificacaoRepository()
notificacao_service = NotificacaoService()

@notificacao_bp.route('/recentes')
@login_required
def recentes():
    notificacoes = notificacao_repo.get_by_usuario(session['user_id'], limit=10)
    
    notifications = []
    for notif in notificacoes:
        notifications.append({
            'id': notif.id,
            'titulo': notif.titulo,
            'mensagem': notif.mensagem,
            'timestamp': notif.created_at.isoformat(),
            'lida': notif.lida,
            'tipo': notif.tipo
        })
    
    return jsonify(notifications)

@notificacao_bp.route('/marcar-lida/<int:notificacao_id>', methods=['POST'])
@login_required
def marcar_lida(notificacao_id):
    notificacao = notificacao_repo.marcar_como_lida(notificacao_id, session['user_id'])
    if notificacao:
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@notificacao_bp.route('/marcar-todas-lidas', methods=['POST'])
@login_required
def marcar_todas_lidas():
    count = notificacao_repo.marcar_todas_como_lidas(session['user_id'])
    return jsonify({'success': True, 'count': count})

@notificacao_bp.route('/gerar-automaticas', methods=['POST'])
@login_required
def gerar_automaticas():
    if session.get('user_tipo') == 'admin':
        notificacao_service.gerar_notificacoes_automaticas()
        return jsonify({'success': True, 'message': 'Notificações geradas'})
    return jsonify({'success': False}), 403