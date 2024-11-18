from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash
from server.models import User


class TestAuth:
    def test_register_user(self, client, db_session):
        """Test user registration."""
        existing_user = db_session.query(User).filter_by(nick='testuser').first()
        assert existing_user == None

        response = client.post(
            "/auth/register",
            data={
                "nick": "testuser",
                "name": "Test",
                "surname": "User",
                "email": "test@example.com",
                "password": "password123",
                'repeat_password': 'password123',
                "age": '2000-01-01',
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

        soup = BeautifulSoup(response.data, 'html.parser')
        nick = soup.find('h1', class_='display-4')

        assert nick == 'testuser'
        
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
                age=22,
            )
        )
        db_session.commit()

        response = client.post(
            "/auth/login",
            data={"nick": "testuser", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_logout_user(self, client):
        """Test user logout."""
        response = client.post(
            "/auth/login",
            data={"nick": "testuser", "password": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        nick = soup.find('h1', class_='display-4')

        assert nick == 'testuser'

        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200
