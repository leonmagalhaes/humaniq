from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body=None):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    # Enviar e-mail em uma thread separada para não bloquear a resposta da API
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_welcome_email(user):
    subject = "Bem-vindo ao HUMANIQ!"
    recipients = [user.email]
    text_body = f"""
    Olá {user.name},
    
    Bem-vindo ao HUMANIQ! Estamos muito felizes em tê-lo conosco.
    
    O HUMANIQ é uma plataforma dedicada ao desenvolvimento de soft skills essenciais para o mercado de trabalho.
    
    Para começar, faça o teste inicial de habilidades e descubra quais são seus pontos fortes e áreas para desenvolvimento.
    
    Atenciosamente,
    Equipe HUMANIQ
    """
    
    html_body = f"""
    <h2>Olá {user.name},</h2>
    
    <p>Bem-vindo ao <strong>HUMANIQ</strong>! Estamos muito felizes em tê-lo conosco.</p>
    
    <p>O HUMANIQ é uma plataforma dedicada ao desenvolvimento de soft skills essenciais para o mercado de trabalho.</p>
    
    <p>Para começar, faça o teste inicial de habilidades e descubra quais são seus pontos fortes e áreas para desenvolvimento.</p>
    
    <p>Atenciosamente,<br>
    Equipe HUMANIQ</p>
    """
    
    send_email(subject, recipients, text_body, html_body)

def send_challenge_reminder(user, challenges):
    subject = "HUMANIQ - Desafios da semana"
    recipients = [user.email]
    
    challenge_list = "\n".join([f"- {challenge.title}" for challenge in challenges])
    
    text_body = f"""
    Olá {user.name},
    
    Não se esqueça de completar seus desafios desta semana:
    
    {challenge_list}
    
    Completar esses desafios ajudará você a desenvolver suas soft skills e ganhar pontos na plataforma.
    
    Atenciosamente,
    Equipe HUMANIQ
    """
    
    html_challenge_list = "".join([f"<li>{challenge.title}</li>" for challenge in challenges])
    
    html_body = f"""
    <h2>Olá {user.name},</h2>
    
    <p>Não se esqueça de completar seus desafios desta semana:</p>
    
    <ul>
    {html_challenge_list}
    </ul>
    
    <p>Completar esses desafios ajudará você a desenvolver suas soft skills e ganhar pontos na plataforma.</p>
    
    <p>Atenciosamente,<br>
    Equipe HUMANIQ</p>
    """
    
    send_email(subject, recipients, text_body, html_body)

def send_monthly_report(user, progress_data):
    subject = "HUMANIQ - Seu relatório mensal de progresso"
    recipients = [user.email]
    
    text_body = f"""
    Olá {user.name},
    
    Aqui está seu relatório mensal de progresso no HUMANIQ:
    
    Pontos totais: {user.points}
    Nível atual: {user.level}
    Desafios completados: {progress_data['completed_challenges']}
    Badges conquistadas: {progress_data['badges_earned']}
    
    Habilidades mais desenvolvidas:
    - {progress_data['top_skills'][0]}
    - {progress_data['top_skills'][1]}
    
    Continue se dedicando ao seu desenvolvimento!
    
    Atenciosamente,
    Equipe HUMANIQ
    """
    
    html_body = f"""
    <h2>Olá {user.name},</h2>
    
    <p>Aqui está seu relatório mensal de progresso no HUMANIQ:</p>
    
    <ul>
        <li><strong>Pontos totais:</strong> {user.points}</li>
        <li><strong>Nível atual:</strong> {user.level}</li>
        <li><strong>Desafios completados:</strong> {progress_data['completed_challenges']}</li>
        <li><strong>Badges conquistadas:</strong> {progress_data['badges_earned']}</li>
    </ul>
    
    <p><strong>Habilidades mais desenvolvidas:</strong></p>
    <ul>
        <li>{progress_data['top_skills'][0]}</li>
        <li>{progress_data['top_skills'][1]}</li>
    </ul>
    
    <p>Continue se dedicando ao seu desenvolvimento!</p>
    
    <p>Atenciosamente,<br>
    Equipe HUMANIQ</p>
    """
    
    send_email(subject, recipients, text_body, html_body)