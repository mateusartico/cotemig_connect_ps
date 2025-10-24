from flask import Blueprint, request, jsonify, session
from app.repositories.monitoria_repository import MonitoriaRepository
from app.core.decorator import login_required
from app.core.database_singleton import db

favorito_bp = Blueprint('favorito', __name__, url_prefix='/favoritos')
monitoria_repo = MonitoriaRepository()

@favorito_bp.route('/toggle/<int:monitoria_id>', methods=['POST'])
@login_required
def toggle_favorito(monitoria_id):
    """Adiciona ou remove monitoria dos favoritos"""
    user_id = session.get('user_id')
    
    # Simulação - em produção usaria tabela de favoritos
    favoritos_session = session.get('favoritos', [])
    
    if monitoria_id in favoritos_session:
        favoritos_session.remove(monitoria_id)
        action = 'removed'
    else:
        favoritos_session.append(monitoria_id)
        action = 'added'
    
    session['favoritos'] = favoritos_session
    
    return jsonify({
        'success': True,
        'action': action,
        'total': len(favoritos_session)
    })

@favorito_bp.route('/listar')
@login_required
def listar_favoritos():
    """Lista monitorias favoritas do usuário"""
    favoritos_ids = session.get('favoritos', [])
    monitorias = []
    
    for monitoria_id in favoritos_ids:
        monitoria = monitoria_repo.get_by_id(monitoria_id)
        if monitoria:
            monitorias.append({
                'id': monitoria.id,
                'titulo': monitoria.titulo,
                'data_hora': monitoria.data_hora.isoformat(),
                'vagas_disponiveis': monitoria.vagas_disponiveis
            })
    
    return jsonify(monitorias)