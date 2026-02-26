from .database import Base, engine, SessionLocal
from extensions import db

from usuario import Usuario

def init_db():
    db.create_all()