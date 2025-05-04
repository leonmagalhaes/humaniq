from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
from flask_cors import CORS

# Inicialização das extensões
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicialização das extensões com a aplicação
    db.init_app(app)
    jwt.init_app(app)
    # Configuração mais específica do CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Registro dos blueprints
    from app.resources.auth import auth_bp
    from app.resources.user import user_bp
    from app.resources.assessment import assessment_bp
    from app.resources.desafio import desafio_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(assessment_bp, url_prefix='/api/assessments')
    app.register_blueprint(desafio_bp, url_prefix='/api/desafios')

    # Rota de teste para verificar se a API está funcionando
    @app.route('/api/ping', methods=['GET'])
    def ping():
        return {'message': 'API HUMANIQ está online!'}, 200

    # Criação das tabelas do banco de dados
    with app.app_context():
        db.create_all()

    return app