import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ.get('USER_DB')}:{os.environ.get('PASSWORD_DB')}@localhost:5432/Library"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')