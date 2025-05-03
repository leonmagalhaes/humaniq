"""
Script para inicializar o banco de dados usando Flask-SQLAlchemy.
Este script cria as tabelas definidas nos modelos e popula o banco de dados com dados de exemplo.
"""

import os
import sys
import sqlite3

# Adiciona o diretório pai ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def init_flask_db():
    """Inicializa o banco de dados usando Flask-SQLAlchemy."""
    from app import create_app, db
    from app.models import User, Challenge, SkillAssessment, ChallengeResult, Badge, ForumPost, ForumComment
    from werkzeug.security import generate_password_hash
    
    app = create_app('development')
    
    with app.app_context():
        # Cria as tabelas
        db.create_all()
        print("Tabelas criadas com sucesso!")
        
        # Verifica se já existem dados
        if User.query.first() is not None:
            print("O banco de dados já contém dados. Deseja limpar e recriar? (s/n)")
            choice = input().lower()
            if choice == 's':
                # Limpa todas as tabelas
                db.session.query(ForumComment).delete()
                db.session.query(ForumPost).delete()
                db.session.query(ChallengeResult).delete()
                db.session.query(SkillAssessment).delete()
                db.session.query(User).delete()
                db.session.query(Challenge).delete()
                db.session.query(Badge).delete()
                db.session.commit()
                print("Dados existentes removidos.")
            else:
                print("Operação cancelada.")
                return
        
        # Popula o banco de dados com dados de exemplo
        print("Populando o banco de dados com dados de exemplo...")
        
        # Executa o script SQL de população de dados
        script_dir = os.path.dirname(__file__)
        seed_data_path = os.path.join(script_dir, 'seed_data.sql')
        
        # Conecta diretamente ao SQLite para executar o script SQL
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'humaniq.db'))
        conn = sqlite3.connect(db_path)
        
        with open(seed_data_path, 'r') as f:
            seed_data_script = f.read()
            conn.executescript(seed_data_script)
        
        conn.commit()
        conn.close()
        
        print("Banco de dados populado com sucesso!")
        
        # Verifica se os dados foram inseridos corretamente
        users_count = User.query.count()
        challenges_count = Challenge.query.count()
        
        print(f"\nDados inseridos:")
        print(f"- Usuários: {users_count}")
        print(f"- Desafios: {challenges_count}")
        print(f"- Avaliações: {SkillAssessment.query.count()}")
        print(f"- Resultados de desafios: {ChallengeResult.query.count()}")
        print(f"- Badges: {Badge.query.count()}")
        print(f"- Posts no fórum: {ForumPost.query.count()}")
        print(f"- Comentários no fórum: {ForumComment.query.count()}")

if __name__ == "__main__":
    print("Inicializando o banco de dados HUMANIQ usando Flask-SQLAlchemy...")
    init_flask_db()
    print("Inicialização concluída!")
