import pathlib
from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).parent.parent
config = dotenv_values(".env")


class Config:
    MONGODB_SETTINGS = {"host": "mongodb://localhost/assist"}
    SECRET_KEY = config['SECRET_KEY']

