"""
Script simples para testar a conexão com o banco de dados SQLite.
"""

import os
import sqlite3

def test_sqlite_connection():
    """Testa a conexão direta com o banco de dados SQLite."""
    # Define o caminho do banco de dados
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'humaniq.db'))
    
    print(f"Tentando conectar ao banco de dados em: {db_path}")
    print(f"O arquivo existe? {os.path.exists(db_path)}")
    
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lista as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nTabelas encontradas:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Conta registros em algumas tabelas
    print("\nContagem de registros por tabela:")
    for table in ['users', 'challenges', 'skill_assessments', 'forum_posts']:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"- {table}: {count} registros")
    
    # Lista alguns usuários
    print("\nUsuários cadastrados:")
    cursor.execute("SELECT id, name, email, points FROM users;")
    users = cursor.fetchall()
    for user in users:
        print(f"ID: {user[0]}, Nome: {user[1]}, Email: {user[2]}, Pontos: {user[3]}")
    
    # Lista alguns desafios
    print("\nDesafios disponíveis:")
    cursor.execute("SELECT id, title, skill_type FROM challenges;")
    challenges = cursor.fetchall()
    for challenge in challenges:
        print(f"ID: {challenge[0]}, Título: {challenge[1]}, Tipo: {challenge[2]}")
    
    # Fecha a conexão
    conn.close()
    
    print("\nConexão com o banco de dados testada com sucesso!")

if __name__ == "__main__":
    print("Testando conexão direta com o banco de dados SQLite...")
    test_sqlite_connection()
