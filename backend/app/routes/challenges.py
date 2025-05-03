from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Challenge, ChallengeResult
from datetime import datetime

challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/', methods=['GET'])
@jwt_required()
def get_challenges():
    current_user_id = get_jwt_identity()
    
    # Parâmetros de filtro opcionais
    skill_type = request.args.get('skill_type')
    challenge_type = request.args.get('challenge_type')
    
    # Construir a query base
    query = Challenge.query
    
    # Aplicar filtros se fornecidos
    if skill_type:
        query = query.filter_by(skill_type=skill_type)
    if challenge_type:
        query = query.filter_by(challenge_type=challenge_type)
    
    # Ordenar por data de criação (mais recentes primeiro)
    challenges = query.order_by(Challenge.created_at.desc()).all()
    
    # Buscar resultados do usuário para esses desafios
    challenge_ids = [c.id for c in challenges]
    results = ChallengeResult.query.filter(
        ChallengeResult.user_id == current_user_id,
        ChallengeResult.challenge_id.in_(challenge_ids)
    ).all()
    
    # Mapear resultados por challenge_id
    results_map = {r.challenge_id: r for r in results}
    
    # Preparar resposta com desafios e status de conclusão
    response = []
    for challenge in challenges:
        challenge_data = challenge.to_dict()
        result = results_map.get(challenge.id)
        
        if result:
            challenge_data['completed'] = result.completed
            challenge_data['score'] = result.score
        else:
            challenge_data['completed'] = False
            challenge_data['score'] = None
        
        response.append(challenge_data)
    
    return jsonify(response), 200

@challenges_bp.route('/<int:challenge_id>', methods=['GET'])
@jwt_required()
def get_challenge(challenge_id):
    current_user_id = get_jwt_identity()
    
    challenge = Challenge.query.get(challenge_id)
    
    if not challenge:
        return jsonify({'message': 'Desafio não encontrado'}), 404
    
    # Buscar resultado do usuário para este desafio
    result = ChallengeResult.query.filter_by(
        user_id=current_user_id,
        challenge_id=challenge_id
    ).first()
    
    challenge_data = challenge.to_dict()
    
    if result:
        challenge_data['completed'] = result.completed
        challenge_data['score'] = result.score
        challenge_data['feedback'] = result.feedback
    else:
        challenge_data['completed'] = False
        challenge_data['score'] = None
        challenge_data['feedback'] = None
    
    return jsonify(challenge_data), 200

@challenges_bp.route('/<int:challenge_id>/complete', methods=['POST'])
@jwt_required()
def complete_challenge(challenge_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    challenge = Challenge.query.get(challenge_id)
    
    if not challenge:
        return jsonify({'message': 'Desafio não encontrado'}), 404
    
    data = request.get_json() or {}
    
    # Verificar se o desafio já foi completado
    existing_result = ChallengeResult.query.filter_by(
        user_id=current_user_id,
        challenge_id=challenge_id
    ).first()
    
    if existing_result and existing_result.completed:
        return jsonify({'message': 'Desafio já foi completado anteriormente'}), 400
    
    # Processar resultado do desafio
    score = data.get('score')
    feedback = data.get('feedback')
    
    # Para desafios do tipo quiz, o score é obrigatório
    if challenge.challenge_type == 'quiz' and (score is None or not isinstance(score, int)):
        return jsonify({'message': 'Score é obrigatório para desafios do tipo quiz'}), 400
    
    # Criar ou atualizar o resultado
    if existing_result:
        existing_result.completed = True
        existing_result.score = score
        existing_result.feedback = feedback
        existing_result.completed_at = datetime.utcnow()
    else:
        new_result = ChallengeResult(
            user_id=current_user_id,
            challenge_id=challenge_id,
            completed=True,
            score=score,
            feedback=feedback,
            completed_at=datetime.utcnow()
        )
        db.session.add(new_result)
    
    # Adicionar pontos ao usuário
    level_up = user.add_points(challenge.points)
    
    db.session.commit()
    
    response = {
        'message': 'Desafio completado com sucesso',
        'points_earned': challenge.points,
        'total_points': user.points,
        'level': user.level,
        'level_up': level_up
    }
    
    return jsonify(response), 200

# Rota administrativa para criar novos desafios (em produção, deve ser protegida)
@challenges_bp.route('/', methods=['POST'])
@jwt_required()
def create_challenge():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Verificar se o usuário tem permissão (simplificado para desenvolvimento)
    # Em produção, deve verificar se o usuário é admin
    
    data = request.get_json()
    
    # Validar dados
    required_fields = ['title', 'description', 'skill_type', 'challenge_type', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Campo obrigatório ausente: {field}'}), 400
    
    # Validar tipo de skill
    valid_skills = ['communication', 'active_listening', 'conflict_resolution', 
                    'teamwork', 'critical_thinking', 'time_management']
    if data['skill_type'] not in valid_skills:
        return jsonify({'message': f'Tipo de skill inválido. Use um dos seguintes: {", ".join(valid_skills)}'}), 400
    
    # Validar tipo de desafio
    valid_challenge_types = ['video', 'quiz', 'practice']
    if data['challenge_type'] not in valid_challenge_types:
        return jsonify({'message': f'Tipo de desafio inválido. Use um dos seguintes: {", ".join(valid_challenge_types)}'}), 400
    
    # Criar novo desafio
    challenge = Challenge(
        title=data['title'],
        description=data['description'],
        skill_type=data['skill_type'],
        challenge_type=data['challenge_type'],
        content=data['content'],
        points=data.get('points', 10)  # Pontos padrão: 10
    )
    
    db.session.add(challenge)
    db.session.commit()
    
    return jsonify({
        'message': 'Desafio criado com sucesso',
        'challenge': challenge.to_dict()
    }), 201