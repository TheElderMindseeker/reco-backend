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

    response = client.get('/users', query_string=json_data)
    assert response.status_code == 200
    assert 'token' in response.json.keys()

    access_token = response.json['token']
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    response = client.get('/users/+71234567890', headers=headers)
    assert response.status_code == 200
    assert 'points' in response.json


def test_users_set_add(client):
    """Set user to be operator and add points"""
    json_data = {
        'phone': '+71234567891',
        'password': '1234oper',
    }
    response = client.post('/users', json=json_data)
    assert response.status_code == 200

    t_user = User.query.filter_by(phone='+71234567891').first()
    t_user.is_operator = True
    t_user.save()

    response = client.get('/users', query_string=json_data)
    assert response.status_code == 200

    access_token = response.json['token']
    headers = {
        ('Authorization', 'Bearer ' + access_token),
    }
    json_data = {
        'add_points': 10,
    }
    response = client.put('/users/+71234567891', headers=headers, json=json_data)
    assert response.status_code == 200
