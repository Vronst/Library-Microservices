import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    DATABASE_URL: str = f"postgresql+psycopg://{os.environ.get('USER_DB')}:{os.environ.get('PASSWORD_DB')}@{os.getenv('SERVER')}/{os.environ.get('POSTGRES_DB')}"
    # DATABASE_URL = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str | None = os.environ.get('SECRET_KEY')