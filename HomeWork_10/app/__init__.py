from flask import Flask
from flask_mongoengine import MongoEngine

from config import config

app = Flask(__name__)
app.debug = True
app.config.from_object(config.Config)
db = MongoEngine(app)

from app import routes, db_models
