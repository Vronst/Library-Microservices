from datetime import datetime
from typing import Any
from flask import Flask, g
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base, User, Reading as Lb
from .routes.main import main
from .routes.auth import auth as auth
from .config import Config
from .utils import login_manager


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)

    login_manager.init_app(app)

    engine: Engine = create_engine(Config.DATABASE_URL)
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = scoped_session(sessionlocal)

    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
           
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.session = session # type: ignore[attr-defined]
          
    @app.teardown_appcontext
    def remove_session(exception=None) -> None:
        session.remove()
    
    @app.before_request
    def current_year() -> None:
        g.current_year = datetime.now().year


    return app