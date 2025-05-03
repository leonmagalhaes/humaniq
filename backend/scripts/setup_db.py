"""
Script para configurar o banco de dados SQLite do projeto HUMANIQ.
Este script cria as tabelas e popula o banco de dados com dados de exemplo.
"""

import os
import sys
import sqlite3

# Adiciona o diretório pai ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def setup_db():
    """Configura o banco de dados com as tabelas e dados de exemplo."""
    # Cria o diretório instance se não existir
    instance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    # Define o caminho do banco de dados
    db_path = os.path.join(instance_dir, 'humaniq.db')
    
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
    
    print(f"Banco de dados configurado com sucesso em {db_path}")

if __name__ == "__main__":
    print("Configurando o banco de dados HUMANIQ...")
    setup_db()
    print("Configuração concluída!")
