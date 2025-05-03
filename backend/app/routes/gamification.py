from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Badge, user_badges
from sqlalchemy import desc

gamification_bp = Blueprint('gamification', __name__)

@gamification_bp.route('/badges', methods=['GET'])
@jwt_required()
def get_badges():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Buscar todas as badges disponíveis
    all_badges = Badge.query.all()
    
    # Preparar resposta com status de conquista
    response = []
    for badge in all_badges:
        badge_data = badge.to_dict()
        badge_data['earned'] = badge in user.badges
        response.append(badge_data)
    
    return jsonify(response), 200

@gamification_bp.route('/badges/<int:badge_id>', methods=['GET'])
@jwt_required()
def get_badge(badge_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    badge = Badge.query.get(badge_id)
    
    if not badge:
        return jsonify({'message': 'Badge não encontrada'}), 404
    
    badge_data = badge.to_dict()
    badge_data['earned'] = badge in user.badges
    
    return jsonify(badge_data), 200

@gamification_bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    # Buscar os 10 usuários com mais pontos
    top_users = User.query.order_by(desc(User.points)).limit(10).all()
    
    # Preparar resposta
    leaderboard = []
    for i, user in enumerate(top_users):
        leaderboard.append({
            'position': i + 1,
            'name': user.name,
            'points': user.points,
            'level': user.level,
            'badges_count': len(user.badges)
        })
    
    return jsonify(leaderboard), 200

# Rota administrativa para criar novas badges (em produção, deve ser protegida)
@gamification_bp.route('/badges', methods=['POST'])
@jwt_required()
def create_badge():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Verificar se o usuário tem permissão (simplificado para desenvolvimento)
    # Em produção, deve verificar se o usuário é admin
    
    data = request.get_json()
    
    # Validar dados
    required_fields = ['name', 'description', 'image_url', 'requirement']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Campo obrigatório ausente: {field}'}), 400
    
    # Verificar se já existe uma badge com o mesmo nome
    existing_badge = Badge.query.filter_by(name=data['name']).first()
    if existing_badge:
        return jsonify({'message': 'Já existe uma badge com este nome'}), 409
    
    # Criar nova badge
    badge = Badge(
        name=data['name'],
        description=data['description'],
        image_url=data['image_url'],
        requirement=data['requirement']
    )
    
    db.session.add(badge)
    db.session.commit()
    
    return jsonify({
        'message': 'Badge criada com sucesso',
        'badge': badge.to_dict()
    }), 201

# Rota para atribuir uma badge a um usuário (em produção, deve ser protegida ou automatizada)
@gamification_bp.route('/badges/<int:badge_id>/award', methods=['POST'])
@jwt_required()
def award_badge(badge_id):
    data = request.get_json() or {}
    user_id = data.get('user_id') or get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    badge = Badge.query.get(badge_id)
    if not badge:
        return jsonify({'message': 'Badge não encontrada'}), 404
    
    # Verificar se o usuário já possui esta badge
    if badge in user.badges:
        return jsonify({'message': 'Usuário já possui esta badge'}), 400
    
    # Atribuir badge ao usuário
    user.badges.append(badge)
    
    # Adicionar pontos ao usuário
    user.add_points(30)  # 30 pontos por badge conquistada
    
    db.session.commit()
    
    return jsonify({
        'message': 'Badge atribuída com sucesso',
        'badge': badge.to_dict(),
        'user': user.to_dict()
    }), 200