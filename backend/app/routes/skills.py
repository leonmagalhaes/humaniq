from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, SkillAssessment
from datetime import datetime

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/assessment', methods=['POST'])
@jwt_required()
def create_assessment():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    # Validar dados
    required_skills = ['communication', 'active_listening', 'conflict_resolution', 
                       'teamwork', 'critical_thinking', 'time_management']
    
    for skill in required_skills:
        if skill not in data:
            return jsonify({'message': f'Falta avaliação para a habilidade: {skill}'}), 400
        
        # Validar escala Likert (1-5)
        if not isinstance(data[skill], int) or data[skill] < 1 or data[skill] > 5:
            return jsonify({'message': f'Avaliação inválida para {skill}. Use valores de 1 a 5'}), 400
    
    # Criar nova avaliação
    assessment = SkillAssessment(
        user_id=current_user_id,
        communication=data['communication'],
        active_listening=data['active_listening'],
        conflict_resolution=data['conflict_resolution'],
        teamwork=data['teamwork'],
        critical_thinking=data['critical_thinking'],
        time_management=data['time_management'],
        assessment_date=datetime.utcnow()
    )
    
    db.session.add(assessment)
    
    # Adicionar pontos ao usuário pela primeira avaliação
    first_assessment = not SkillAssessment.query.filter_by(user_id=current_user_id).first()
    if first_assessment:
        user.add_points(20)  # 20 pontos pela primeira avaliação
    
    db.session.commit()
    
    return jsonify({
        'message': 'Avaliação de habilidades registrada com sucesso',
        'assessment': assessment.to_dict()
    }), 201

@skills_bp.route('/assessment/history', methods=['GET'])
@jwt_required()
def get_assessment_history():
    current_user_id = get_jwt_identity()
    
    # Buscar todas as avaliações do usuário, ordenadas por data
    assessments = SkillAssessment.query.filter_by(user_id=current_user_id).order_by(SkillAssessment.assessment_date.desc()).all()
    
    return jsonify({
        'assessments': [assessment.to_dict() for assessment in assessments]
    }), 200

@skills_bp.route('/assessment/latest', methods=['GET'])
@jwt_required()
def get_latest_assessment():
    current_user_id = get_jwt_identity()
    
    # Buscar a avaliação mais recente do usuário
    assessment = SkillAssessment.query.filter_by(user_id=current_user_id).order_by(SkillAssessment.assessment_date.desc()).first()
    
    if not assessment:
        return jsonify({'message': 'Nenhuma avaliação encontrada'}), 404
    
    return jsonify(assessment.to_dict()), 200

@skills_bp.route('/assessment/progress', methods=['GET'])
@jwt_required()
def get_skills_progress():
    current_user_id = get_jwt_identity()
    
    # Buscar todas as avaliações do usuário, ordenadas por data
    assessments = SkillAssessment.query.filter_by(user_id=current_user_id).order_by(SkillAssessment.assessment_date).all()
    
    if not assessments:
        return jsonify({'message': 'Nenhuma avaliação encontrada'}), 404
    
    # Preparar dados para o gráfico de progresso
    progress_data = {
        'dates': [assessment.assessment_date.strftime('%d/%m/%Y') for assessment in assessments],
        'communication': [assessment.communication for assessment in assessments],
        'active_listening': [assessment.active_listening for assessment in assessments],
        'conflict_resolution': [assessment.conflict_resolution for assessment in assessments],
        'teamwork': [assessment.teamwork for assessment in assessments],
        'critical_thinking': [assessment.critical_thinking for assessment in assessments],
        'time_management': [assessment.time_management for assessment in assessments]
    }
    
    return jsonify(progress_data), 200