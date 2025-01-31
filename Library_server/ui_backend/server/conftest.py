from typing import Generator, Any
import os
import pytest
from flask import Flask
from server import create_app
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from .models import metadata, User  # Ensure all models are imported
from .config import TestConfig


DB_LOC = 'test.db'
DB_URI = f'sqlite:///{DB_LOC}'
USER: dict[str, Any]
DATA: dict[str, str]
USER, ADMIN, DATA, ADATA = {
    "admin": False,
    "nick": 'main_test',
    "name": 'tester',
    "surname": 'test1',
    "email": 'test@test.pl',
    "password": generate_password_hash('testpass', salt_length=24),
     },\
    {
        'admin': True,
        'nick': 'adam',
        'name': 'adam',
        'surname': 'adam',
        'email': 'adam@example.com',
        'password': generate_password_hash('adam', salt_length=24),
    },\
    {
    "nick": "main_test",    
    "name": "tester",
    "surname": "test1",
    "email": "test@test.pl",
    "password": "testpass",
    'repeat_password': 'testpass',
      },\
    {
        'nick': 'adam',
        'name': 'adam',
        'surname': 'adam',
        'email': 'adam@example.com',
        'password': 'adam',
    }


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    """Set up the Flask application for testing."""
    app: Flask = create_app(testing=True)
    # app.config["TESTING"] = True
    # app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    # app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests

    yield app  # Provide the app for tests

    # if os.path.exists(DB_LOC):
        # os.unlink(DB_LOC)
        

@pytest.fixture(scope="session")
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


@pytest.fixture(scope="function")
def db_session(engine):
    """Provide a clean database session for each test."""
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session  # Provide the session for tests
    finally:
        # Rollback uncommitted changes and close the session
        # session.rollback()
        # session.query(User).delete()
        for table in reversed(metadata.sorted_tables):  # Reverse order to avoid FK issues
            session.execute(table.delete())
        session.commit() 
        session.close()


@pytest.fixture(scope="session")
def client(app):
    """Provide the Flask test client."""
    # return app.test_client()
    with app.test_client() as client:
        yield client
