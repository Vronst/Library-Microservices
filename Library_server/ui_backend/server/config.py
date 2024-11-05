import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # DATABASE_URL = f"postgresql+psycopg2://{os.environ.get('USER_DB')}:{os.environ.get('PASSWORD_DB')}@localhost:5432/library"
    #FIXMEL: change to postgres when psycopg2 will work
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')