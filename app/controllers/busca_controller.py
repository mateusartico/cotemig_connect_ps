from flask import Blueprint, render_template, request, session, jsonify
from app.repositories.monitoria_repository import MonitoriaRepository, DisciplinaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.historico_busca_repository import HistoricoBuscaRepository
from app.models.entities import HistoricoBusca
from app.core.strategy import SearchContext, FullTextSearchStrategy, TitleSearchStrategy
from app.core.decorator import login_required, log_execution_time, cache_result
from app.core.database_singleton import db
import json

busca_bp = Blueprint('busca', __name__, url_prefix='/busca')
monitoria_repo = MonitoriaRepository()
disciplina_repo = DisciplinaRepository()
usuario_repo = UsuarioRepository()
historico_repo = HistoricoBuscaRepository()



@busca_bp.route('/')
def index():
    return render_template('busca/index.html')

@busca_bp.route('/pesquisar')
@log_execution_time
@cache_result(timeout=60)
def pesquisar():
    termo = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '')
    avaliacao_min = request.args.get('avaliacao', type=int)
    
    if 'user_id' in session and termo:
        filtros = {
            'categoria': categoria,
            'avaliacao_min': avaliacao_min
        }
        historico_repo.create(
            usuario_id=session['user_id'],
            termo_busca=termo,
            filtros=json.dumps(filtros)
        )
    
    monitorias = monitoria_repo.buscar(termo, categoria, avaliacao_min)
    
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
    historico = historico_repo.get_by_usuario(session['user_id'], limit=20)
    return render_template('busca/historico.html', historico=historico)

@busca_bp.route('/comparar')
def comparar():
    ids = request.args.getlist('ids', type=int)
    if len(ids) < 2:
        return render_template('busca/comparar.html', error="Selecione pelo menos 2 monitorias")
    
    monitorias = [monitoria_repo.get_by_id(id) for id in ids]
    monitorias = [m for m in monitorias if m]
    
    return render_template('busca/comparar.html', monitorias=monitorias)