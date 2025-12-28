from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Todo, User
from schemas import TodoCreateSchema, TodoUpdateSchema

todos_bp = Blueprint('todos', __name__)


@todos_bp.route('/', methods=['GET'])
@jwt_required()
def list_todos():
    user_id = int(get_jwt_identity())
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    pagination = Todo.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    items = [t.to_dict() for t in pagination.items]
    return jsonify({'items': items, 'page': page, 'per_page': per_page, 'total': pagination.total})


@todos_bp.route('/', methods=['POST'])
@jwt_required()
def create_todo():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    try:
        payload = TodoCreateSchema(**data)
    except Exception as e:
        return jsonify({'msg': 'Invalid input', 'error': str(e)}), 400

    todo = Todo(title=payload.title, description=payload.description, completed=payload.completed, user_id=user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


def _get_todo_or_404(todo_id, user_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return None
    return todo


@todos_bp.route('/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    user_id = int(get_jwt_identity())
    todo = _get_todo_or_404(todo_id, user_id)
    if not todo:
        return jsonify({'msg': 'Not found'}), 404
    return jsonify(todo.to_dict())


@todos_bp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    user_id = int(get_jwt_identity())
    todo = _get_todo_or_404(todo_id, user_id)
    if not todo:
        return jsonify({'msg': 'Not found'}), 404

    data = request.get_json() or {}
    try:
        payload = TodoUpdateSchema(**data)
    except Exception as e:
        return jsonify({'msg': 'Invalid input', 'error': str(e)}), 400

    if payload.title is not None:
        todo.title = payload.title
    if payload.description is not None:
        todo.description = payload.description
    if payload.completed is not None:
        todo.completed = payload.completed

    db.session.commit()
    return jsonify(todo.to_dict())


@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    user_id = int(get_jwt_identity())
    todo = _get_todo_or_404(todo_id, user_id)
    if not todo:
        return jsonify({'msg': 'Not found'}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'msg': 'Deleted'})
