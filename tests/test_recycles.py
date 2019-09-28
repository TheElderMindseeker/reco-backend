import pytest

from src import create_app
from src.config import TestConfig
from src.models import db, Recycle, TrashPoint


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


def test_get_recycle(client):
    """Test recycle aggregation"""
    new_recycle = Recycle(
        name='Recycle 2',
        address='Recycling str, 24',
        position='POINT(45.853467 65.254376)',
        open_time='10:00',
        close_time='19:00',
        trash_types='plastic&organic&javascript',
        bonus_program=False,
    )
    new_recycle.save()

    query_str = {
        'c_lat': '45.853467',
        'c_lng': '65.254376',
        'radius': 1.0,
    }
    response = client.get('/recycles', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['result'], list)
    assert len(response.json['result']) >= 1

    query_str = {
        'c_lat': '45.853467',
        'c_lng': '65.254376',
        'radius': 1.0,
        'trash_types': 'javascript,organic',
    }
    response = client.get('/recycles', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['result'], list)
    assert len(response.json['result']) >= 1

    query_str = {
        'c_lat': '45.853467',
        'c_lng': '65.254376',
        'radius': 1.0,
        'trash_types': 'plastic,metal',
    }
    response = client.get('/recycles', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['result'], list)
    assert len(response.json['result']) == 0

    response = client.get('/recycles/{}'.format(new_recycle.id))
    assert response.status_code == 200
    assert 'pos_lat' in response.json
    assert 'pos_lng' in response.json


def test_get_trash_point(client):
    """Test getting trash points"""
    new_trash_point = TrashPoint(
        address='Trash Avenue, 77',
        position='POINT(45.173467 64.254076)',
        comment='Pick up here',
        contacts='@TrashGiver',
        trash_types='metal&organic&plastic',
    )
    new_trash_point.save()

    query_str = {
        'c_lat': '45.173467',
        'c_lng': '64.254076',
        'radius': 1.0,
    }
    response = client.get('/trashpoints', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) >= 1

    query_str = {
        'c_lat': '45.173467',
        'c_lng': '64.254076',
        'radius': 1.0,
        'trash_types': 'metal',
    }
    response = client.get('/trashpoints', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) >= 1

    query_str = {
        'c_lat': '45.173467',
        'c_lng': '64.254076',
        'radius': 1.0,
        'trash_types': 'javascript,metal',
    }
    response = client.get('/trashpoints', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) == 0

    response = client.get('/trashpoints/{}'.format(new_trash_point.id))
    assert response.status_code == 200
    assert 'pos_lat' in response.json
    assert 'pos_lng' in response.json


def test_post_recycle(client):
    """Test recycle creation"""
    json_data = {
        'name': 'Recycle 1',
        'address': 'Recycling str, 12',
        'pos_lat': '78.194639',
        'pos_lng': '19.750175',
        'open_time': '10:00',
        'close_time': '19:00',
        'trash_types': 'plastic&organic&javascript',
        'bonus_program': False,
    }
    response = client.post('/recycles', json=json_data)
    assert response.status_code == 200


def test_post_trash_point(client):
    """Test trash point creation"""
    json_data = {
        'address': 'Recycling str, 12',
        'pos_lat': '78.194639',
        'pos_lng': '19.750175',
        'comment': 'thanks dude!',
        'contacts': 'Im so easy to find!',
        'trash_types': 'plastic&organic&javascript',
    }
    response = client.post('/trashpoints', json=json_data)
    assert response.status_code == 200
