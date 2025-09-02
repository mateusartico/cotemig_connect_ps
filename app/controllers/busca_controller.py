from flask import Blueprint, render_template, request, session, jsonify
from app.repositories.monitoria_repository import MonitoriaRepository, DisciplinaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.models.entities import HistoricoBusca
from app import db
import json

busca_bp = Blueprint('busca', __name__, url_prefix='/busca')
monitoria_repo = MonitoriaRepository()
disciplina_repo = DisciplinaRepository()
usuario_repo = UsuarioRepository()

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login necessário'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@busca_bp.route('/')
def index():
    return render_template('busca/index.html')

@busca_bp.route('/pesquisar')
def pesquisar():
    termo = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '')
    avaliacao_min = request.args.get('avaliacao', type=int)
    
    # Salvar no histórico se usuário logado
    if 'user_id' in session and termo:
        filtros = {
            'categoria': categoria,
            'avaliacao_min': avaliacao_min
        }
        historico = HistoricoBusca(
            usuario_id=session['user_id'],
            termo_busca=termo,
            filtros=json.dumps(filtros)
        )
        db.session.add(historico)
        db.session.commit()
    
    # Buscar monitorias
    query = monitoria_repo.model.query.filter_by(status='agendada')
    
    if termo:
        query = query.filter(
            monitoria_repo.model.titulo.contains(termo) |
            monitoria_repo.model.descricao.contains(termo) |
            monitoria_repo.model.tags.contains(termo)
        )
    
    if categoria:
        query = query.join(monitoria_repo.model.disciplina).filter_by(categoria=categoria)
    
    monitorias = query.all()
    
    # Filtrar por avaliação se especificado
    if avaliacao_min:
        monitorias = [m for m in monitorias if m.media_avaliacoes >= avaliacao_min]
    
    disciplinas = disciplina_repo.get_ativas()
    categorias = list(set(d.categoria for d in disciplinas))
    
    return render_template('busca/resultados.html', 
                         monitorias=monitorias, 
                         termo=termo,
                         categorias=categorias,
                         categoria_selecionada=categoria,
                         avaliacao_selecionada=avaliacao_min)

@busca_bp.route('/historico')
@login_required
def historico():
    historico = db.session.query(HistoricoBusca).filter_by(
        usuario_id=session['user_id']
    ).order_by(HistoricoBusca.created_at.desc()).limit(20).all()
    
    return render_template('busca/historico.html', historico=historico)

@busca_bp.route('/comparar')
def comparar():
    ids = request.args.getlist('ids', type=int)
    if len(ids) < 2:
        return render_template('busca/comparar.html', error="Selecione pelo menos 2 monitorias")
    
    monitorias = [monitoria_repo.get_by_id(id) for id in ids]
    monitorias = [m for m in monitorias if m]  # Remove None
    
    return render_template('busca/comparar.html', monitorias=monitorias)