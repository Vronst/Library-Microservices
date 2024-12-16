from bs4 import BeautifulSoup
from flask import url_for, request
from werkzeug.security import generate_password_hash
from server.models import User
from ...utils import simple_logs


class TestAuth:
    def test_register_user(self, client, db_session):
        """Test user registration."""
        existing_user = db_session.query(User).filter_by(nick='testuser').first()
        assert existing_user == None

        response = client.post(
            "/auth/register",
            data={
                "nick": "testuser1",
                "name": "Test",
                "surname": "User",
                "email": "test1@example.com",
                "password": "password123",
                'repeat_password': 'password123',
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

        soup = BeautifulSoup(response.data, 'html.parser')
        nick = soup.find('h1', class_='display-4')

        simple_logs('test_register', response.text)

        assert nick.string == 'testuser'
        
        user = db_session.query(User).filter_by(nick="testuser").first()
        assert user is not None

    def test_login_user(self, client, db_session):
        """Test user login."""
        # Create a user directly in the database
        db_session.add(
            User(
                nick="testuser",
                name="Test",
                surname="User",
                email="test@example.com",
                password=generate_password_hash('pasword123', salt_length=24),  
            )
        )
        # db_session.commit()

        response = client.post(
            "/auth/login",
            data={"email": "test@example.com", "password": "password123"},
            follow_redirects=True,
        )
        simple_logs('test_login', response.text)
        assert response.status_code == 200
        assert response.request.path == '/'

    def test_logout_user(self, client, db_session):
        """Test user logout."""
        db_session.add(
            User(
                nick='testuer',
                name='Test',
                surname='User',
                email='test@example.com',
                password=generate_password_hash('password123')
            )
        )
        # db_session.commit()
        response = client.post(
            "/auth/login",
            data={"email": "test@example.com", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        simple_logs('test_logout', response.text) 
        soup = BeautifulSoup(response.data, 'html.parser')
        nick = soup.find('h1', class_='display-4')

        assert nick.string == 'Welcome Test!'

        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200
