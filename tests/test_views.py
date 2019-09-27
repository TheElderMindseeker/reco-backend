"""Testing basic views"""
import pytest

from src.config import TestConfig
from src.main import create_app
from src.models import db


@pytest.fixture(scope='module')
def client():
    """Test client for Flask WSGI application"""
    app = create_app(TestConfig)
    with app.app_context():
        t_client = app.test_client()
        db.create_all()
        yield t_client
        db.drop_all()


def test_hello(client):
    """Test hello view"""
    response = client.get('/hello')
    assert response.status_code == 200
