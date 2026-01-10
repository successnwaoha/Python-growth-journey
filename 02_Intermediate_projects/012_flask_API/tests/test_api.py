import os
import sys
import pytest

# ensure project root is on sys.path so `from app import create_app` works
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from app import create_app
from config import Config
from extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-jwt-secret'


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client


def register_and_login(client):
    user = {'username': 'alice', 'email': 'alice@example.com', 'password': 'secret123'}
    r = client.post('/auth/register', json=user)
    assert r.status_code == 201

    r = client.post('/auth/login', json={'username': 'alice', 'password': 'secret123'})
    assert r.status_code == 200
    token = r.get_json()['access_token']
    return token


def test_todo_crud_flow(client):
    token = register_and_login(client)
    headers = {'Authorization': f'Bearer {token}'}

    # create
    r = client.post('/todos/', json={'title': 'Buy milk', 'description': '2 liters'}, headers=headers)
    assert r.status_code == 201
    todo = r.get_json()
    todo_id = todo['id']

    # list
    r = client.get('/todos/', headers=headers)
    data = r.get_json()
    assert r.status_code == 200
    assert data['total'] == 1

    # get
    r = client.get(f'/todos/{todo_id}', headers=headers)
    assert r.status_code == 200

    # update
    r = client.put(f'/todos/{todo_id}', json={'completed': True}, headers=headers)
    assert r.status_code == 200
    assert r.get_json()['completed'] is True

    # delete
    r = client.delete(f'/todos/{todo_id}', headers=headers)
    assert r.status_code == 200

    # ensure deleted
    r = client.get('/todos/', headers=headers)
    assert r.get_json()['total'] == 0
