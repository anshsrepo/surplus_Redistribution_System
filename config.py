import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default_secret_key"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root123@localhost/charity_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
