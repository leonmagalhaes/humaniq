"""
Script para testar a conexão com o banco de dados usando Flask-SQLAlchemy.
"""

import os
import sys

# Adiciona o diretório pai ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_flask_db_connection():
    """Testa a conexão com o banco de dados usando Flask-SQLAlchemy."""
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    # Cria uma aplicação Flask simples
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'humaniq.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o SQLAlchemy
    db = SQLAlchemy(app)
    
    # Define um modelo simples para teste
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        email = db.Column(db.String(100))
        points = db.Column(db.Integer)
    
    # Testa a conexão
    with app.app_context():
        # Verifica as tabelas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelas encontradas: {tables}")
        
        # Conta usuários
        users_count = User.query.count()
        print(f"\nNúmero de usuários: {users_count}")
        
        # Lista usuários
        print("\nUsuários cadastrados:")
        for user in User.query.all():
            print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}, Pontos: {user.points}")
    
    print("\nConexão com o banco de dados usando Flask-SQLAlchemy testada com sucesso!")

if __name__ == "__main__":
    print("Testando conexão com o banco de dados usando Flask-SQLAlchemy...")
    test_flask_db_connection()
