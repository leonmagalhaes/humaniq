from datetime import datetime, timedelta
from flask import current_app
from app import db
from app.models import User, Challenge, ChallengeResult, SkillAssessment
from app.email_utils import send_challenge_reminder, send_monthly_report
from sqlalchemy import func

def send_weekly_reminders():
    """Envia lembretes semanais sobre desafios pendentes"""
    with current_app.app_context():
        # Buscar todos os usuários ativos
        users = User.query.all()
        
        # Buscar desafios ativos
        active_challenges = Challenge.query.order_by(Challenge.created_at.desc()).limit(3).all()
        
        for user in users:
            # Verificar se o usuário já completou os desafios
            completed_challenges = ChallengeResult.query.filter(
                ChallengeResult.user_id == user.id,
                ChallengeResult.challenge_id.in_([c.id for c in active_challenges]),
                ChallengeResult.completed == True
            ).all()
            
            # Filtrar apenas os desafios não completados
            pending_challenges = [c for c in active_challenges if c.id not in [cr.challenge_id for cr in completed_challenges]]
            
            # Enviar e-mail apenas se houver desafios pendentes
            if pending_challenges:
                send_challenge_reminder(user, pending_challenges)

def send_monthly_reports():
    """Envia relatórios mensais de progresso para os usuários"""
    with current_app.app_context():
        # Buscar todos os usuários ativos
        users = User.query.all()
        
        # Data de um mês atrás
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        
        for user in users:
            # Contar desafios completados no último mês
            completed_challenges = ChallengeResult.query.filter(
                ChallengeResult.user_id == user.id,
                ChallengeResult.completed == True,
                ChallengeResult.completed_at >= one_month_ago
            ).count()
            
            # Contar badges conquistadas no último mês
            badges_earned = len(user.badges)
            
            # Buscar as habilidades mais desenvolvidas
            latest_assessment = SkillAssessment.query.filter_by(user_id=user.id).order_by(SkillAssessment.assessment_date.desc()).first()
            
            top_skills = []
            if latest_assessment:
                skills = {
                    'Comunicação clara': latest_assessment.communication,
                    'Escuta ativa': latest_assessment.active_listening,
                    'Resolução de conflitos': latest_assessment.conflict_resolution,
                    'Trabalho em equipe': latest_assessment.teamwork,
                    'Pensamento crítico': latest_assessment.critical_thinking,
                    'Gestão do tempo': latest_assessment.time_management
                }
                
                # Ordenar habilidades por pontuação
                sorted_skills = sorted(skills.items(), key=lambda x: x[1], reverse=True)
                top_skills = [skill[0] for skill in sorted_skills[:2]]
            else:
                top_skills = ['Não avaliado', 'Não avaliado']
            
            # Preparar dados para o relatório
            progress_data = {
                'completed_challenges': completed_challenges,
                'badges_earned': badges_earned,
                'top_skills': top_skills
            }
            
            # Enviar relatório
            send_monthly_report(user, progress_data)

def init_scheduler(scheduler):
    """Inicializa o agendador de tarefas"""
    # Agendar o envio de lembretes semanais (toda segunda-feira às 9h)
    scheduler.add_job(
        send_weekly_reminders,
        'cron',
        day_of_week='mon',
        hour=9,
        minute=0
    )
    
    # Agendar o envio de relatórios mensais (primeiro dia do mês às 10h)
    scheduler.add_job(
        send_monthly_reports,
        'cron',
        day=1,
        hour=10,
        minute=0
    )