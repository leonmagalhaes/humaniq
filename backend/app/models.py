from datetime import datetime, timedelta, timezone
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    avaliacoes = db.relationship('Avaliacao', backref='usuario', lazy=True)
    resultados = db.relationship('Resultado', backref='usuario', lazy=True)
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'data_cadastro': self.data_cadastro.isoformat()
        }

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    pontuacao = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)
    
    # Armazenar as respostas do teste como JSON
    respostas = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'data': self.data.isoformat(),
            'pontuacao': self.pontuacao,
            'feedback': self.feedback,
            'respostas': self.respostas
        }

class Desafio(db.Model):
    __tablename__ = 'desafios'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='ativo')  # ativo, inativo
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    prazo = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=7))

    
    # Perguntas do quiz relacionadas ao desafio
    perguntas = db.Column(db.JSON)
    
    # Detalhes do desafio prático
    desafio_pratico = db.Column(db.Text)
    
    # Relacionamentos
    resultados = db.relationship('Resultado', backref='desafio', lazy=True)
    
    def to_dict(self):
        return {
            'desafio_id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'video_url': self.video_url,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat(),
            'prazo': self.prazo.isoformat() if self.prazo else None,
            'perguntas': self.perguntas,
            'desafio_pratico': self.desafio_pratico
        }

class Resultado(db.Model):
    __tablename__ = 'resultados'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    desafio_id = db.Column(db.Integer, db.ForeignKey('desafios.id'), nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, concluído, falhou
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_conclusao = db.Column(db.DateTime)
    
    # Respostas do quiz e do desafio prático
    respostas_quiz = db.Column(db.JSON)
    resposta_pratica = db.Column(db.Text)
    
    # Pontuação obtida
    pontuacao = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'desafio_id': self.desafio_id,
            'status': self.status,
            'data_inicio': self.data_inicio.isoformat(),
            'data_conclusao': self.data_conclusao.isoformat() if self.data_conclusao else None,
            'pontuacao': self.pontuacao,
            'respostas_quiz': self.respostas_quiz,
            'resposta_pratica': self.resposta_pratica
        }

# Modelo para as perguntas do teste inicial
class PerguntaTeste(db.Model):
    __tablename__ = 'perguntas_teste'
    
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50))  # Categoria da pergunta (opcional)
    ordem = db.Column(db.Integer)  # Ordem de exibição
    
    def to_dict(self):
        return {
            'id': self.id,
            'texto': self.texto,
            'categoria': self.categoria,
            'ordem': self.ordem
        }
