from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.repositories.monitoria_repository import MonitoriaRepository, PresencaRepository
from app.models.entities import Avaliacao
from app import db

avaliacao_bp = Blueprint('avaliacao', __name__, url_prefix='/avaliacao')
monitoria_repo = MonitoriaRepository()
presenca_repo = PresencaRepository()

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@avaliacao_bp.route('/criar/<int:monitoria_id>', methods=['GET', 'POST'])
@login_required
def criar(monitoria_id):
    if session.get('user_tipo') != 'aluno':
        flash('Apenas alunos podem avaliar', 'error')
        return redirect(url_for('main.dashboard'))
    
    monitoria = monitoria_repo.get_by_id(monitoria_id)
    if not monitoria:
        flash('Monitoria não encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Verificar se aluno participou
    if not presenca_repo.existe_presenca(session['user_id'], monitoria_id):
        flash('Você precisa ter participado da monitoria para avaliar', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Verificar se já avaliou
    avaliacao_existente = db.session.query(Avaliacao).filter_by(
        aluno_id=session['user_id'],
        monitoria_id=monitoria_id
    ).first()
    
    if request.method == 'POST':
        nota = int(request.form.get('nota'))
        comentario = request.form.get('comentario', '').strip()
        
        if avaliacao_existente:
            avaliacao_existente.nota = nota
            avaliacao_existente.comentario = comentario
        else:
            avaliacao = Avaliacao(
                aluno_id=session['user_id'],
                monitoria_id=monitoria_id,
                nota=nota,
                comentario=comentario
            )
            db.session.add(avaliacao)
        
        db.session.commit()
        flash('Avaliação salva com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('avaliacao/criar.html', 
                         monitoria=monitoria, 
                         avaliacao=avaliacao_existente)

@avaliacao_bp.route('/listar/<int:monitoria_id>')
def listar(monitoria_id):
    monitoria = monitoria_repo.get_by_id(monitoria_id)
    if not monitoria:
        flash('Monitoria não encontrada', 'error')
        return redirect(url_for('main.dashboard'))
    
    avaliacoes = db.session.query(Avaliacao).filter_by(
        monitoria_id=monitoria_id
    ).order_by(Avaliacao.created_at.desc()).all()
    
    return render_template('avaliacao/listar.html', 
                         monitoria=monitoria, 
                         avaliacoes=avaliacoes)