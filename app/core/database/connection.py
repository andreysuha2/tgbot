from app.core.config import config
from mongoengine import connect

def run_db():
    connect(host=config.env.get("MONGO_DB_URL"))