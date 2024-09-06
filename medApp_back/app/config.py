import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:28469@localhost:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JSON_AS_ASCII = False

