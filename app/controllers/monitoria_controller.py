from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.repositories.monitoria_repository import MonitoriaRepository, ReservaRepository, PresencaRepository, DisciplinaRepository
from datetime import datetime

monitoria_bp = Blueprint('monitoria', __name__, url_prefix='/monitoria')
monitoria_repo = MonitoriaRepository()
reserva_repo = ReservaRepository()
presenca_repo = PresencaRepository()
disciplina_repo = DisciplinaRepository()

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@monitoria_bp.route('/criar', methods=['GET', 'POST'])
@login_required
def criar():
    if session.get('user_tipo') != 'monitor':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        data_str = request.form.get('data')
        hora_str = request.form.get('hora')
        duracao = int(request.form.get('duracao', 60))
        vagas_total = int(request.form.get('vagas_total', 10))
        local = request.form.get('local')
        disciplina_id = int(request.form.get('disciplina_id'))
        
        data_hora = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M")
        
        if data_hora <= datetime.now():
            flash('Data deve ser futura', 'error')
        else:
            monitoria_repo.create(
                titulo=titulo, descricao=descricao, data_hora=data_hora,
                duracao=duracao, vagas_total=vagas_total, local=local,
                monitor_id=session['user_id'], disciplina_id=disciplina_id
            )
            flash('Monitoria criada com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
    
    disciplinas = disciplina_repo.get_ativas()
    return render_template('monitoria/criar.html', disciplinas=disciplinas)

@monitoria_bp.route('/reservar/<int:monitoria_id>')
@login_required
def reservar(monitoria_id):
    if session.get('user_tipo') != 'aluno':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    monitoria = monitoria_repo.get_by_id(monitoria_id)
    
    if not monitoria:
        flash('Monitoria não encontrada', 'error')
    elif monitoria.vagas_disponiveis <= 0:
        flash('Não há vagas disponíveis', 'error')
    elif reserva_repo.existe_reserva(session['user_id'], monitoria_id):
        flash('Você já tem reserva nesta monitoria', 'error')
    else:
        reserva_repo.create(aluno_id=session['user_id'], monitoria_id=monitoria_id)
        monitoria.vagas_ocupadas += 1
        monitoria_repo.save(monitoria)
        flash('Reserva realizada com sucesso!', 'success')
    
    return redirect(url_for('main.dashboard'))

@monitoria_bp.route('/cancelar/<int:monitoria_id>')
@login_required
def cancelar_reserva(monitoria_id):
    if session.get('user_tipo') != 'aluno':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    reserva = reserva_repo.model.query.filter_by(
        aluno_id=session['user_id'], monitoria_id=monitoria_id, status='confirmada'
    ).first()
    
    if not reserva:
        flash('Reserva não encontrada', 'error')
    else:
        reserva.status = 'cancelada'
        reserva_repo.save(reserva)
        
        monitoria = monitoria_repo.get_by_id(monitoria_id)
        monitoria.vagas_ocupadas -= 1
        monitoria_repo.save(monitoria)
        flash('Reserva cancelada com sucesso!', 'success')
    
    return redirect(url_for('main.dashboard'))

@monitoria_bp.route('/iniciar/<int:monitoria_id>')
@login_required
def iniciar(monitoria_id):
    if session.get('user_tipo') != 'monitor':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    monitoria = monitoria_repo.get_by_id(monitoria_id)
    
    if not monitoria or monitoria.monitor_id != session['user_id']:
        flash('Monitoria não encontrada', 'error')
    elif monitoria.status != 'agendada':
        flash('Monitoria não pode ser iniciada', 'error')
    else:
        codigo = monitoria.gerar_codigo_presenca()
        monitoria.status = 'em_andamento'
        monitoria_repo.save(monitoria)
        flash(f'Monitoria iniciada! Código de presença: {codigo}', 'success')
    
    return redirect(url_for('main.dashboard'))

@monitoria_bp.route('/presenca', methods=['GET', 'POST'])
@login_required
def registrar_presenca():
    if session.get('user_tipo') != 'aluno':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        monitoria = monitoria_repo.get_by_codigo_presenca(codigo)
        
        if not monitoria:
            flash('Código inválido', 'error')
        elif not reserva_repo.existe_reserva(session['user_id'], monitoria.id):
            flash('Você não tem reserva nesta monitoria', 'error')
        elif presenca_repo.existe_presenca(session['user_id'], monitoria.id):
            flash('Presença já registrada', 'error')
        else:
            presenca_repo.create(aluno_id=session['user_id'], monitoria_id=monitoria.id)
            flash('Presença registrada com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
    
    return render_template('monitoria/presenca.html')