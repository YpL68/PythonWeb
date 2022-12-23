from flask import Flask
from flask_mongoengine import MongoEngine
import redis
from redis_lru import RedisLRU

from config import config

app = Flask(__name__)
app.debug = True
app.config.from_object(config.Config)
db = MongoEngine(app)

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

from app import routes, db_models
