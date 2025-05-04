from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Usuario, Avaliacao, Resultado
from app import db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def obter_perfil():
    """
    Endpoint para obter o perfil do usuário autenticado
    ---
    Requer:
      - Token de acesso JWT válido
    Retorna:
      - Informações do perfil do usuário
    """
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(int(current_user_id))
    
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Obter avaliações e resultados do usuário
    avaliacoes = Avaliacao.query.filter_by(usuario_id=int(current_user_id)).all()
    resultados = Resultado.query.filter_by(usuario_id=int(current_user_id)).all()
    
    # Preparar dados para retorno
    perfil = usuario.to_dict()
    perfil['avaliacoes'] = [avaliacao.to_dict() for avaliacao in avaliacoes]
    perfil['resultados'] = [resultado.to_dict() for resultado in resultados]
    
    return jsonify({
        'message': 'Perfil obtido com sucesso',
        'perfil': perfil
    }), 200

@user_bp.route('/perfil', methods=['PUT'])
@jwt_required()
def atualizar_perfil():
    """
    Endpoint para atualizar o perfil do usuário autenticado
    ---
    Requer:
      - Token de acesso JWT válido
    Parâmetros:
      - nome: Novo nome do usuário (opcional)
      - email: Novo email do usuário (opcional)
      - senha_atual: Senha atual (obrigatória para alterar a senha)
      - nova_senha: Nova senha (opcional)
    Retorna:
      - Informações atualizadas do perfil
    """
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(int(current_user_id))
    
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização'}), 400
    
    # Atualizar nome se fornecido
    if 'nome' in data and data['nome']:
        usuario.nome = data['nome']
    
    # Atualizar email se fornecido
    if 'email' in data and data['email']:
        # Verificar se o novo email já está em uso por outro usuário
        email_existente = Usuario.query.filter_by(email=data['email']).first()
        if email_existente and email_existente.id != int(current_user_id):
            return jsonify({'message': 'Email já está em uso por outro usuário'}), 409
        
        usuario.email = data['email']
    
    # Atualizar senha se fornecida
    if 'nova_senha' in data and data['nova_senha']:
        # Verificar se a senha atual foi fornecida e está correta
        if not data.get('senha_atual'):
            return jsonify({'message': 'Senha atual é obrigatória para alterar a senha'}), 400
        
        if not usuario.verificar_senha(data['senha_atual']):
            return jsonify({'message': 'Senha atual incorreta'}), 401
        
        # Atualizar a senha
        usuario.senha_hash = generate_password_hash(data['nova_senha'])
    
    # Salvar alterações
    db.session.commit()
    
    return jsonify({
        'message': 'Perfil atualizado com sucesso',
        'usuario': usuario.to_dict()
    }), 200

@user_bp.route('/progresso', methods=['GET'])
@jwt_required()
def obter_progresso():
    """
    Endpoint para obter o progresso do usuário nos desafios
    ---
    Requer:
      - Token de acesso JWT válido
    Retorna:
      - Informações sobre o progresso do usuário nos desafios
    """
    current_user_id = get_jwt_identity()
    
    # Obter resultados dos desafios do usuário
    resultados = Resultado.query.filter_by(usuario_id=int(current_user_id)).all()
    
    # Calcular estatísticas de progresso
    total_desafios = len(resultados)
    desafios_concluidos = sum(1 for r in resultados if r.status == 'concluído')
    desafios_pendentes = sum(1 for r in resultados if r.status == 'pendente')
    
    # Calcular pontuação total
    pontuacao_total = sum(r.pontuacao for r in resultados)
    
    # Preparar dados para retorno
    progresso = {
        'total_desafios': total_desafios,
        'desafios_concluidos': desafios_concluidos,
        'desafios_pendentes': desafios_pendentes,
        'pontuacao_total': pontuacao_total,
        'resultados': [resultado.to_dict() for resultado in resultados]
    }
    
    return jsonify({
        'message': 'Progresso obtido com sucesso',
        'progresso': progresso
    }), 200
