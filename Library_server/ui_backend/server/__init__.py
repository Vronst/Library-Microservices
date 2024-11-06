from datetime import datetime
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base, User, Reading as Lb
from .routes.main import main
from .routes.auth import main as auth
from .config import Config

# FIXME: install psycopg2 - dll eror

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = scoped_session(SessionLocal)

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