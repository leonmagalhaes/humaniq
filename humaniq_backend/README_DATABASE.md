# Configuração do Banco de Dados HUMANIQ

Este documento descreve a configuração do banco de dados SQLite para o projeto HUMANIQ.

## Estrutura do Banco de Dados

O banco de dados SQLite está localizado em `~/humaniq_backend/instance/humaniq.db` e contém as seguintes tabelas:

1. **users** - Armazena informações dos usuários
   - id, name, email, password_hash, created_at, last_login, points, level

2. **skill_assessments** - Armazena avaliações de soft skills dos usuários
   - id, user_id, communication, active_listening, conflict_resolution, teamwork, critical_thinking, time_management, assessment_date

3. **challenges** - Armazena os desafios disponíveis
   - id, title, description, skill_type, challenge_type, content, points, created_at

4. **challenge_results** - Armazena os resultados dos desafios completados pelos usuários
   - id, user_id, challenge_id, completed, score, feedback, completed_at

5. **badges** - Armazena as conquistas disponíveis
   - id, name, description, image_url, requirement

6. **user_badges** - Tabela de associação entre usuários e badges
   - user_id, badge_id

7. **forum_posts** - Armazena os posts do fórum
   - id, user_id, title, content, created_at

8. **forum_comments** - Armazena os comentários nos posts do fórum
   - id, post_id, user_id, content, created_at

9. **certificates** - Armazena os certificados emitidos para os usuários
   - id, user_id, title, description, issue_date

## Scripts Disponíveis

Os seguintes scripts estão disponíveis na pasta `scripts/`:

1. **create_tables.sql** - Script SQL para criar as tabelas do banco de dados
2. **seed_data.sql** - Script SQL para popular o banco de dados com dados de exemplo
3. **setup_db.py** - Script Python para configurar o banco de dados (criar tabelas e inserir dados de exemplo)
4. **init_db.py** - Script Python interativo para inicializar o banco de dados
5. **simple_test_db.py** - Script Python para testar a conexão direta com o banco de dados SQLite
6. **flask_test_db.py** - Script Python para testar a conexão com o banco de dados usando Flask-SQLAlchemy
7. **init_flask_db.py** - Script Python para inicializar o banco de dados usando Flask-SQLAlchemy

## Como Usar

### Configuração Inicial do Banco de Dados

Para configurar o banco de dados pela primeira vez, execute:

```bash
cd ~/humaniq_backend
python scripts/setup_db.py
```

### Testar a Conexão com o Banco de Dados

Para testar a conexão direta com o banco de dados SQLite:

```bash
cd ~/humaniq_backend
python scripts/simple_test_db.py
```

Para testar a conexão com o banco de dados usando Flask-SQLAlchemy:

```bash
cd ~/humaniq_backend
python scripts/flask_test_db.py
```

### Reinicializar o Banco de Dados

Para reinicializar o banco de dados usando Flask-SQLAlchemy:

```bash
cd ~/humaniq_backend
python scripts/init_flask_db.py
```

## Modelos SQLAlchemy

Os modelos SQLAlchemy estão definidos em `app/models.py` e incluem:

- User
- SkillAssessment
- Challenge
- ChallengeResult
- Badge
- ForumPost
- ForumComment
- Certificate

## Conexão com o Backend

O backend Flask está configurado para usar o banco de dados SQLite em `instance/humaniq.db`. A configuração está definida em `config.py`:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/humaniq.db'
```

A inicialização do banco de dados ocorre em `app/__init__.py` através da extensão Flask-SQLAlchemy.
