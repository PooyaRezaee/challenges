import os

class Config:
    _db_name = os.getenv("DB_NAME")
    _db_user = os.getenv("DB_USER")
    _db_password = os.getenv("DB_PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f'postgresql://{_db_user}:{_db_password}@localhost/{_db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False