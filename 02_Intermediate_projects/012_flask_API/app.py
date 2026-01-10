from flask import Flask, jsonify
from config import Config

from extensions import db, jwt

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # JWT error handlers to return JSON responses
    @jwt.unauthorized_loader
    def missing_token_callback(err_msg):
        return jsonify({'msg': 'Missing token', 'error': err_msg}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(err_msg):
        return jsonify({'msg': 'Invalid token', 'error': err_msg}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'msg': 'Token expired'}), 401


    from auth import auth_bp
    from routes.todos import todos_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(todos_bp, url_prefix="/todos")

    @app.route('/')
    def index():
        return jsonify({'msg': 'To-Do API', 'status': 'ok'})

    # create database if not exists
    with app.app_context():
        from models import User, Todo  # noqa: F401
        db.create_all()

    return app


app = create_app()
