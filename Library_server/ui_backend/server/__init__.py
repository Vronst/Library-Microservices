from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base, User, Reading as Lb
from .routes import main
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
   
        
    @app.teardown_appcontext
    def remove_session(exception=None) -> None:
        session.remove()

    return app