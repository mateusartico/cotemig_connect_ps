from flask import Blueprint, render_template, session, redirect, url_for
from app.repositories.monitoria_repository import MonitoriaRepository, ReservaRepository
from app.core.decorator import login_required

main_bp = Blueprint('main', __name__)
monitoria_repo = MonitoriaRepository()
reserva_repo = ReservaRepository()

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_tipo = session.get('user_tipo')
    
    if user_tipo == 'monitor':
        monitorias = monitoria_repo.get_by_monitor(session['user_id'])
        return render_template('dashboard.html', monitorias=monitorias)
    
    elif user_tipo == 'aluno':
        proximas_monitorias = monitoria_repo.get_proximas()
        minhas_reservas = reserva_repo.get_by_aluno(session['user_id'])
        return render_template('dashboard.html', 
                             proximas_monitorias=proximas_monitorias,
                             minhas_reservas=minhas_reservas)
    
    return render_template('dashboard.html')