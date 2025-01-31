from bs4 import BeautifulSoup
from flask import url_for, request
from werkzeug.security import generate_password_hash
from server.models import User
from ...utils import simple_logs
from ...conftest import USER, DATA


class TestAuthPositive:
    user: User = User(**USER)

    def test_register_user(self, client, db_session) -> None:
        """Test user registration."""
        existing_user = db_session.query(User).filter_by(nick=self.user.nick).first()
        assert existing_user == None

        response = client.post(
            "/auth/register",
            data=DATA,
            follow_redirects=True,
        )
        assert response.status_code == 200

        soup = BeautifulSoup(response.data, 'html.parser')
        nick = soup.find('h1', class_='display-4')

        simple_logs('test_register', response.text)

        assert nick.string == 'Welcome tester!'
        
        user = db_session.query(User).filter_by(nick=self.user.nick).first()
        assert user is not None

    def test_login_and_logout_user(self, client, db_session) -> None:
        """Test user login."""
        # Create a user directly in the database
        db_session.add(
            self.user
        )
        db_session.commit()

        response = client.post(
            "/auth/login",
            data={"email": DATA.get('email'), "password": DATA.get('password')},
            follow_redirects=True,
        )
        simple_logs('test_login', response.text)
        assert response.status_code == 200
        assert response.request.path == '/'

        soup = BeautifulSoup(response.data, 'html.parser')
        nick = soup.find('h1', class_='display-4')

        assert nick.string == f'Welcome {DATA.get("name")}!'
        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'
    
    # for some reason this won't work ;/
    # def test_logout_user(self, client, db_session) -> None:
    #     """Test user logout."""
    #     db_session.add(
    #         self.user
    #     )
    #     db_session.commit()
    #     # print(db_session.get(User, self.user.id))
    #     response = client.post(
    #         "/auth/login",
    #         data={"email": self.data.get("email"), "password": self.data.get("password")},
    #         follow_redirects=True,
    #     )
    #     assert db_session.query(User).filter_by(email=self.data.get('email')).first() != None
    #     assert response.status_code == 200
    #     simple_logs('test_logout', response.text) 
    #     soup = BeautifulSoup(response.data, 'html.parser')
    #     nick = soup.find('h1', class_='display-4')

    #     assert nick.string == f'Welcome {self.data.get("name")}!'

    #     response = client.get("/auth/logout", follow_redirects=True)
    #     assert response.status_code == 200
    #     assert response.request.path == '/'

    # there must be db_session, otherwise there is no database to register to
    def test_logout_after_registration(self, client, db_session) -> None:
        response = client.post(
            "/auth/register",
            data=DATA,
            follow_redirects=True,
        )
        assert response.status_code == 200

        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200

class TestAuthNegative:
    user: User = User(**USER)

    def test_email_taken(self, client, db_session) -> None:
        db_session.add(self.user)
        db_session.commit()
        
        assert db_session.query(User).filter_by(email=self.user.email).first() is not None
        # assert self.user == db_session.get(User, self.user.id)
        print(db_session.query(User).all())

        response = client.post(
            "/auth/register",
            data=DATA,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.request.path == '/auth/register'
        
    def test_logout_when_not_logged(self, client, db_session) -> None:
        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login'
        
    def test_login_without_account(self, client, db_session) -> None:
        response = client.post(
            "/auth/login",
            data={"email": "notexistent@gmail.com'", "password": "testpass"},
        )
        assert response.status_code == 200
        assert response.request.path == '/auth/login'
        