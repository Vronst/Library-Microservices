from flask import Flask, current_app
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from .routes.main import main
from .config import Config
from .models import library, metadata


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)

    engine: Engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    metadata.create_all(engine)
    app.engine = engine # type: ignore[attr-defined]
    
    app.register_blueprint(main, url_prefix='/db/v1')
    

    @app.teardown_appcontext
    def close_connection(exception=None):
        if hasattr(current_app, "engine"):
            current_app.engine.dispose()
   
    return app