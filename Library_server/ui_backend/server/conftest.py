from typing import Generator
import os
import pytest
from flask import Flask
from server import create_app
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from .models import metadata, User  # Ensure all models are imported

DB_LOC = 'test_db.db'
DB_URI = f'sqlite:///{DB_LOC}'


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    """Set up the Flask application for testing."""
    app: Flask = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests

    yield app  # Provide the app for tests


@pytest.fixture(scope="function")
def engine() -> Generator[Engine, None, None]:
    """Provide a database engine for tests."""
    engine: Engine = create_engine(DB_URI)

    # Create all tables before tests
    metadata.create_all(engine)
    try:
        yield engine  # Provide the engine for tests
    finally:
        # Drop all tables and clean up the database
        metadata.drop_all(engine)
        if os.path.exists(DB_LOC):
            os.unlink(DB_LOC)


@pytest.fixture(scope="function")
def db_session(engine):
    """Provide a clean database session for each test."""
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session  # Provide the session for tests
    finally:
        # Rollback uncommitted changes and close the session
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(app):
    """Provide the Flask test client."""
    return app.test_client()
