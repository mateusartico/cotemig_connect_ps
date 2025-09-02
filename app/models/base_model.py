from app.models.database import db
from datetime import datetime
import bcrypt
import re

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # aluno, professor, monitor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.matricula = self._extrair_matricula_usuario(email)
        self.senha = self._hash_password(senha)
        self.tipo_usuario = self._determinar_tipo_usuario(email)
    
    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.senha.encode('utf-8'))
    
    def _extrair_matricula_usuario(self, email):
        if email.endswith('@aluno.cotemig.com.br'):
            return email.split('@')[0]  # Matrícula do aluno
        elif email.endswith('@cotemig.com.br'):
            return email.split('@')[0]  # Usuário do funcionário
        return email.split('@')[0]
    
    def _determinar_tipo_usuario(self, email):
        if email.endswith('@aluno.cotemig.com.br'):
            return 'aluno'
        elif email.endswith('@cotemig.com.br'):
            if 'professor' in email.lower():
                return 'professor'
            elif 'monitor' in email.lower():
                return 'monitor'
        return 'aluno'
    
    @staticmethod
    def validar_email_aluno(email):
        if not email.endswith('@aluno.cotemig.com.br'):
            return False
        matricula = email.split('@')[0]
        return len(matricula) == 8 and matricula.isdigit()
    
    @staticmethod
    def validar_email_funcionario(email):
        return email.endswith('@cotemig.com.br') and ('professor' in email.lower() or 'monitor' in email.lower())
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'matricula': self.matricula,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario
        }