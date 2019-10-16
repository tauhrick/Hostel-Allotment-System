import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/../instance/server.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False