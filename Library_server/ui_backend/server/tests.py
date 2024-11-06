import pytest
from . import create_app
from flask import url_for

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'  # Add this line

    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login_redirect(client):
    login_url = url_for('auth.login')
    for _ in range(50):  # Adjust to desired number of checks
        response = client.get(login_url, follow_redirects=True)
        
        assert response.request.path == '/auth/login'
        assert response.status_code == 200

