from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token
from schemas import UserCreateSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    try:
        payload = UserCreateSchema(**data)
    except Exception as e:
        return jsonify({'msg': 'Invalid input', 'error': str(e)}), 400

    if User.query.filter((User.username == payload.username) | (User.email == payload.email)).first():
        return jsonify({'msg': 'User with that username or email already exists'}), 400

    user = User(username=payload.username, email=payload.email)
    user.set_password(payload.password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'User created', 'user': {'id': user.id, 'username': user.username}}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    try:
        payload = UserLoginSchema(**data)
    except Exception as e:
        return jsonify({'msg': 'Invalid input', 'error': str(e)}), 400

    user = User.query.filter_by(username=payload.username).first()
    if not user or not user.check_password(payload.password):
        return jsonify({'msg': 'Bad username or password'}), 401

    # PyJWT expects string 'sub' claim; store user id as string in token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200
