from datetime import datetime
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base, User, Reading as Lb
from .routes.main import main
from .routes.auth import auth as auth
from .config import Config
from .utils import login_manager

# FIXME: install psycopg2 - dll eror

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    login_manager.init_app(app)

    engine = create_engine(Config.DATABASE_URL)
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = scoped_session(sessionlocal)

    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
           
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.session = session
          
    @app.teardown_appcontext
    def remove_session(exception=None) -> None:
        session.remove()
    
    @app.before_request
    def current_year():
        g.current_year = datetime.now().year


    return app