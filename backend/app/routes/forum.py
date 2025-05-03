from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, ForumPost, ForumComment
from datetime import datetime

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Buscar posts com paginação
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).paginate(page=page, per_page=per_page)
    
    # Preparar resposta
    response = {
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    }
    
    return jsonify(response), 200

@forum_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    # Validar dados
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Título e conteúdo são obrigatórios'}), 400
    
    # Criar novo post
    post = ForumPost(
        user_id=current_user_id,
        title=data['title'],
        content=data['content'],
        created_at=datetime.utcnow()
    )
    
    db.session.add(post)
    
    # Adicionar pontos ao usuário
    user.add_points(5)  # 5 pontos por criar um post
    
    db.session.commit()
    
    return jsonify({
        'message': 'Post criado com sucesso',
        'post': post.to_dict()
    }), 201

@forum_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = ForumPost.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    # Buscar comentários do post
    comments = ForumComment.query.filter_by(post_id=post_id).order_by(ForumComment.created_at).all()
    
    # Preparar resposta
    post_data = post.to_dict()
    post_data['comments'] = [comment.to_dict() for comment in comments]
    
    return jsonify(post_data), 200

@forum_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    post = ForumPost.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    data = request.get_json()
    
    # Validar dados
    if not data or not data.get('content'):
        return jsonify({'message': 'Conteúdo é obrigatório'}), 400
    
    # Criar novo comentário
    comment = ForumComment(
        post_id=post_id,
        user_id=current_user_id,
        content=data['content'],
        created_at=datetime.utcnow()
    )
    
    db.session.add(comment)
    
    # Adicionar pontos ao usuário
    user.add_points(2)  # 2 pontos por comentar
    
    db.session.commit()
    
    return jsonify({
        'message': 'Comentário criado com sucesso',
        'comment': comment.to_dict()
    }), 201

@forum_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()
    
    post = ForumPost.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    # Verificar se o usuário é o autor do post
    if post.user_id != current_user_id:
        return jsonify({'message': 'Você não tem permissão para editar este post'}), 403
    
    data = request.get_json()
    
    # Validar dados
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização'}), 400
    
    # Atualizar campos
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Post atualizado com sucesso',
        'post': post.to_dict()
    }), 200

@forum_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    
    post = ForumPost.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    # Verificar se o usuário é o autor do post
    if post.user_id != current_user_id:
        return jsonify({'message': 'Você não tem permissão para excluir este post'}), 403
    
    # Excluir comentários relacionados
    ForumComment.query.filter_by(post_id=post_id).delete()
    
    # Excluir o post
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Post excluído com sucesso'
    }), 200

@forum_bp.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(post_id, comment_id):
    current_user_id = get_jwt_identity()
    
    comment = ForumComment.query.filter_by(id=comment_id, post_id=post_id).first()
    
    if not comment:
        return jsonify({'message': 'Comentário não encontrado'}), 404
    
    # Verificar se o usuário é o autor do comentário
    if comment.user_id != current_user_id:
        return jsonify({'message': 'Você não tem permissão para excluir este comentário'}), 403
    
    # Excluir o comentário
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({
        'message': 'Comentário excluído com sucesso'
    }), 200