from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, SkillAssessment, ChallengeResult, Certificate, Challenge
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Buscar a avaliação mais recente
    latest_assessment = SkillAssessment.query.filter_by(user_id=current_user_id).order_by(SkillAssessment.assessment_date.desc()).first()
    
    # Contar desafios completados
    completed_challenges = ChallengeResult.query.filter_by(user_id=current_user_id, completed=True).count()
    
    # Buscar certificados
    certificates = Certificate.query.filter_by(user_id=current_user_id).all()
    
    # Preparar resposta
    profile_data = user.to_dict()
    profile_data['completed_challenges'] = completed_challenges
    profile_data['certificates'] = [cert.to_dict() for cert in certificates]
    
    if latest_assessment:
        profile_data['latest_assessment'] = latest_assessment.to_dict()
    
    return jsonify(profile_data), 200

@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar apenas os campos permitidos
    if 'name' in data:
        user.name = data['name']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Perfil atualizado com sucesso',
        'user': user.to_dict()
    }), 200

@profile_bp.route('/certificates', methods=['GET'])
@jwt_required()
def get_certificates():
    current_user_id = get_jwt_identity()
    
    certificates = Certificate.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'certificates': [cert.to_dict() for cert in certificates]
    }), 200

@profile_bp.route('/certificates/<int:certificate_id>', methods=['GET'])
@jwt_required()
def get_certificate(certificate_id):
    current_user_id = get_jwt_identity()
    
    certificate = Certificate.query.filter_by(id=certificate_id, user_id=current_user_id).first()
    
    if not certificate:
        return jsonify({'message': 'Certificado não encontrado'}), 404
    
    return jsonify(certificate.to_dict()), 200

@profile_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Buscar todas as avaliações do usuário, ordenadas por data
    assessments = SkillAssessment.query.filter_by(user_id=current_user_id).order_by(SkillAssessment.assessment_date).all()
    
    # Buscar todos os desafios completados, agrupados por tipo de habilidade
    challenge_results = db.session.query(
        ChallengeResult.challenge_id,
        ChallengeResult.completed_at
    ).join(
        Challenge, ChallengeResult.challenge_id == Challenge.id
    ).filter(
        ChallengeResult.user_id == current_user_id,
        ChallengeResult.completed == True
    ).all()
    
    # Preparar dados de progresso
    progress_data = {
        'user': user.to_dict(),
        'assessments': [assessment.to_dict() for assessment in assessments],
        'completed_challenges': len(challenge_results),
        'completion_dates': [result.completed_at.strftime('%Y-%m-%d') for result in challenge_results if result.completed_at]
    }
    
    return jsonify(progress_data), 200

# Rota para gerar certificado (simplificada para desenvolvimento)
@profile_bp.route('/certificates', methods=['POST'])
@jwt_required()
def generate_certificate():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'message': 'Título do certificado é obrigatório'}), 400
    
    # Criar novo certificado
    certificate = Certificate(
        user_id=current_user_id,
        title=data['title'],
        description=data.get('description', 'Certificado de conclusão'),
        issue_date=datetime.utcnow()
    )
    
    db.session.add(certificate)
    db.session.commit()
    
    return jsonify({
        'message': 'Certificado gerado com sucesso',
        'certificate': certificate.to_dict()
    }), 201