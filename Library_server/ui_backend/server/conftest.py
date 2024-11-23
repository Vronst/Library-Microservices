from typing import Generator
import os
import pytest
from flask import Flask
from server import create_app
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from .models import User


DB_LOC = 'test_db.db'
DB_URI = f'sqlite:///{DB_LOC}'


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    """Set up the Flask application for testing."""
    app: Flask = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["WTF_CSRF_ENABLED"] = False

    yield app


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    """Provide a database engine for tests."""
    engine: Engine = create_engine(DB_URI)

    from server.models import metadata
    metadata.create_all(engine)
    yield engine

    metadata.drop_all(engine)
    os.unlink(DB_LOC)
    

@pytest.fixture(scope="function")
def db_session(engine):
    """Provide a clean database session for each test."""

    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session
    # Cleanup after test
    session.query(User).delete()
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def client(app):
    """Provide the Flask test client."""
    return app.test_client()
