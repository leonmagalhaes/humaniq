from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Tabela de associação entre usuários e badges
user_badges = db.Table('user_badges',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badges.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    
    # Relacionamentos
    assessments = db.relationship('SkillAssessment', backref='user', lazy='dynamic')
    challenge_results = db.relationship('ChallengeResult', backref='user', lazy='dynamic')
    forum_posts = db.relationship('ForumPost', backref='author', lazy='dynamic')
    badges = db.relationship('Badge', secondary=user_badges, backref=db.backref('users', lazy='dynamic'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_points(self, points):
        self.points += points
        # Verificar se o usuário subiu de nível
        new_level = (self.points // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return True
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'points': self.points,
            'level': self.level,
            'badges': [badge.to_dict() for badge in self.badges]
        }

class SkillAssessment(db.Model):
    __tablename__ = 'skill_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    communication = db.Column(db.Integer, nullable=False)  # Escala Likert 1-5
    active_listening = db.Column(db.Integer, nullable=False)
    conflict_resolution = db.Column(db.Integer, nullable=False)
    teamwork = db.Column(db.Integer, nullable=False)
    critical_thinking = db.Column(db.Integer, nullable=False)
    time_management = db.Column(db.Integer, nullable=False)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'communication': self.communication,
            'active_listening': self.active_listening,
            'conflict_resolution': self.conflict_resolution,
            'teamwork': self.teamwork,
            'critical_thinking': self.critical_thinking,
            'time_management': self.time_management,
            'assessment_date': self.assessment_date.isoformat()
        }

class Challenge(db.Model):
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skill_type = db.Column(db.String(50), nullable=False)  # Tipo de soft skill
    challenge_type = db.Column(db.String(20), nullable=False)  # video, quiz, practice
    content = db.Column(db.Text, nullable=False)  # URL do vídeo ou conteúdo do quiz
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    results = db.relationship('ChallengeResult', backref='challenge', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'skill_type': self.skill_type,
            'challenge_type': self.challenge_type,
            'content': self.content,
            'points': self.points,
            'created_at': self.created_at.isoformat()
        }

class ChallengeResult(db.Model):
    __tablename__ = 'challenge_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, nullable=True)  # Para quizzes
    feedback = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'completed': self.completed,
            'score': self.score,
            'feedback': self.feedback,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Badge(db.Model):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    requirement = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'requirement': self.requirement
        }

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    comments = db.relationship('ForumComment', backref='post', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'author_name': self.author.name,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'comments_count': self.comments.count()
        }

class ForumComment(db.Model):
    __tablename__ = 'forum_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com o usuário
    author = db.relationship('User', backref='comments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author_name': self.author.name,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com o usuário
    user = db.relationship('User', backref='certificates')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'issue_date': self.issue_date.isoformat()
        }