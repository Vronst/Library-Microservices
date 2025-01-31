from bs4 import BeautifulSoup
from flask import url_for, request
from ...conftest import USER, DATA, ADATA, ADMIN
from ...models import User
from ...utils import simple_logs


class TestAdminPositive:
    user: User = User(**USER)
    admin_user: User = User(**ADMIN)
    
    def test_admin_logged_access(self, client, db_session) -> None:
        """Test access to admin panel by admin user."""
        db_session.add(
            self.admin_user
        )
        db_session.commit()
        assert db_session.query(User).filter_by(nick=self.admin_user.nick).first() is not None
        response = client.post(
            "/auth/login",
            data={"email": ADATA.get('email'), "password": ADATA.get('password')}
            )
        simple_logs("test_admin_logged_access-redirect", response.text)
        assert response.status_code == 302
        response = client.get(url_for('admin.index'))
        simple_logs("test_admin_logged_access", response.text)
        assert response.status_code == 200
        assert response.request.path == url_for("admin.index")


class TestAdminNegative:
    user: User = User(**USER)
    
    def test_not_logged_admin_access(self, client, db_session) -> None:
        """Test access to admin panel by unlogged user."""
        response = client.get(
            "/admin",
            follow_redirects=True,
        )
        assert response.status_code == 200

        assert request.path == url_for("auth.login")
    
    def test_not_admin_logged_access(self, client, db_session) -> None:
        """Test access to admin panel by not admin user."""
        db_session.add(
            self.user
        )
        db_session.commit()
        assert db_session.query(User).filter_by(nick=self.user.nick).first() is not None
        redirect = client.post(
            "/auth/login",
            data={"email": DATA.get('email'), "password": DATA.get('password')}
            )
        assert redirect.status_code == 302
        response = client.get(
            '/admin', follow_redirects=True
        )

        simple_logs("test_not_admin_logged_access", response.text)
        assert response.status_code ==403
        assert response.request.path == url_for('admin.index')
        