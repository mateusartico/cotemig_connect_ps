from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.repositories.usuario_repository import UsuarioRepository
from app.models.entities import Usuario
from app.core.factory import EntityFactoryProvider
from app.core.strategy import ValidationContext, EmailValidationStrategy, PasswordValidationStrategy
from app.core.decorator import audit_log, validate_input
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
usuario_repo = UsuarioRepository()

def detectar_tipo_usuario(email):
    """Detecta automaticamente o tipo de usuário baseado no email"""
    import re
    
    # Padrão para aluno: 8 dígitos + @aluno.cotemig.com.br
    aluno_pattern = r'^\d{8}@aluno\.cotemig\.com\.br$'
    # Padrão para monitor: qualquer coisa + @cotemig.com.br (exceto aluno)
    monitor_pattern = r'^[a-zA-Z][a-zA-Z0-9._-]*@cotemig\.com\.br$'
    
    if re.match(aluno_pattern, email):
        return 'aluno'
    elif re.match(monitor_pattern, email):
        return 'monitor'
    else:
        return None

def validar_email(email):
    """Valida se o email está no formato correto"""
    tipo = detectar_tipo_usuario(email)
    return tipo is not None

@auth_bp.route('/login', methods=['GET', 'POST'])
@audit_log('Login de usuário')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = usuario_repo.get_by_email(email)
        
        if not usuario or not usuario.check_password(senha):
            flash('Email ou senha inválidos', 'error')
        elif not usuario.ativo:
            flash('Usuário inativo', 'error')
        else:
            session['user_id'] = usuario.id
            session['user_tipo'] = usuario.tipo
            session['user_nome'] = usuario.nome
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
@audit_log('Cadastro de usuário')
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Detectar tipo automaticamente
        tipo = detectar_tipo_usuario(email)
        
        if not tipo:
            flash('Email inválido. Use o formato institucional correto.', 'error')
        elif usuario_repo.get_by_email(email):
            flash('Email já cadastrado', 'error')
        elif len(senha) < 8:
            flash('Senha deve ter pelo menos 8 caracteres', 'error')
        else:
            # Usar Factory para criar usuário
            usuario = EntityFactoryProvider.create_entity('usuario', 
                nome=nome, 
                email=email, 
                tipo=tipo,
                senha=senha
            )
            codigo = usuario.gerar_codigo_verificacao()
            usuario_repo.save(usuario)
            
            flash(f'Cadastro realizado! Código de verificação: {codigo}', 'success')
            return redirect(url_for('auth.verificar'))
    
    return render_template('auth/cadastro.html')

@auth_bp.route('/verificar', methods=['GET', 'POST'])
def verificar():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        usuario = usuario_repo.get_by_codigo_verificacao(codigo)
        
        if not usuario:
            flash('Código inválido', 'error')
        else:
            usuario.verificado = True
            usuario.codigo_verificacao = None
            usuario_repo.save(usuario)
            
            session['user_id'] = usuario.id
            session['user_tipo'] = usuario.tipo
            session['user_nome'] = usuario.nome
            flash('Conta verificada com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
    
    return render_template('auth/verificar.html')

@auth_bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = usuario_repo.get_by_email(email)
        
        if usuario:
            token = usuario.gerar_reset_token()
            usuario_repo.save(usuario)
            flash(f'Token de recuperação: {token}', 'success')
            return redirect(url_for('auth.redefinir_senha'))
        else:
            flash('Email não encontrado', 'error')
    
    return render_template('auth/esqueci_senha.html')

@auth_bp.route('/redefinir-senha', methods=['GET', 'POST'])
def redefinir_senha():
    if request.method == 'POST':
        token = request.form.get('token')
        nova_senha = request.form.get('nova_senha')
        
        usuario = usuario_repo.get_by_reset_token(token)
        
        if not usuario:
            flash('Token inválido', 'error')
        elif len(nova_senha) < 8:
            flash('Senha deve ter pelo menos 8 caracteres', 'error')
        else:
            usuario.set_password(nova_senha)
            usuario.reset_token = None
            usuario_repo.save(usuario)
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/redefinir_senha.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))