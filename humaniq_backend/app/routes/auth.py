from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.email_utils import send_welcome_email
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validação dos dados
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    # Validar formato de e-mail
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return jsonify({'message': 'Formato de e-mail inválido'}), 400
    
    # Verificar se o e-mail já está em uso
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'E-mail já cadastrado'}), 409
    
    # Validar senha (mínimo 8 caracteres)
    if len(data['password']) < 8:
        return jsonify({'message': 'A senha deve ter pelo menos 8 caracteres'}), 400
    
    # Criar novo usuário
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Enviar e-mail de boas-vindas
    send_welcome_email(user)
    
    # Gerar tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Usuário registrado com sucesso',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'E-mail ou senha incorretos'}), 401
    
    # Atualizar data do último login
    user.last_login = db.func.now()
    db.session.commit()
    
    # Gerar tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': access_token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if not user.check_password(data['current_password']):
        return jsonify({'message': 'Senha atual incorreta'}), 401
    
    if len(data['new_password']) < 8:
        return jsonify({'message': 'A nova senha deve ter pelo menos 8 caracteres'}), 400
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Senha alterada com sucesso'}), 200