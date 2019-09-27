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
        db.drop_all()


def test_get_recycle(client):
    """Test recycle aggregation"""
    new_recycle = Recycle(
        name='Recycle 2',
        address='Recycling str, 24',
        position='POINT(20 40)',
        open_time='10:00',
        close_time='19:00',
        trash_types='plastic&organic&javascript',
        bonus_program=False,
    )
    new_recycle.save()

    query_str = {
        'center': 'POINT(20 40)',
        'radius': 1.0,
    }
    response = client.get('/recycles', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) >= 1

    query_str = {
        'center': 'POINT(20 40)',
        'radius': 1.0,
        'trash_types': 'javascript,organic',
    }
    response = client.get('/recycles', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) >= 1

    query_str = {
        'center': 'POINT(20 40)',
        'radius': 1.0,
        'trash_types': 'plastic,metal',
    }
    response = client.get('/recycles', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) == 0

    response = client.get('/recycles/{}'.format(new_recycle.id))
    assert response.status_code == 200


def test_get_trash_point(client):
    """Test getting trash points"""
    new_trash_point = TrashPoint(
        address='Trash Avenue, 77',
        position='POINT(100 20)',
        comment='Pick up here',
        contacts='@TrashGiver',
        trash_types='metal&organic&plastic',
    )
    new_trash_point.save()

    query_str = {
        'center': 'POINT(100 20)',
        'radius': 1.0,
    }
    response = client.get('/trashpoints', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) >= 1

    query_str = {
        'center': 'POINT(100 20)',
        'radius': 1.0,
        'trash_types': 'metal',
    }
    response = client.get('/trashpoints', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) >= 1

    query_str = {
        'center': 'POINT(100 20)',
        'radius': 1.0,
        'trash_types': 'javascript,metal',
    }
    response = client.get('/trashpoints', query_string=query_str)
    assert response.status_code == 200
    assert isinstance(response.json['ids'], list)
    assert len(response.json['ids']) == 0


def test_post_recycle(client):
    """Test recycle creation"""
    json_data = {
        'name': 'Recycle 1',
        'address': 'Recycling str, 12',
        'position': 'POINT(0 1)',
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
        'position': 'POINT(0 1)',
        'comment': 'thanks dude!',
        'contacts': 'Im so easy to find!',
        'trash_types': 'plastic&organic&javascript',
    }
    response = client.post('/trashpoints', json=json_data)
    assert response.status_code == 200
