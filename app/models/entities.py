from app.core.database_singleton import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    verificado = db.Column(db.Boolean, default=False)
    codigo_verificacao = db.Column(db.String(6))
    reset_token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    monitorias_criadas = db.relationship('Monitoria', foreign_keys='Monitoria.monitor_id', backref='monitor')
    reservas = db.relationship('Reserva', backref='aluno')
    presencas = db.relationship('Presenca', backref='aluno')
    avaliacoes = db.relationship('Avaliacao', backref='aluno')
    historico_buscas = db.relationship('HistoricoBusca', backref='usuario')
    
    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)
    
    def gerar_codigo_verificacao(self):
        # Gera código de 6 dígitos
        self.codigo_verificacao = str(secrets.randbelow(900000) + 100000)
        return self.codigo_verificacao
    
    def gerar_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        return self.reset_token

class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    categoria = db.Column(db.String(50), default='Geral')
    ativa = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    monitorias = db.relationship('Monitoria', backref='disciplina')

class Monitoria(db.Model):
    __tablename__ = 'monitorias'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Integer, default=60)
    vagas_total = db.Column(db.Integer, default=10)
    vagas_ocupadas = db.Column(db.Integer, default=0)
    local = db.Column(db.String(100))
    codigo_presenca = db.Column(db.String(6))
    status = db.Column(db.String(20), default='agendada')
    tags = db.Column(db.String(200))
    
    # Chaves estrangeiras
    monitor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    reservas = db.relationship('Reserva', backref='monitoria', cascade='all, delete-orphan')
    presencas = db.relationship('Presenca', backref='monitoria', cascade='all, delete-orphan')
    avaliacoes = db.relationship('Avaliacao', backref='monitoria', cascade='all, delete-orphan')
    
    def gerar_codigo_presenca(self):
        # Gera código de 6 dígitos para presença
        self.codigo_presenca = str(secrets.randbelow(900000) + 100000)
        return self.codigo_presenca
    
    @property
    def vagas_disponiveis(self):
        return self.vagas_total - self.vagas_ocupadas
    
    @property
    def media_avaliacoes(self):
        if not self.avaliacoes:
            return 0
        return sum(a.nota for a in self.avaliacoes) / len(self.avaliacoes)

class Reserva(db.Model):
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    monitoria_id = db.Column(db.Integer, db.ForeignKey('monitorias.id'), nullable=False)
    status = db.Column(db.String(20), default='confirmada')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('aluno_id', 'monitoria_id'),)

class Presenca(db.Model):
    __tablename__ = 'presencas'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    monitoria_id = db.Column(db.Integer, db.ForeignKey('monitorias.id'), nullable=False)
    presente = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('aluno_id', 'monitoria_id'),)

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    monitoria_id = db.Column(db.Integer, db.ForeignKey('monitorias.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('aluno_id', 'monitoria_id'),)

class HistoricoBusca(db.Model):
    __tablename__ = 'historico_buscas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    termo_busca = db.Column(db.String(200), nullable=False)
    filtros = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Suporte(db.Model):
    __tablename__ = 'suporte'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    assunto = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='aberto')
    resposta = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref='tickets_suporte')

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref='notificacoes')