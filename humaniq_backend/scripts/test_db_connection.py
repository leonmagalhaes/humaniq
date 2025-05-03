"""
Script para testar a conexão com o banco de dados SQLite usando Flask-SQLAlchemy.
"""

import os
import sys

# Adiciona o diretório pai ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_connection():
    """Testa a conexão com o banco de dados e exibe informações sobre as tabelas."""
    from app import create_app, db
    from app.models import User, Challenge, SkillAssessment, ChallengeResult, Badge, ForumPost, ForumComment
    
    app = create_app('development')
    
    with app.app_context():
        # Verifica se as tabelas existem
        print("Verificando tabelas no banco de dados...")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelas encontradas: {tables}")
        
        # Conta registros em cada tabela
        print("\nContagem de registros por tabela:")
        print(f"Usuários: {User.query.count()}")
        print(f"Avaliações de habilidades: {SkillAssessment.query.count()}")
        print(f"Desafios: {Challenge.query.count()}")
        print(f"Resultados de desafios: {ChallengeResult.query.count()}")
        print(f"Badges: {Badge.query.count()}")
        print(f"Posts no fórum: {ForumPost.query.count()}")
        print(f"Comentários no fórum: {ForumComment.query.count()}")
        
        # Lista alguns usuários
        print("\nUsuários cadastrados:")
        for user in User.query.all():
            print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}, Pontos: {user.points}")
        
        # Lista alguns desafios
        print("\nDesafios disponíveis:")
        for challenge in Challenge.query.all():
            print(f"ID: {challenge.id}, Título: {challenge.title}, Tipo: {challenge.skill_type}")
        
        print("\nConexão com o banco de dados testada com sucesso!")

if __name__ == "__main__":
    print("Testando conexão com o banco de dados HUMANIQ...")
    test_connection()
