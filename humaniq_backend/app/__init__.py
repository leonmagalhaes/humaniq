from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from config import config

# Inicialização das extensões
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
scheduler = BackgroundScheduler()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicialização das extensões com a aplicação
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Importação e registro dos blueprints
    from app.routes.auth import auth_bp
    from app.routes.skills import skills_bp
    from app.routes.challenges import challenges_bp
    from app.routes.profile import profile_bp
    from app.routes.gamification import gamification_bp
    from app.routes.forum import forum_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(skills_bp, url_prefix='/api/skills')
    app.register_blueprint(challenges_bp, url_prefix='/api/challenges')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(gamification_bp, url_prefix='/api/gamification')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    
    # Inicialização do agendador de tarefas
    with app.app_context():
        from app.tasks import init_scheduler
        init_scheduler(scheduler)
        scheduler.start()
    
    return app