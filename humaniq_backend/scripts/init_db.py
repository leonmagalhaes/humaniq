"""
Script para inicializar o banco de dados SQLite do projeto HUMANIQ.
Este script cria as tabelas e popula o banco de dados com dados de exemplo.
"""

import os
import sys
import sqlite3

# Adiciona o diretório pai ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_instance_dir():
    """Cria o diretório instance se não existir."""
    instance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    return instance_dir

def init_db():
    """Inicializa o banco de dados com as tabelas e dados de exemplo."""
    instance_dir = create_instance_dir()
    db_path = os.path.join(instance_dir, 'humaniq.db')
    
    # Verifica se o banco de dados já existe
    if os.path.exists(db_path):
        print(f"O banco de dados já existe em {db_path}")
        choice = input("Deseja recriá-lo? (s/n): ").lower()
        if choice != 's':
            print("Operação cancelada.")
            return
        os.remove(db_path)
        print("Banco de dados existente removido.")
    
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Executa o script de criação de tabelas
    script_dir = os.path.dirname(__file__)
    create_tables_path = os.path.join(script_dir, 'create_tables.sql')
    
    with open(create_tables_path, 'r') as f:
        create_tables_script = f.read()
        cursor.executescript(create_tables_script)
    
    # Executa o script de população de dados
    seed_data_path = os.path.join(script_dir, 'seed_data.sql')
    
    with open(seed_data_path, 'r') as f:
        seed_data_script = f.read()
        cursor.executescript(seed_data_script)
    
    # Commit e fecha a conexão
    conn.commit()
    conn.close()
    
    print(f"Banco de dados inicializado com sucesso em {db_path}")

def init_db_with_flask():
    """Inicializa o banco de dados usando o Flask-SQLAlchemy."""
    from app import create_app, db
    
    app = create_app('development')
    
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos
        db.create_all()
        
        # Executa o script de população de dados
        script_dir = os.path.dirname(__file__)
        seed_data_path = os.path.join(script_dir, 'seed_data.sql')
        
        with open(seed_data_path, 'r') as f:
            seed_data_script = f.read()
            db.session.execute(seed_data_script)
        
        db.session.commit()
    
    print("Banco de dados inicializado com sucesso usando Flask-SQLAlchemy")

if __name__ == "__main__":
    print("Inicializando o banco de dados HUMANIQ...")
    
    # Escolha o método de inicialização
    method = input("Escolha o método de inicialização (1 - SQLite direto, 2 - Flask-SQLAlchemy): ")
    
    if method == "1":
        init_db()
    elif method == "2":
        init_db_with_flask()
    else:
        print("Opção inválida. Usando SQLite direto por padrão.")
        init_db()
