from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.entities import Suporte
from app import db

suporte_bp = Blueprint('suporte', __name__, url_prefix='/suporte')

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@suporte_bp.route('/')
def index():
    return render_template('suporte/index.html')

@suporte_bp.route('/ticket', methods=['GET', 'POST'])
@login_required
def criar_ticket():
    if request.method == 'POST':
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')
        
        ticket = Suporte(
            usuario_id=session['user_id'],
            assunto=assunto,
            mensagem=mensagem
        )
        db.session.add(ticket)
        db.session.commit()
        
        flash('Ticket criado com sucesso! Nossa equipe entrará em contato.', 'success')
        return redirect(url_for('suporte.meus_tickets'))
    
    return render_template('suporte/criar_ticket.html')

@suporte_bp.route('/meus-tickets')
@login_required
def meus_tickets():
    tickets = db.session.query(Suporte).filter_by(
        usuario_id=session['user_id']
    ).order_by(Suporte.created_at.desc()).all()
    
    return render_template('suporte/meus_tickets.html', tickets=tickets)

@suporte_bp.route('/admin')
@login_required
def admin():
    if session.get('user_tipo') != 'admin':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    tickets = db.session.query(Suporte).order_by(Suporte.created_at.desc()).all()
    return render_template('suporte/admin.html', tickets=tickets)

@suporte_bp.route('/responder/<int:ticket_id>', methods=['POST'])
@login_required
def responder(ticket_id):
    if session.get('user_tipo') != 'admin':
        flash('Acesso negado', 'error')
        return redirect(url_for('main.dashboard'))
    
    ticket = db.session.query(Suporte).get(ticket_id)
    if not ticket:
        flash('Ticket não encontrado', 'error')
        return redirect(url_for('suporte.admin'))
    
    resposta = request.form.get('resposta')
    status = request.form.get('status')
    
    ticket.resposta = resposta
    ticket.status = status
    db.session.commit()
    
    flash('Resposta enviada com sucesso!', 'success')
    return redirect(url_for('suporte.admin'))