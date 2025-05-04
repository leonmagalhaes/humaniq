from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app.models import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para autenticação de usuários
    ---
    Parâmetros:
      - email: Email do usuário
      - senha: Senha do usuário
    Retorna:
      - Token de acesso JWT
      - Token de refresh JWT
      - Informações do usuário
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'message': 'Dados incompletos. Email e senha são obrigatórios.'}), 400
    
    usuario = Usuario.query.filter_by(email=data.get('email')).first()
    
    if not usuario or not usuario.verificar_senha(data.get('senha')):
        return jsonify({'message': 'Credenciais inválidas. Verifique seu email e senha.'}), 401
    
    # Criar tokens JWT
    access_token = create_access_token(identity=str(usuario.id))
    refresh_token = create_refresh_token(identity=str(usuario.id))
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'usuario': usuario.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para renovar o token de acesso usando o token de refresh
    ---
    Requer:
      - Token de refresh JWT válido
    Retorna:
      - Novo token de acesso JWT
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'message': 'Token renovado com sucesso',
        'access_token': new_access_token
    }), 200

@auth_bp.route('/register', methods=['POST'])
def registro():
    """
    Endpoint para registro de novos usuários
    ---
    Parâmetros:
      - nome: Nome completo do usuário
      - email: Email do usuário
      - senha: Senha do usuário
    Retorna:
      - Token de acesso JWT
      - Token de refresh JWT
      - Informações do usuário criado
    """
    data = request.get_json()
    
    if not data or not data.get('nome') or not data.get('email') or not data.get('senha'):
        return jsonify({'message': 'Dados incompletos. Nome, email e senha são obrigatórios.'}), 400
    
    # Verificar se o email já está em uso
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email já cadastrado. Utilize outro email.'}), 409
    
    # Criar novo usuário
    novo_usuario = Usuario(
        nome=data.get('nome'),
        email=data.get('email'),
        senha=data.get('senha')
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    # Criar tokens JWT
    access_token = create_access_token(identity=str(novo_usuario.id))
    refresh_token = create_refresh_token(identity=str(novo_usuario.id))
    
    return jsonify({
        'message': 'Usuário registrado com sucesso',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'usuario': novo_usuario.to_dict()
    }), 201

@auth_bp.route('/verificar', methods=['GET'])
@jwt_required()
def verificar_token():
    """
    Endpoint para verificar se o token JWT é válido
    ---
    Requer:
      - Token de acesso JWT válido
    Retorna:
      - Status da verificação
    """
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'message': 'Token válido',
        'usuario': usuario.to_dict()
    }), 200
