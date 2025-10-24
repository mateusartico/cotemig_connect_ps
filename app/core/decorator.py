"""
Padrão Decorator para funcionalidades adicionais
"""
from functools import wraps
from flask import session, redirect, url_for, flash
from datetime import datetime
import time

def login_required(f):
    """Decorator para verificar se usuário está logado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator para verificar se usuário é admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado', 'error')
            return redirect(url_for('auth.login'))
        
        if session.get('user_tipo') != 'admin':
            flash('Acesso negado. Apenas administradores', 'error')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def monitor_required(f):
    """Decorator para verificar se usuário é monitor"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado', 'error')
            return redirect(url_for('auth.login'))
        
        if session.get('user_tipo') not in ['monitor', 'admin']:
            flash('Acesso negado. Apenas monitores', 'error')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def log_execution_time(f):
    """Decorator para logar tempo de execução"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[PERFORMANCE] {f.__name__} executado em {execution_time:.4f}s")
        return result
    return decorated_function

def audit_log(action):
    """Decorator para auditoria de ações"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id', 'Anônimo')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[AUDIT] {timestamp} - Usuário {user_id} executou: {action}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def cache_result(timeout=300):
    """Decorator para cache de resultados (simulado)"""
    def decorator(f):
        cache = {}
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Cria chave do cache baseada nos argumentos
            cache_key = f"{f.__name__}_{str(args)}_{str(sorted(kwargs.items()))}"
            current_time = time.time()
            
            # Verifica se existe no cache e não expirou
            if cache_key in cache:
                cached_time, cached_result = cache[cache_key]
                if current_time - cached_time < timeout:
                    print(f"[CACHE] Cache hit para {f.__name__}")
                    return cached_result
            
            # Executa função e armazena no cache
            result = f(*args, **kwargs)
            cache[cache_key] = (current_time, result)
            print(f"[CACHE] Cache miss para {f.__name__}")
            return result
        
        return decorated_function
    return decorator

def validate_input(validation_rules):
    """Decorator para validação de entrada"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if request.method == 'POST':
                errors = []
                
                for field, rules in validation_rules.items():
                    value = request.form.get(field, '')
                    
                    if 'required' in rules and not value:
                        errors.append(f"{field} é obrigatório")
                    
                    if 'min_length' in rules and len(value) < rules['min_length']:
                        errors.append(f"{field} deve ter pelo menos {rules['min_length']} caracteres")
                    
                    if 'max_length' in rules and len(value) > rules['max_length']:
                        errors.append(f"{field} deve ter no máximo {rules['max_length']} caracteres")
                
                if errors:
                    for error in errors:
                        flash(error, 'error')
                    return redirect(request.url)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator