from .database import Base, engine, SessionLocal
from extensions import db


def init_db():
    db.create_all()