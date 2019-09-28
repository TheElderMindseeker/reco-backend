import pytest

from src import create_app
from src.config import TestConfig
from src.models import db, Recycle, TrashPoint, User
from src.helpers import bcrypt


@pytest.fixture(scope='module')
def client():
    """Test client for Flask WSGI application"""
    app = create_app(TestConfig)
    with app.app_context():
        t_client = app.test_client()
        db.create_all()
        yield t_client
        db.session.close()
        db.drop_all()


def test_users_post_and_get(client):
    """Test creation of a new user"""
    json_data = {
        'phone': '+79872653548',
        'password': 'mtgdotp2',
    }
    response = client.post('/users', json=json_data)
    assert response.status_code == 200

    query_str = {
        'phone': '+79872653548',
        'password': 'mtgdotp2',
    }
    response = client.get('/users', query_string=query_str)
    assert response.status_code == 200
    assert 'token' in response.json.keys()


def test_users_get_points(client):
    """Get user's points balance"""
    json_data = {
        'phone': '+71234567890',
        'password': '1234user',
    }
    response = client.post('/users', json=json_data)
    assert response.status_code == 200

    query_str = {
        'phone': '+71234567890',
        'password': '1234user',
    }
    response = client.get('/users', query_string=query_str)
    assert response.status_code == 200
    assert 'token' in response.json.keys()

    access_token = response.json['token']
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    response = client.get('/users/+71234567890', headers=headers)
    assert response.status_code == 200
    assert 'points' in response.json
